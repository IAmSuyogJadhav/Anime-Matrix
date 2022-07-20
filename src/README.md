# Anime Matrix display controller (only works for GA401 models currently)

Given here is a small low-level library using which you can control each of the individual 1215 LEDs on the AniMe Matrix display. The intended purpose of this script is to allow for developing dynamically changing Anime Matrix displays. The pixel-to-LED mapping has been figured out by trial and error (and with help from [asusctl](https://gitlab.com/asus-linux/asusctl/-/blob/main/rog-anime/src/image.rs)). Further details of the trial and error can be found in [`trial_and_error_pixel_map.ipynb`](trial_and_error_pixel_map.ipynb).

This is how you can display an image can be displayed on the Anime Matrix display, follow these steps (linux, must have `asusctl` installed):

1. Make sure the requirements are installed in the current environment.
```bash
pip install -r requirements.txt
```
2. Make sure the image you are about to display is the correct size (`56*35` as of writing this, check with the code if its not correct).
3. The part of the image that will actually be displayed is much smaller. To check the visible area and make adjustments as needed, checkout the LED locations in `led_mask_GA401.npy`.
```python
import numpy as np
import matplotlib.pyplot as plt

led_mask = np.load('led_mask_GA401.npy')
plt.title('Visible LEDs'); plt.imshow(led_mask[..., 0]); plt.show()
```

4. Use `display_image` to display your image. If you have an animation consisting of a sequence of images, use `display_animation` instead. It will loop the animation in a forever loop.
```python
from main import display_image, display_animation
import numpy as np

# A static image
my_img = np.zeros((56, 35), dtype=np.uint8)
display_image(my_img)

# Animation
frames = 100
my_animation = np.zeros((frames, 56, 35), dtype=np.uint8)
display_animation(my_animation, fps=30)  # 30 frames per second
```

# A sample dynamic Anime Matrix animation
Currently working on a scrolling text display. It is a very basic implementation currently, with only horizontal scrolling support and the font looks a bit stretched out on the display. Will need to find appropriate fonts that work well in the future. Anyway, here's the current version of the demo:

```python
import numpy as np
from main import display_animation
from utils import scrolling_text_generator

img = np.zeros((56, 35), dtype=np.uint8)
start_x, start_y = img.shape[1], img.shape[0] // 2
gen = scrolling_text_generator(img, "Hello World!", start_x, start_y, step_x=-1, fontScale=1, thickness=1)

display_animation(gen, fps=14)
# The text "Hello World!" will now keep scrolling from one end to the other in a loop till you press Ctrl + C and stop it
```

# Future Work

- Develop a dynamic AniMe Matrix animation (such as a clock, or scrolling text etc.)
- Currently, I have only developed this for the GA401 (G14 2021) model, as that's the one I have with me. The functions defined in the library can in theory work with both the models, if the correct pixel mapping is available. If you have the newer model, and are willing to give it a try, you can checkout [`trial_and_error_pixel_map.ipynb`](trial_and_error_pixel_map.ipynb) for details on how to figure out the pixel mapping by yourself. Feel free to raise an issue if you need further assistance!