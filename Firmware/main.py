import board
import adafruit_neopixel
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.keys import KC

keyboard = KMKKeyboard()

# Matrix pin configuration
keyboard.row_pins = (board.GP0, board.GP1, board.GP2, board.GP3)
keyboard.col_pins = (board.GP4, board.GP5, board.GP6, board.GP7)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Keymap (4x4)
keyboard.keymap = [
    [
        KC.A, KC.B, KC.C, KC.D,
        KC.E, KC.F, KC.G, KC.H,
        KC.I, KC.J, KC.K, KC.L,
        KC.M, KC.N, KC.O, KC.P,
    ]
]

# SK6812 LEDs on GP10
NUM_PIXELS = 16
pixels = adafruit_neopixel.NeoPixel(board.GP10, NUM_PIXELS, brightness=0.3, auto_write=True)
pixels.fill((0, 0, 0))

# One color per key
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (0, 255, 255), (255, 0, 255), (255, 128, 0), (128, 0, 255),
    (0, 128, 255), (0, 255, 128), (128, 255, 0), (255, 0, 128),
    (200, 200, 255), (150, 255, 150), (255, 180, 120), (255, 255, 255),
]

pressed_keys = [False] * NUM_PIXELS

# LED update hook
def handle_leds(kb):
    for i in kb.keys_pressed:
        if not pressed_keys[i]:
            pixels[i] = colors[i]
            pressed_keys[i] = True

    for i in range(NUM_PIXELS):
        if i not in kb.keys_pressed and pressed_keys[i]:
            pixels[i] = (0, 0, 0)
            pressed_keys[i] = False

keyboard.before_matrix_scan_callbacks.append(handle_leds)

keyboard.go()
