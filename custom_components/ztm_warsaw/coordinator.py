import logging
from datetime import datetime, timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
import asyncio
import random
from homeassistant.helpers.event import async_call_later, async_track_time_interval

from .client import ZTMStopClient
from .models import ZTMDepartureData, ZTMDepartureDataReading

_LOGGER = logging.getLogger(__name__)

class ZTMStopCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, stop_id: str, stop_nr: str, line: str, client: ZTMStopClient):
        super().__init__(
            hass,
            _LOGGER,
            name=f"line_{line}_from_{stop_id}_{stop_nr}",
            update_method=self._async_update_data,
        )
        self.stop_id = stop_id
        self.stop_nr = stop_nr
        self.line = line
        self.client = client
        self.data: ZTMDepartureData | None = None
        self.last_update_success_time: datetime | None = None
        self._initial_refresh_done = False
        self._daily_refresh_unsub = None
        self._retry_unsub = None
        self._retry_delay_seconds = 120  # seconds; coordinator-level retry after a failed 02:30 refresh
        self._jitter_max_seconds = 45    # spread refresh calls to avoid thundering herd
        self._midnight_refresh_unsub = None
        self._last_success_local_date = None  # Europe/Warsaw date of last successful fetch
        self._last_stopinfo_refresh_date = None  # Europe/Warsaw date of last stop-info refresh

        self._minute_unsub = None  # 1-minute heartbeat for UI advance

        # Hourly timetable refresh handled by DataUpdateCoordinator
        self.update_interval = timedelta(hours=1)

    async def async_config_entry_first_refresh(self):
        """Perform first refresh and set up schedules."""
        if not self._initial_refresh_done:
            _LOGGER.debug("ZTM Coordinator [%s] — performing initial refresh", self.name)
            await self.async_refresh()
            self._initial_refresh_done = True

            # Ensure stop info is present once at startup (no repeated fetches later)
            try:
                if getattr(self.client, "_stop_name", None) is None:
                    await self.client.get_stop_name()
                    self._last_stopinfo_refresh_date = dt_util.now().date()
            except Exception:
                _LOGGER.debug("ZTM Coordinator [%s] — initial stop-info fetch skipped (non-fatal)", self.name)

        # Cancel existing schedules
        if self._daily_refresh_unsub:
            self._daily_refresh_unsub()
            self._daily_refresh_unsub = None
        if self._retry_unsub:
            self._retry_unsub()
            self._retry_unsub = None

        # Minute heartbeat: notify sensors to advance state every minute without network I/O
        if self._minute_unsub:
            self._minute_unsub()
            self._minute_unsub = None
        self._minute_unsub = async_track_time_interval(
            self.hass,
            self._minute_tick,
            timedelta(minutes=1),
        )

        _LOGGER.debug(
            "ZTM Coordinator [%s] — hourly timetable refresh enabled; no scheduled stop-info refresh",
            self.name,
        )


    async def _minute_tick(self, _now):
        """Push an update to listeners so sensors recompute next departures against current time.
        This does not trigger network refresh; it only re-renders based on cached data.
        """
        try:
            self.async_update_listeners()
        except Exception:  # defensive: never let UI tick crash
            pass


    async def _async_update_data(self) -> ZTMDepartureData:
        _LOGGER.debug("ZTM Coordinator [%s] — fetching new schedule data", self.name)
        try:
            new_data = await self.client.get()
            if new_data is None:
                if self.data is not None:
                    _LOGGER.warning(
                        "ZTM Coordinator [%s] — timetable fetch failed; keeping cached data",
                        self.name,
                    )
                    return self.data
                raise UpdateFailed("Timetable fetch failed and no cached data available")
            
            data_changed = False
            if self.data is None:
                data_changed = True
                _LOGGER.info("ZTM Coordinator [%s] — first data load", self.name)
            elif len(new_data.departures) != len(self.data.departures):
                data_changed = True
                _LOGGER.info(
                    "ZTM Coordinator [%s] — departure count changed: %d → %d", 
                    self.name, len(self.data.departures), len(new_data.departures)
                )
            else:
                old_times = [d.czas for d in self.data.departures]
                new_times = [d.czas for d in new_data.departures]
                if old_times != new_times:
                    data_changed = True
                    _LOGGER.info("ZTM Coordinator [%s] — departure times changed", self.name)
            
            self.data = new_data
            self.last_update_success_time = dt_util.utcnow()
            # Track last success date in local time (Europe/Warsaw)
            self._last_success_local_date = dt_util.now().date()
            
            if data_changed:
                _LOGGER.info("ZTM Coordinator [%s] — new schedule data available, notifying sensors", self.name)
            count = len(new_data.departures)
            _LOGGER.debug(
                "ZTM Coordinator [%s] — successfully fetched %d departures%s",
                self.name,
                count,
                " (empty set)" if count == 0 else "",
            )
            return new_data
            
        except UpdateFailed:
            raise
        except Exception as err:
            if self.data is not None:
                # Keep entity available with last known data; try again on next hourly tick
                _LOGGER.warning(
                    "ZTM Coordinator [%s] — fetch failed (%s); keeping last known timetable and retrying next hour",
                    self.name,
                    err,
                )
                return self.data
            _LOGGER.error("ZTM Coordinator [%s] — failed fetching schedule and no cached data", self.name)
            raise UpdateFailed(f"Error fetching data: {err}") from err

    async def async_shutdown(self):
        """Clean up when coordinator is being shut down."""
        if self._daily_refresh_unsub:
            self._daily_refresh_unsub()
            self._daily_refresh_unsub = None
        if self._retry_unsub:
            self._retry_unsub()
            self._retry_unsub = None
        if self._minute_unsub:
            self._minute_unsub()
            self._minute_unsub = None
        self.data = None
        _LOGGER.info("ZTM Coordinator [%s] — shutdown complete", self.name)
