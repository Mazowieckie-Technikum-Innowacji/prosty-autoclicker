from pynput.mouse import Button, Controller

mouse = Controller()

mouse.click(Button.left, 1)

print("Clicked!")
