"""The pvcharge integration."""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .pvcharger import PVCharger

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up pvcharge from a config entry."""
    # pylint: disable=no-member
    _LOGGER.warning("Enter async_setup")

    hass.data.setdefault(DOMAIN, {})

    pvc = PVCharger(hass, config)
    await pvc.auto()  # type: ignore

    return True
