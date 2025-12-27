from enum import IntEnum


class StoveStatus(IntEnum):
    OFF = 0
    CHECKING_BEFORE_START = 1
    CLEANING_BEFORE_START = 2
    PRELOAD = 3
    WAITING_FIRE = 4 # Called "Attende"
    START_BURNING = 5 # Called "Accende"
    STABILIZATION = 7
    ON = 8
    TURNING_OFF = 9 # Called "Pulizia spegnimento"
    COOLING_DOWN = 10

    WARNING_LOW_PELLET = 14
    ERROR_END_PELLET = 15
    ERROR_SCREW_JAMMED = 65
    CLEAN_BURNER = 70 # Called "Pul. bruc."

    @staticmethod
    def getAllStatusTexts() -> list[str]:
        """Return a list of all known status text values."""
        return [StoveStatus.statusToText(status) for status in StoveStatus]

    @staticmethod
    def statusToText(status: int) -> str:
        if status == StoveStatus.OFF:
            return "Off"
        elif status == StoveStatus.CHECKING_BEFORE_START:
            return "Checking before start"
        elif status == StoveStatus.CLEANING_BEFORE_START:
            return "Cleaning before start"
        elif status == StoveStatus.PRELOAD:
            return "Preloading"
        elif status == StoveStatus.WAITING_FIRE:
            return "Waiting fire"
        elif status == StoveStatus.START_BURNING:
            return "Start burning"
        elif status == StoveStatus.STABILIZATION:
            return "Stabilization"
        elif status == StoveStatus.ON:
            return "On"
        elif status == StoveStatus.TURNING_OFF:
            return "Turning off"
        elif status == StoveStatus.COOLING_DOWN:
            return "Cooling down"
        elif status == StoveStatus.WARNING_LOW_PELLET:
            return "Warning: Low pellet"
        elif status == StoveStatus.ERROR_END_PELLET:
            return "Error: End pellet"
        elif status == StoveStatus.ERROR_SCREW_JAMMED:
            return "Error: Screw jammed"
        elif status == StoveStatus.CLEAN_BURNER:
            return "Clean burner"
        else:
            return "Unknown status " + str(status)
