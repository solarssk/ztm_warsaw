import logging
from datetime import datetime, timezone, timedelta, date
from urllib.parse import quote
from homeassistant.util.dt import as_local

from .utils import get_line_type, get_line_icon

from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.core import callback

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import EntityCategory

from .client import ZTMStopClient
from .const import CONF_DEPARTURES, DOMAIN, CONF_ATTRIBUTION
from .coordinator import ZTMStopCoordinator

_LOGGER = logging.getLogger(__name__)

def _friendly_day(dt):
    """Helper to show friendly day names relative to today."""
    if not dt:
        return "Not available"
    
    try:
        today = datetime.now(tz=timezone.utc).astimezone().date()
        dt_date = dt.astimezone().date()
        
        if dt_date == today:
            return "today"
        if dt_date == (today + timedelta(days=1)):
            return "tomorrow"
        if dt_date == (today - timedelta(days=1)):
            return "yesterday"
        return dt.strftime("%a")  # Mon, Tue ...
    except (AttributeError, TypeError):
        return "Not available"


class ZTMSensor(CoordinatorEntity, SensorEntity):
    """Sensor for tracking ZTM departures."""
    
    def __init__(self, coordinator, entry_id, stop_id, stop_number, line, max_departures):
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._line = line
        self._stop_id = stop_id
        self._stop_number = stop_number
        self._max_departures = max_departures
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_unique_id = f"line_{line}_from_{stop_id}_{stop_number}"
        
        # Get stop name from coordinator if available
        stop_info = self._get_stop_info()
        stop_name = stop_info.get("nazwa_zespolu") if stop_info else None
        if stop_name:
            self._attr_name = f"Line {line} {stop_name} {stop_number}"
        else:
            self._attr_name = f"Line {line} from {stop_id}/{stop_number}"
        
        # Base attributes that don't change
        self._base_attrs = {
            "Line, Number": self._line,
            "Line, Type": get_line_type(self._line),
            "Line, Timezone": "Europe/Warsaw",
            "Line, Full Timetable": f"https://www.wtp.waw.pl/rozklady-jazdy/?wtp_md=3&wtp_ln={quote(str(self._line))}",
            "Stop, ID": self._stop_id,
            "Stop, Number": self._stop_number,
        }
        
        # Attribute placeholders for no service
        self._no_service_attrs = {
            "Upcoming, Headsign": "No service",
            "Upcoming, Departure Day": "Not available",
            "Upcoming, Route ID": "Not available",
            "Upcoming, Brigade": "Not available",
        }
        
        # Initialize attributes and state
        self._attributes = {}
        self._next_departure = None
        self._previous_departure = None
        self._scheduled_unsub = None
        self._last_coordinator_update = None
        
        # Don't set entity_id manually - let HA handle it

    def _get_stop_info(self):
        """Safely get stop info from coordinator data."""
        try:
            if self.coordinator and self.coordinator.data:
                return getattr(self.coordinator.data, "stop_info", {}) or {}
        except (AttributeError, TypeError):
            pass
        return {}

    def _is_night_line(self, line):
        """Check if this is a night line (starting with N)."""
        return str(line).upper().startswith('N')

    def _is_in_schedule_refresh_window(self, current_time):
        """Check if we're in the schedule refresh window (00:00-2:40)."""
        if not current_time:
            return False
        
        current_hour = current_time.hour
        current_minute = current_time.minute
        return current_hour < 2 or (current_hour == 2 and current_minute < 40)

    def _get_schedule_date(self, now: datetime) -> date:
        """Determine logical schedule day (shifted if before 2:30)."""
        if now.hour < 2 or (now.hour == 2 and now.minute < 40):
            return (now - timedelta(days=1)).date()
        return now.date()

    def _timetable_url(self):
        """Generate timetable URL for today."""
        try:
            today_str = datetime.now(tz=timezone.utc).astimezone().strftime("%Y-%m-%d")
            return f"https://www.wtp.waw.pl/rozklady-jazdy/?wtp_dt={today_str}&wtp_md=3&wtp_ln={quote(str(self._line))}"
        except Exception:
            return f"https://www.wtp.waw.pl/rozklady-jazdy/?wtp_md=3&wtp_ln={quote(str(self._line))}"

    @property
    def native_value(self):
        """Return the next departure as a timezone‑aware datetime (or None)."""
        return self._next_departure

    @property
    def icon(self):
        """Return appropriate icon based on transport type."""
        return get_line_icon(self._line)

    @property
    def extra_state_attributes(self):
        """Return attributes, excluding any None values to satisfy recorder."""
        attributes = self._attributes or {}
        return {k: v for k, v in attributes.items() if v is not None}

    @property
    def device_info(self):
        """Return device info for this entity."""
        return {
            "identifiers": {(DOMAIN, f"line_{self._line}")},
            "name": f"Line {self._line}",
            "manufacturer": "Zarząd Transportu Miejskiego",
            "entry_type": "service",
            "model": get_line_type(self._line),
            "configuration_url": self._timetable_url(),
        }

    def _cancel_scheduled_update(self):
        """Cancel any scheduled update."""
        if self._scheduled_unsub:
            self._scheduled_unsub()
            self._scheduled_unsub = None

    def _schedule_update_at_departure(self, departure_time):
        """Schedule update at specific departure time."""
        if not departure_time:
            return
        
        # Don't schedule if departure time is in the past
        from homeassistant.util.dt import now as ha_utcnow
        now = ha_utcnow().astimezone()
        if departure_time <= now:
            _LOGGER.debug("Not scheduling update for past departure time: %s", departure_time)
            return
        
        try:
            self._cancel_scheduled_update()
            self._scheduled_unsub = async_track_point_in_time(
                self.hass, self._scheduled_update, departure_time
            )
            _LOGGER.debug("Scheduled update for %s at %s", self.entity_id, as_local(departure_time))
        except Exception as e:
            _LOGGER.error("Failed to schedule update for %s: %s", self.entity_id, e)

    def _update_from_coordinator(self):
        """Update state and attributes based on coordinator data."""
        from homeassistant.util.dt import now as ha_utcnow
        
        if not self.coordinator or not self.coordinator.data:
            _LOGGER.warning("No timetable data available from coordinator for %s", self.entity_id)
            self._set_no_departures()
            self.async_write_ha_state()
            return

        data = self.coordinator.data
        
        # Check if coordinator has new data
        current_coordinator_update = self.coordinator.last_update_success_time
        if current_coordinator_update != self._last_coordinator_update:
            _LOGGER.info("Coordinator has new data for %s, forcing full update", self.entity_id)
            self._last_coordinator_update = current_coordinator_update
            self._cancel_scheduled_update()
        
        # Validate and filter departures
        valid_departures = []
        for d in (data.departures or []):
            if hasattr(d, 'dt') and d.dt and isinstance(d.dt, datetime):
                valid_departures.append(d)
            else:
                _LOGGER.debug("Skipping invalid departure: %s", d)
        
        if not valid_departures:
            _LOGGER.info("No valid departures found for %s", self.entity_id)
            self._set_no_departures()
            self.async_write_ha_state()
            return
        
        _LOGGER.debug("Found %d valid departures for %s", len(valid_departures), self.entity_id)
        
        # Sort departures by time
        try:
            departures = sorted(valid_departures, key=lambda d: d.dt)
        except Exception as e:
            _LOGGER.error("Failed to sort departures for %s: %s", self.entity_id, e)
            self._set_no_departures()
            self.async_write_ha_state()
            return

        # Get current time
        now_warsaw = ha_utcnow().astimezone()
        _LOGGER.debug("Current Warsaw time: %s", now_warsaw)
        
        _LOGGER.debug("DEBUG %s: Current time: %s, Is night line: %s",
                    self.entity_id, now_warsaw, self._is_night_line(self._line))
        
        # Filter out early next-day departures if we're between the last departure and 2:30,
        # to avoid the false impression that the morning schedule is already in effect.
        # Cutoff threshold for day schedule between midnight and 2:30
        cutoff_hour = 2
        cutoff_minute = 30
        cutoff_time = now_warsaw.replace(hour=cutoff_hour, minute=cutoff_minute, second=0, microsecond=0)
        if now_warsaw > cutoff_time:
            cutoff_time = cutoff_time + timedelta(days=1)

        future_departures = []
        for d in departures:
            if d.dt >= now_warsaw:
                if self._is_night_line(self._line):
                    future_departures.append(d)
                else:
                    # For day lines
                    schedule_date = self._get_schedule_date(now_warsaw)
                    same_day = d.dt.date() == schedule_date
                    before_cutoff = d.dt <= cutoff_time
                    if same_day or before_cutoff:
                        future_departures.append(d)
        
        _LOGGER.debug("DEBUG %s: Total departures: %d, Future departures: %d",
                    self.entity_id, len(departures), len(future_departures))
        all_sorted = sorted(data.departures, key=lambda d: d.dt)
        first_dep = all_sorted[0].dt if all_sorted else None
        last_dep = all_sorted[-1].dt if all_sorted else None
        _LOGGER.debug("DEBUG %s: First departure (raw): %s, Last departure (raw): %s",
                    self.entity_id, as_local(first_dep) if first_dep else None, as_local(last_dep) if last_dep else None)

        # UPDATED LOGIC: Check whether to hide schedule after last departure
        if not future_departures and not self._is_night_line(self._line):
            # For day lines without future departures
            last_departure = departures[-1].dt if departures else None
            current_hour = now_warsaw.hour
            current_minute = now_warsaw.minute

            # Check if we are in the 00:00–02:30 window
            in_night_window = current_hour < 2 or (current_hour == 2 and current_minute <= 30)

            if last_departure:
                time_since_last = now_warsaw - last_departure
                # Add detailed logging
                _LOGGER.debug(">>> last_departure=%s, now=%s, since_last=%s, in_night_window=%s",
                              last_departure, now_warsaw, time_since_last, in_night_window)
                # New precise condition: hide schedule only in night window and if 5+ minutes passed since last departure
                if in_night_window and time_since_last > timedelta(minutes=5):
                    _LOGGER.info("Day line %s: hiding schedule (new rule) - last departure at %s (%s ago), current time %s [in night window]",
                            self._line, last_departure, time_since_last, now_warsaw)
                    self._set_no_departures()
                    self.async_write_ha_state()
                    return
        
        # If there are no future departures and we are not hiding the schedule
        if not future_departures:
            _LOGGER.info("No future departures found for %s", self.entity_id)
            self._previous_departure = self._next_departure
            self._next_departure = None
            self._set_no_departures()
            self.async_write_ha_state()
            return
        
        # Update stop name if available
        self._update_stop_name()
        
        # Update state and attributes
        self._update_departure_info(future_departures, now_warsaw)
        
        # Schedule next update
        next_departure = future_departures[0]
        self._schedule_update_at_departure(next_departure.dt)
        
        # Notify Home Assistant of state change (only once)
        self.async_write_ha_state()

    def _update_stop_name(self):
        """Update friendly name if stop info is now available."""
        stop_info = self._get_stop_info()
        stop_name = stop_info.get("nazwa_zespolu")
        if stop_name:
            new_name = f"Line {self._line} {stop_name} {self._stop_number}"
            if self._attr_name != new_name:
                _LOGGER.info("Updating friendly name for %s to: %s", self.entity_id, new_name)
                self._attr_name = new_name

    def _update_departure_info(self, future_departures, now_warsaw):
        """Update departure information and attributes."""
        if not future_departures:
            return
        
        # Update next departure
        new_departure = future_departures[0].dt
        self._previous_departure = self._next_departure
        self._next_departure = new_departure
        
        _LOGGER.info("Next departure for %s: %s → %s", 
                    self.entity_id, as_local(new_departure), future_departures[0].kierunek)

        # Start with base attributes
        self._attributes = dict(self._base_attrs)
        
        # Add stop information
        stop_info = self._get_stop_info()
        self._attributes["Stop, Name"] = stop_info.get("nazwa_zespolu", "Not available")
        self._attributes["Stop, Street ID"] = stop_info.get("id_ulicy", "Not available")
        self._attributes["Stop, Latitude"] = stop_info.get("szer_geo", "Not available")
        self._attributes["Stop, Longitude"] = stop_info.get("dlug_geo", "Not available")
        self._attributes["Stop, Timezone"] = "Europe/Warsaw"
        self._attributes[ATTR_ATTRIBUTION] = CONF_ATTRIBUTION

        # Add current departure information
        current = future_departures[0]
        self._attributes["Upcoming, Headsign"] = getattr(current, 'kierunek', 'Not available')
        self._attributes["Upcoming, Departure Day"] = _friendly_day(current.dt)
        self._attributes["Upcoming, Route ID"] = getattr(current, 'trasa', 'Not available')
        self._attributes["Upcoming, Brigade"] = getattr(current, 'brygada', 'Not available')

        # Add information about next departures
        for seq, dep in enumerate(future_departures[1:self._max_departures + 1], start=1):
            try:
                local_dt = dep.dt.astimezone(now_warsaw.tzinfo)
                time_str = local_dt.strftime("%H:%M")
                self._attributes[f"Next {seq}, Headsign"] = getattr(dep, 'kierunek', 'Not available')
                self._attributes[f"Next {seq}, Departure Day"] = _friendly_day(local_dt)
                self._attributes[f"Next {seq}, Departure Time"] = time_str
                self._attributes[f"Next {seq}, Route ID"] = getattr(dep, 'trasa', 'Not available')
                self._attributes[f"Next {seq}, Brigade"] = getattr(dep, 'brygada', 'Not available')
            except Exception as e:
                _LOGGER.warning("Failed to process departure %d for %s: %s", seq, self.entity_id, e)

    @callback
    def _scheduled_update(self, now):
        """Callback triggered at scheduled departure time to refresh state."""
        _LOGGER.info("Scheduled update triggered for %s at departure time (%s)", self.entity_id, as_local(now))
        self._update_from_coordinator()

    def _set_no_departures(self):
        """Set attributes for no departures case."""
        # Cancel any scheduled update
        self._cancel_scheduled_update()

        # Start with base attributes
        self._attributes = dict(self._base_attrs)

        # Use timetable url helper
        self._attributes["Line, Full Timetable"] = self._timetable_url()

        # Add stop info if available
        stop_info = self._get_stop_info()
        if stop_info:
            self._attributes["Stop, Name"] = stop_info.get("nazwa_zespolu", "Not available")
            self._attributes["Stop, Street ID"] = stop_info.get("id_ulicy", "Not available")
            self._attributes["Stop, Latitude"] = stop_info.get("szer_geo", "Not available")
            self._attributes["Stop, Longitude"] = stop_info.get("dlug_geo", "Not available")
        else:
            self._attributes["Stop, Name"] = "Not available"
            self._attributes["Stop, Street ID"] = "Not available"
            self._attributes["Stop, Latitude"] = "Not available"
            self._attributes["Stop, Longitude"] = "Not available"
            self._attributes["Stop, Direction"] = "Not available"
            self._attributes["Stop, Effective From"] = "Not available"

        # Set timezone
        self._attributes["Stop, Timezone"] = "Europe/Warsaw"

        # Only set no service attributes (do not set Upcoming..., Next..., etc.)
        self._attributes.update(self._no_service_attrs)

        # Set note and attribution
        self._attributes["Note"] = "No upcoming schedule available. Please verify on wtp.waw.pl or call 19115."
        self._attributes[ATTR_ATTRIBUTION] = CONF_ATTRIBUTION

        # Update state if changed
        if self._next_departure is not None:
            self._previous_departure = None
            self._next_departure = None
        else:
            self._previous_departure = None

    async def async_will_remove_from_hass(self):
        """Cancel any scheduled listener when removing."""
        self._cancel_scheduled_update()
        await super().async_will_remove_from_hass()
        
    async def async_added_to_hass(self):
        """When entity is added to Home Assistant."""
        await super().async_added_to_hass()
        self._update_from_coordinator()
        
    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator and self.coordinator.last_update_success
        
    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        _LOGGER.debug("Coordinator update received for %s", self.entity_id)
        self._update_from_coordinator()


