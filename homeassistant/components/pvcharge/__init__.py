"""The pvcharge integration."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN
from .pvcharger import PVCharger

_LOGGER = logging.getLogger(__name__)

CONF_CHARGER_HOST = "charger_host"
CONF_DURATION = "boost_duration"
CONF_BALANCE_ENTITY = "balance_entity"
CONF_SOC_ENTITY = "soc_entity"
CONF_LOW_VALUE = "soc_low_value"
CONF_REFRESH = "pid_interval"
CONF_PV_REFRESH = "pv_interval"

DEFAULT_SETPOINT = 0.0
DEFAULT_MA_LENGTH = 1
DEFAULT_DURATION = 30

PVCHARGE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CHARGER_HOST): cv.string,
        vol.Required(CONF_DURATION, default=DEFAULT_DURATION): vol.Coerce(int),
        vol.Required(CONF_BALANCE_ENTITY): cv.entity_id,
        vol.Optional(CONF_SOC_ENTITY): cv.entity_id,
        vol.Optional(CONF_LOW_VALUE): vol.Coerce(float),
        vol.Optional(CONF_REFRESH): vol.Coerce(int),
        vol.Optional(CONF_PV_REFRESH): vol.Coerce(int),
    }
)

CONFIG_SCHEMA = vol.Schema({DOMAIN: PVCHARGE_SCHEMA}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up pvcharge from a config entry."""
    # pylint: disable=no-member
    _LOGGER.warning("Enter async_setup")

    params = [config[DOMAIN].get(k, None) for k in PVCHARGE_SCHEMA.schema.keys()]

    pvc = PVCharger(hass, *params)
    await pvc.run()  # type: ignore

    return True
