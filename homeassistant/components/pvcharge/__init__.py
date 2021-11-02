"""The pvcharge integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN
from .pvcharge import PVCharger

_LOGGER = logging.getLogger(__name__)

REFRESH_INTERVAL = timedelta(seconds=5)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up pvcharge from a config entry."""
    # pylint: disable=no-member
    _LOGGER.warning("Enter async_setup_entry")

    hass.data.setdefault(DOMAIN, {})

    def make_data():
        return {
            "sun": hass.states.get("sun.sun").state,
            "updater": hass.states.get("binary_sensor.updater").state,
        }

    pvc = PVCharger()
    pvc.start(make_data())  # type: ignore

    async def async_refresh(event_time):
        """Update controller state and parameters."""
        _LOGGER.debug("Run pvc.touch()")
        pvc.touch(make_data())

    pvc.timer = async_track_time_interval(  # type: ignore
        hass,
        async_refresh,
        REFRESH_INTERVAL,
    )

    hass.data[DOMAIN][entry.entry_id] = pvc

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.warning("Enter async_unload_entry")

    return True