class ZTMLastUpdateSensor(CoordinatorEntity, SensorEntity):
    """Sensor to expose the last successful update time from coordinator."""

    def __init__(self, coordinator, line, stop_id, stop_number):
        super().__init__(coordinator)
        self._attr_entity_registry_enabled_default = False
        self._line = line
        self._stop_id = stop_id
        self._stop_number = stop_number
        
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_unique_id = f"line_{line}_from_{stop_id}_{stop_number}_last_update"
        
        # Set friendly name
        stop_info = self._get_stop_info()
        stop_name = stop_info.get('nazwa_zespolu') if stop_info else stop_id
        self._attr_name = f"Line {line} {stop_name} {stop_number} Last update"

    def _get_stop_info(self):
        """Safely get stop info from coordinator data."""
        try:
            if self.coordinator and self.coordinator.data:
                return getattr(self.coordinator.data, "stop_info", {}) or {}
        except (AttributeError, TypeError):
            pass
        return {}

    @property
    def native_value(self):
        """Return last update time."""
        if not self.coordinator:
            return None
        
        last_update = getattr(self.coordinator, "last_update_success_time", None)
        return last_update if isinstance(last_update, datetime) else None

    def _timetable_url(self):
        """Generate timetable URL for today."""
        try:
            today_str = datetime.now(tz=timezone.utc).astimezone().strftime("%Y-%m-%d")
            return f"https://www.wtp.waw.pl/rozklady-jazdy/?wtp_dt={today_str}&wtp_md=3&wtp_ln={quote(str(self._line))}"
        except Exception:
            return f"https://www.wtp.waw.pl/rozklady-jazdy/?wtp_md=3&wtp_ln={quote(str(self._line))}"

    @property
    def device_info(self):
        """Return device info for this entity."""
        return {
            "identifiers": {(DOMAIN, f"line_{self._line}")},
            "name": f"Line {self._line}",
            "manufacturer": "Zarząd Transportu Miejskiego",
            "entry_type": "service",
            "model": get_line_type(self._line),
            "configuration_url": self._timetable_url(),
        }

    @property
    def extra_state_attributes(self):
        """Return extra attributes for diagnostics."""
        if not self.coordinator:
            return {}

        departures_count = 0
        if self.coordinator.data and hasattr(self.coordinator.data, 'departures'):
            departures_count = len(self.coordinator.data.departures or [])
        
        return {
            "Last update successful": getattr(self.coordinator, 'last_update_success', False),
            "Number of fetched departures": departures_count,
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
        }


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up ZTM sensor from a config entry."""
    try:
        # Read configuration and options
        data = config_entry.data
        options = config_entry.options

        stop_id = str(data["busstop_id"])
        stop_number = str(data["busstop_nr"])
        line = data["line"]
        # Use departures option if set, else fallback to initial data
        departures = options.get(CONF_DEPARTURES, data.get(CONF_DEPARTURES, 1))

        # Create session and client
        session = async_get_clientsession(hass)
        client = ZTMStopClient(
            session=session,
            api_key=data["api_key"],
            stop_id=stop_id,
            stop_number=stop_number,
            line=line,
        )

        # Create coordinator
        coordinator = ZTMStopCoordinator(
            hass=hass,
            client=client,
            stop_id=stop_id,
            stop_nr=stop_number,
            line=line,
        )

        # Initialize coordinator
        await coordinator.async_config_entry_first_refresh()
        hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = coordinator

        # Create entities
        entity = ZTMSensor(
            coordinator=coordinator,
            entry_id=config_entry.entry_id,
            stop_id=stop_id,
            stop_number=stop_number,
            line=line,
            max_departures=departures,
        )

        diag_sensor = ZTMLastUpdateSensor(
            coordinator=coordinator,
            line=line,
            stop_id=stop_id,
            stop_number=stop_number,
        )

        entities = [entity, diag_sensor]

        # Add entities
        async_add_entities(entities)
        
        _LOGGER.info("Successfully set up ZTM sensors for line %s at stop %s/%s", 
                    line, stop_id, stop_number)

    except Exception as e:
        _LOGGER.error("Failed to set up ZTM sensor: %s", e)
        raise
