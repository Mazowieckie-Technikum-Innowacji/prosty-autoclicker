from evdev import UInput
from evdev import ecodes as e


class Click:
    def __init__(self):
        self.capabilities = {
            e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT, e.BTN_MIDDLE],
        }
        self.name = "autoclicker"

        self.bus_type = 0x03

        self.indev = UInput(self.capabilities, name=self.name, bustype=self.bus_type)

    def press(self):
        self.indev.write(e.EV_KEY, e.BTN_LEFT, 1)
        self.indev.syn()

    def release(self):
        self.indev.write(e.EV_KEY, e.BTN_LEFT, 0)
        self.indev.syn()

    def __call__(self):
        self.press()
        self.release()

    def __del__(self):
        if hasattr(self, "indev"):
            self.indev.close()
