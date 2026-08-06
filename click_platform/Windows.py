from pynput import mouse


class Click:
    def __init__(self):
        self.mouse_ctrl = mouse.Controller()

    def press(self):
        self.mouse_ctrl.press(mouse.Button.left)

    def release(self):
        self.mouse_ctrl.release(mouse.Button.left)

    def __call__(self):
        self.press()
        self.release()
