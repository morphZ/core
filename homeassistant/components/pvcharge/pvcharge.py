"""Logic and code to run pvcharge."""
import logging

from simple_pid import PID
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
        """Set up PVCharger instance."""
        self.machine = Machine(
            model=self,
            states=PVCharger.states,
            transitions=PVCharger.transitions,
            initial="off",
        )

        self.pid = PID(
            -1.0, -0.1, 0.0, setpoint=0.0, sample_time=6, output_limits=(2.0, 11.0)
        )
        self.pid.sample_time = 6
        self.output = 0.0

    def on_enter_pv(self, data):
        """Run control loop for pv controlled charging."""
        _LOGGER.info("See data=%s", data)

        self.output = self.pid(float(data["excess"]))
