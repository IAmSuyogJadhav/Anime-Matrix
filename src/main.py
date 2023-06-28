from dasbus.client.proxy import ObjectProxy
from dasbus.connection import SystemMessageBus
import numpy as np
import time

led_mask = np.load('led_mask_GA401.npy')
led_height = led_mask.shape[0]
led_width = led_mask.shape[1]


def get_dbus_proxy() -> ObjectProxy:
    """Returns a proxy to the Anime Matrix control interface defined by asusctl.

    Returns:
        ObjectProxy: The interface proxy. Any method calls on this proxy will be 
            sent to the corresponding method on the interface.
    """
    bus = SystemMessageBus()

    proxy = bus.get_proxy(
        "org.asuslinux.Daemon",
        "/org/asuslinux/Anime"
    )

    return proxy


def get_blank_image(rgb=False) -> np.ndarray:
    """Returns a blank image in the correct shape.

    Args:
        rgb (bool): If True, the image will be of shape (56, 35, 3). If False, the image will be of shape (56, 35).

    Returns:
        np.ndarray: A blank image.
    """
    if rgb:
        return np.zeros((led_height, led_width, 3), dtype=np.uint8)
    else:
        return np.zeros((led_height, led_width), dtype=np.uint8)


def image_to_anime(img: np.ndarray) -> list:
    """Converts a NumPy array (containing the pixel art) to a ByteArray as needed by the Anime Matrix.

    Args:
        img (np.ndarray): The image to be converted. Must have the shape (56, 35). Must be of Dtype uint8.

    Returns:
        list: The ByteArray to be sent to the Anime Matrix.
    """
    # The last channel has the locations of all the LEDs we will need
    mask_all_leds = led_mask[..., -1]

    # Make sure the image is in the right format and shape
    assert img.dtype == np.uint8
    assert img.shape == mask_all_leds.shape

    # Convert to anime-matrix bytes format
    anime_bytes = []
    for i in range(mask_all_leds.shape[0]):
        img_row, mask_row = img[i], mask_all_leds[i]

        # For each row, keep only the pixels that correspond to an LED
        anime_bytes.extend([img_pixel for img_pixel, mask_pixel in zip(img_row, mask_row) if mask_pixel])

    return anime_bytes  # The length should be == 1254


def write_to_display(proxy: ObjectProxy, anime_bytes: list):
    """Writes the given anime_bytes to the Anime Matrix.

    Args:
        proxy (ObjectProxy): The proxy to the Anime Matrix interface.
        anime_bytes (list): The ByteArray to be sent to the Anime Matrix.   
    """
    # Write to the display
    # proxy.Write(anime_bytes)
    proxy.Write((anime_bytes, 0))  # New format


def display_image(img: np.ndarray, proxy: ObjectProxy = None):
    """Displays the given image on the Anime Matrix.

    Args:
        img (np.ndarray): The image to be displayed. Must have the shape (56, 35). Must be of Dtype uint8.
        proxy (ObjectProxy): The proxy to the Anime Matrix interface. If None, a new one will be created.
    """
    if proxy is None:
        proxy = get_dbus_proxy()
    anime_bytes = image_to_anime(img)
    write_to_display(proxy, anime_bytes)


def display_animation(animation: np.ndarray, fps: int, proxy: ObjectProxy = None):
    """Displays the given animation on the Anime Matrix in an infinite loop. Stop the loop by pressing Ctrl+C.

    Args:
        animation (np.ndarray): The animation to be displayed. Must have the shape (frames, 56, 35). Must be of Dtype uint8.
        fps (int): The frames per second of the animation.
        proxy (ObjectProxy): The proxy to the Anime Matrix interface. If None, a new one will be created.
    """
    if proxy is None:
        proxy = get_dbus_proxy()

    # Main animation loop
    # while True:
    try:
        for frame in animation:
            anime_bytes = image_to_anime(frame)
            write_to_display(proxy, anime_bytes)
            time.sleep(1 / fps)
    except KeyboardInterrupt:
        write_to_display(proxy, [0] * 1254)  # Clear the display
        return
