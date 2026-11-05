"""Check the integration in native Core without the stale pytest plugin."""

import asyncio
import json
import tempfile
import shutil
from pathlib import Path
from homeassistant import bootstrap, loader
from homeassistant.const import __version__
from homeassistant.components.marketplace.repositories.integration import (
    _check_loadable_manifest,
    _validated_domain,
)
from homeassistant.components.marketplace.utils.validate import (
    REPOSITORY_MANIFEST_VALUES,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntryState
from tests.e2e.fake_city import FakeCity, DEFAULT_TOKEN, route_to_fake_city


async def main() -> None:
    """Set up a line against the fake City and verify loading and unloading."""
    assert __version__ == "2026.11.0", __version__
    folder = Path("custom_components/ztm_warsaw")
    _check_loadable_manifest(folder, "ztm_warsaw")
    assert (
        _validated_domain(json.loads((folder / "manifest.json").read_text())["domain"])
        == "ztm_warsaw"
    )
    for key, value in json.loads(Path("hacs.json").read_text()).items():
        if key in REPOSITORY_MANIFEST_VALUES:
            REPOSITORY_MANIFEST_VALUES[key](value)
    with tempfile.TemporaryDirectory(prefix="ztm-native-11-") as config:
        shutil.copytree(
            "custom_components",
            Path(config) / "custom_components",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        hass = HomeAssistant(config)
        hass.config.skip_pip = True
        hass.config.skip_pip_packages = []
        loader.async_setup(hass)
        fake = FakeCity()
        await fake.start()
        try:
            with route_to_fake_city(fake):
                assert await bootstrap.async_from_config_dict(
                    {
                        "homeassistant": {
                            "latitude": 52.23,
                            "longitude": 21.01,
                            "elevation": 100,
                            "time_zone": "Europe/Warsaw",
                            "country": "PL",
                        }
                    },
                    hass,
                )
                flow = hass.config_entries.flow
                result = await flow.async_init("ztm_warsaw", context={"source": "user"})
                assert result["type"] == "form", result
                result = await flow.async_configure(
                    result["flow_id"], {"api_key": DEFAULT_TOKEN, "manual": True}
                )
                result = await flow.async_configure(
                    result["flow_id"],
                    {
                        "api_key": DEFAULT_TOKEN,
                        "busstop_id": 7009,
                        "busstop_nr": "01",
                        "line": "151",
                    },
                )
                await hass.async_block_till_done()
                assert result["type"] == "create_entry", result
                entry = result["result"]
                assert entry.state is ConfigEntryState.LOADED, entry.state
                state = hass.states.get("sensor.line_151_from_7009_01")
                assert state is not None
                assert state.state != "unavailable", state
                assert "Stop, ID" in state.attributes
                assert fake.count("timetable") >= 1
                assert await hass.config_entries.async_unload(entry.entry_id)
                await hass.async_block_till_done()
                assert entry.state is ConfigEntryState.NOT_LOADED
                assert not fake.blocked, fake.blocked
                print(
                    "Core 2026.11.0 native smoke passed: config flow, loaded entry, timetable sensor, unload; fake City only."
                )
        finally:
            await hass.async_stop(force=True)
            await fake.stop()


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=60))
