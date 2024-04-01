import numpy as np
import cv2
import os

# def scrolling_text_generator(img, text, start_x, start_y, step_x, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, thickness=1, color=255):
#     """Generates a scrolling text on the given image. Currently, only horizontal direction scrolling is supported.
#     Args:
#         img (np.ndarray): The image to be written to.
#         text (str): The text to be written.
#         start_x (int): The x coordinate of the bottom left corner of the text.
#         start_y (int): The y coordinate of the bottom left corner of the text.
#         step_x (int): The number of pixels to move the text each frame (x direction).
#         fontFace (int): The font face to use.
#         fontScale (float): The font scale to use.
#         thickness (int): The thickness of the text.
#         color (int): The color of the text (0-255).
#     """
#     # Calculate last index based on the information provided
#     end_x = (abs(step_x) / step_x) * cv2.getTextSize(text, fontFace, fontScale, thickness)[0][0]
#     xs = np.arange(start_x, end_x, step_x, dtype=np.int)

#     while True:
#         try:
#             for x in xs:
#                 # print(x, type(x), start_y, type(start_y)) # DEBUG
#                 img1 = cv2.putText(img.copy(), text, (x, start_y), fontFace, fontScale, color, thickness)
#                 yield(img1)
#         except KeyboardInterrupt:
#             break

def get_border_indices(top=True, bottom=True, left=True, right=True):
    border_indices = []
    leds_mask = np.load(os.path.join(os.path.dirname(__file__), "led_mask_GA401.npy"))[..., 0]
    if top:
        border_indices.extend([(0, j) for j in range(leds_mask.shape[1]) if leds_mask[0, j]])  # Add top border
    
    # Add the left and right border indices
    for i in range(1, leds_mask.shape[0] - 2):
        for j in range(leds_mask.shape[1]):
            if leds_mask[i, j]:
                if left:
                    border_indices.append((i, j))
                if right:
                    border_indices.append((i, leds_mask.shape[1]-1))
                break
    
    # Add bottom border
    if bottom:
        border_indices.extend([(leds_mask.shape[0]-2, j) for j in range(leds_mask.shape[1]) if leds_mask[-2, j]])

    return border_indices


def scrolling_text_generator(img, text, start_x, start_y, step_x, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, thickness=1, color=255, unshrink_factor=1):
    """Generates a scrolling text on the given image.
    Args:
        img (np.ndarray): The image to be written to.
        text (str): The text to be written.
        start_x (int): The x coordinate of the bottom left corner of the text.
        start_y (int): The y coordinate of the bottom left corner of the text.
        step_x (int): The number of pixels to move the text each frame (x direction).
        fontFace (int): The font face to use.
        fontScale (float): The font scale to use.
        thickness (int): The thickness of the text.
        color (int): The color of the text (0-255).
        unshrink_factor (int): The factor by which the text will be shrunk each frame. This is required because the text appears elongated when it is displayed otherwise.
            An unshrink factor of 1 will display the text as it is, while a factor of 2 will display the text half its size (only along the x) and so on. Very hacky solution
            but can sometimes work. Very rarely works for >2. Default is 1.

    Yields:
        np.ndarray: The image with the text written to it. The frames are yielded infinitely. 
    """

    # Expand the image before putting the text on by interleaving zeros with the image...
    # ...and later removing this zero padding to effectively shrink the image and the text back to the original size
    assert unshrink_factor >= 1
    expanded_img = np.zeros((img.shape[0], img.shape[1] * unshrink_factor), dtype=np.uint8)
    padding = np.zeros_like(img)
    # Add the padding
    for i in range(1, unshrink_factor):
        expanded_img[:, i::unshrink_factor] = padding
    # Add the image
    expanded_img[:, ::unshrink_factor] = img
    img = expanded_img

    # Adjust start_x and start_y to account for the padding
    start_x *= unshrink_factor

    # Calculate last index based on the information provided
    end_x = (abs(step_x) / step_x) * cv2.getTextSize(text, fontFace, fontScale, thickness)[0][0]
    xs = np.arange(start_x, end_x, step_x, dtype=int)

    # Yield the animation frame by frame (effectively outputs an infinite number of looping frames)
    while True:
        try:
            for x in xs:
                img1 = cv2.putText(img.copy(), "Hello World!", (x, start_y), fontFace, fontScale, color, thickness)
                yield(img1[:, ::unshrink_factor])
        except KeyboardInterrupt:
            break