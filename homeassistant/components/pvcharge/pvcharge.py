"""Logic and code to run pvcharge."""
import logging

from transitions import Machine

_LOGGER = logging.getLogger()


class PVCharger:
    """Finite state machine to control the PV charging."""

    states = ["off", "pv", "boost", "calendar"]
    transitions = [
        ["start", "off", "pv"],
        ["battery_low", "*", "boost"],
        ["battery_ok", "boost", "pv"],
        ["calendar_event", ["off", "pv"], "calendar"],
        ["touch", ["pv", "calendar"], "="],
        ["off", "*", "off"],
    ]

    def __init__(self) -> None:
        """Do setup PVCharger instance."""
        self.machine = Machine(
            model=self,
            states=PVCharger.states,
            transitions=PVCharger.transitions,
            initial="off",
        )

    def on_enter_pv(self, data):
        """Run control loop for pv controlled charging."""
        _LOGGER.info("See data=%s", data)
