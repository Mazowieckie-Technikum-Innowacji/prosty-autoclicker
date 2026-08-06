import time
from pynput.mouse import Button, Controller

mouse = Controller()

time.sleep(1)

mouse.click(Button.left, 1)

print("Clicked!")
