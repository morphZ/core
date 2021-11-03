"""The pvcharge integration."""
from __future__ import annotations

# from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .pvcharger import PVCharger

# from homeassistant.helpers.event import async_call_later


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up pvcharge from a config entry."""
    # pylint: disable=no-member
    _LOGGER.warning("Enter async_setup_entry")

    hass.data.setdefault(DOMAIN, {})

    pvc = PVCharger(hass)
    await pvc.auto()  # type: ignore

    hass.data[DOMAIN][entry.entry_id] = pvc

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.warning("Enter async_unload_entry")

    pvc = hass.data[DOMAIN].pop(entry.entry_id)
    pvc.close()

    return True
