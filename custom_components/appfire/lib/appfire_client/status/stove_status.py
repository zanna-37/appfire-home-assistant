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
    def get_all_status_keys() -> list[str]:
        """Return a list of all known status keys for translations."""
        return [StoveStatus.status_to_key(status) for status in StoveStatus]

    @staticmethod
    def status_to_key(status: int) -> str:
        """Convert status code to translation key."""
        if status == StoveStatus.OFF:
            return "off"
        elif status == StoveStatus.CHECKING_BEFORE_START:
            return "checking_before_start"
        elif status == StoveStatus.CLEANING_BEFORE_START:
            return "cleaning_before_start"
        elif status == StoveStatus.PRELOAD:
            return "preloading"
        elif status == StoveStatus.WAITING_FIRE:
            return "waiting_fire"
        elif status == StoveStatus.START_BURNING:
            return "start_burning"
        elif status == StoveStatus.STABILIZATION:
            return "stabilization"
        elif status == StoveStatus.ON:
            return "on"
        elif status == StoveStatus.TURNING_OFF:
            return "turning_off"
        elif status == StoveStatus.COOLING_DOWN:
            return "cooling_down"
        elif status == StoveStatus.WARNING_LOW_PELLET:
            return "warning_low_pellet"
        elif status == StoveStatus.ERROR_END_PELLET:
            return "error_end_pellet"
        elif status == StoveStatus.ERROR_SCREW_JAMMED:
            return "error_screw_jammed"
        elif status == StoveStatus.CLEAN_BURNER:
            return "clean_burner"
        else:
            return f"unknown_{status}"
