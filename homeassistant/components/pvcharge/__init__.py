"""The pvcharge integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_call_later

from .const import DOMAIN
from .pvcharge import PVCharger

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up pvcharge from a config entry."""
    # pylint: disable=no-member
    _LOGGER.warning("Enter async_setup_entry")

    hass.data.setdefault(DOMAIN, {})

    pvc = PVCharger(hass)
    pvc.start()  # type: ignore

    hass.data[DOMAIN][entry.entry_id] = pvc

    @callback
    async def async_halt(event_time) -> None:
        pvc.to_idle()  # type: ignore

    async_call_later(hass, 15, async_halt)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.warning("Enter async_unload_entry")

    return True
