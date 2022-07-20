import numpy as np
from main import display_animation
from utils import scrolling_text_generator

img = np.zeros((56, 35), dtype=np.uint8)
start_x, start_y = img.shape[1], img.shape[0] // 2
gen = scrolling_text_generator(img, "Hello World!", start_x, start_y, step_x=-1, fontScale=1, thickness=1)

display_animation(gen, fps=14)
# The text "Hello World!" will now keep scrolling from one end to the other in a loop till you press Ctrl + C and stop it