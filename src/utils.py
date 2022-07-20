import numpy as np
import cv2

def scrolling_text_generator(img, text, start_x, start_y, step_x, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, thickness=1, color=255):
    """Generates a scrolling text on the given image. Currently, only horizontal direction scrolling is supported.
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
    """
    # Calculate last index based on the information provided
    end_x = (abs(step_x) / step_x) * cv2.getTextSize(text, fontFace, fontScale, thickness)[0][0]
    xs = np.arange(start_x, end_x, step_x)

    while True:
        try:
            for x in xs:
                img1 = cv2.putText(img.copy(), text, (x, start_y), fontFace, fontScale, color, thickness)
                yield(img1)
        except KeyboardInterrupt:
            break