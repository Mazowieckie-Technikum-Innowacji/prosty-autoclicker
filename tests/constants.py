import platform as _platform

CURRENT_OS = _platform.system().lower()

TRUE_INPUTS = ["true", "t", "y", "yes", "1", "on", "", " "]
TRUE_INPUT = "t"
FALSE_INPUTS = ["false", "no", "n", "0", "off"]

SUPPORTED_OS_LIST = ["windows", "win32", "windows nt", "linux", "linuxbsd"]

ERROR_IMPOSSIBLE_FLUCTUATION = "Brak możliwości losowania przy tych wartościach!"

EV_KEY = "EV_KEY"
BTN_LEFT = "BTN_LEFT"
BTN_RIGHT = "BTN_RIGHT"
BTN_MIDDLE = "BTN_MIDDLE"
