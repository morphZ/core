"""Config flow for pvcharge integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# REFRESH_INTERVAL = timedelta(seconds=5)
# MOVING_AVERAGE_WINDOW = 10
# CONF_GRID_BALANCE_ENTITY = "input_number.grid_return"
# CONF_CHARGE_ENTITY = "input_number.charge_power"
# CONF_CHARGE_MIN = 2.0
# CONF_CHARGE_MAX = 11.0
# CONF_PV_THRESHOLD = 0.5
# CONF_PV_HYSTERESIS = 10.0
# CONF_DEFAULT_MAX_TIME = timedelta(minutes=30)
# CONF_SOC_ENTITY = "input_number.soc"
# CONF_MIN_SOC = 30

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("grid_entity"): cv.string,
        vol.Required("charge_entity"): cv.string,
        vol.Required("charge_min"): cv.positive_float,
        vol.Required("charge_max"): cv.positive_float,
        # vol.Required("charge_threshold"): cv.positive_float,
        # vol.Required("charge_hysteresis"): cv.positive_float,
        # vol.Optional("boost_time", default=30): cv.positive_int,
        # vol.Optional("soc_entity"): cv.string,
        # vol.Optional("soc_min"): cv.positive_float,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    # Return info that you want to store in the config entry.
    return {"title": "PV charge controller"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for pvcharge."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
