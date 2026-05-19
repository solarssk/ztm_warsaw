import logging
import voluptuous as vol
import aiohttp
import re
import urllib.parse
import asyncio
import json

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_API_KEY, CONF_BUSSTOP_ID, CONF_BUSSTOP_NR, CONF_LINE, CONF_DEPARTURES



_LOGGER = logging.getLogger(__name__)

TIMEOUT = aiohttp.ClientTimeout(total=20)
RETRIES = 1   # number of retries for timeout/5xx during validation
BACKOFF = 1.5 # seconds backoff multiplier


def _sanitize_url(url: str) -> str:
    """Mask apikey in URL for safe logging."""
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    if "apikey" in query:
        query["apikey"] = ["****"] * len(query["apikey"])
    masked_query = urllib.parse.urlencode(query, doseq=True)
    sanitized_url = urllib.parse.urlunparse(parsed._replace(query=masked_query))
    return sanitized_url


async def _get_json(session: aiohttp.ClientSession, url: str) -> dict:
    """GET URL and return parsed JSON with a small retry.
    # English-only comments for OSS clarity
    """
    attempt = 0
    while True:
        try:
            async with session.get(url, timeout=TIMEOUT) as resp:
                text = await resp.text()
                # Retry on 5xx
                if 500 <= resp.status <= 599 and attempt < RETRIES:
                    _LOGGER.warning("HTTP %s for %s; retrying (%s/%s)", resp.status, _sanitize_url(url), attempt + 1, RETRIES)
                    attempt += 1
                    await asyncio.sleep(BACKOFF * attempt)
                    continue
                if resp.status != 200:
                    _LOGGER.error("API HTTP error %s for %s body=%s", resp.status, _sanitize_url(url), text[:300])
                    raise ValueError("api_http_error")
                try:
                    return json.loads(text)
                except Exception:
                    _LOGGER.error("API returned invalid JSON for %s body=%s", _sanitize_url(url), text[:300])
                    raise ValueError("api_http_error")
        except asyncio.TimeoutError:
            if attempt < RETRIES:
                _LOGGER.warning("Timeout for %s; retrying (%s/%s)", _sanitize_url(url), attempt + 1, RETRIES)
                attempt += 1
                await asyncio.sleep(BACKOFF * attempt)
                continue
            _LOGGER.error("API timeout after %ss for %s", TIMEOUT, _sanitize_url(url))
            raise ValueError("api_connection_error")
        except aiohttp.ClientError as e:
            _LOGGER.error("API connection error for %s: %s", _sanitize_url(url), e)
            raise ValueError("api_connection_error")

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_KEY): str,
    vol.Required(CONF_BUSSTOP_ID): vol.Coerce(int),
    vol.Required(CONF_BUSSTOP_NR): str,
    vol.Required(CONF_LINE): str,
    vol.Required(CONF_DEPARTURES, default=1): vol.In({
        1: "Next departure",
        2: "Next two departures",
        3: "Next three departures"
    }),
})

async def validate_input(api_key, stop_id, stop_nr, line):
    """Validate input against City of Warsaw API."""
    line_check_url = (
        "https://api.um.warszawa.pl/api/action/dbtimetable_get/"
        "?id=88cd555f-6f31-43ca-9de4-66c479ad5942"
        f"&busstopId={stop_id}"
        f"&busstopNr={stop_nr}"
        f"&apikey={api_key}"
    )

    timetable_url = (
        "https://api.um.warszawa.pl/api/action/dbtimetable_get/"
        "?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238"
        f"&busstopId={stop_id}"
        f"&busstopNr={stop_nr}"
        f"&line={line}"
        f"&apikey={api_key}"
    )

    try:
        async with aiohttp.ClientSession() as session:
            # 1) Verify stop/line exists for given stop_id/stop_nr
            data = await _get_json(session, line_check_url)
            if data.get("result") == "false":
                # ZTM returns string "false" on errors (incl. bad apikey)
                raise ValueError("invalid_api_key")
            result = data.get("result")
            if result is None:
                raise ValueError("line_check_failed")
            if not isinstance(result, list):
                _LOGGER.error("Unexpected result type in line_check: %s", type(result).__name__)
                raise ValueError("line_check_failed")

            available_lines = []
            for item in result:
                if not isinstance(item, dict):
                    continue
                vals = item.get("values") or []
                if isinstance(vals, list):
                    for val in vals:
                        if isinstance(val, dict) and val.get("key") == "linia":
                            available_lines.append(val.get("value"))

            if line not in available_lines:
                raise ValueError("line_not_found")

            # 2) Verify timetable returns at least one valid HH:MM:SS entry
            data = await _get_json(session, timetable_url)
            if data.get("result") == "false":
                raise ValueError("invalid_api_key")
            result = data.get("result")
            if result is None:
                raise ValueError("no_departures")
            if not isinstance(result, list):
                _LOGGER.error("Unexpected result type in timetable: %s", type(result).__name__)
                raise ValueError("no_departures")

            for item in result:
                if not isinstance(item, list):
                    continue
                czas = next((v.get("value") for v in item if isinstance(v, dict) and v.get("key") == "czas"), None)
                if isinstance(czas, str) and re.match(r"^\d{2}:\d{2}:\d{2}$", czas):
                    return True

            raise ValueError("no_valid_times")

    except ValueError:
        raise
    except Exception as e:
        _LOGGER.exception("Unexpected error during validation: %s", e)
        raise ValueError("unknown")

class ZtmWarsawConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg]
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Validate stop number format
            if not user_input[CONF_BUSSTOP_NR].isdigit() or len(user_input[CONF_BUSSTOP_NR]) != 2:
                errors["base"] = "invalid_stop_number"
            else:
                try:
                    await validate_input(
                        user_input[CONF_API_KEY],
                        user_input[CONF_BUSSTOP_ID],
                        user_input[CONF_BUSSTOP_NR],
                        user_input[CONF_LINE],
                    )
                except ValueError as err:
                    key = str(err)
                    errors["base"] = key
                    _LOGGER.warning("Validation error: %s", key)
                except Exception as e:
                    _LOGGER.exception("Unexpected error: %s", e)
                    errors["base"] = "unknown"
                else:
                    title = f"Line {user_input[CONF_LINE]} from {user_input[CONF_BUSSTOP_ID]}/{user_input[CONF_BUSSTOP_NR]}"
                    return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ZtmWarsawOptionsFlow(config_entry)


class ZtmWarsawOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        schema = vol.Schema({
            vol.Optional(
                CONF_DEPARTURES,
                default=self._config_entry.options.get(
                    CONF_DEPARTURES,
                    self._config_entry.data.get(CONF_DEPARTURES, 1),
                )
            ): vol.In({
                1: "Next departure",
                2: "Next two departures",
                3: "Next three departures",
            })
        })

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders={},
        ) 