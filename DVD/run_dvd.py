"""
Author: Suyog Jadhav 01-04-2024
Bouncing DVD logo animation for Anime Matrix using PyGame.
Modified from the original code by Tomeczekqq (https://github.com/Tomeczekqq/dvd-corner).
"""
from random import randint
import pygame
import os
import time
import numpy as np
import argparse

# Import the led handler
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from main import display_image, get_dbus_proxy, led_height, led_mask, led_width
from utils import get_border_indices


# The Bouncing Logo
# logo = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/DVD_logo_stretch.png')); scale_factor = (10, 15)
logo = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images/DVD_logo_pixel_perfect.png')); scale_factor = (14, 16)  # Pixel-perfect version
fps = 30  # Frames per second for the animation
SPEED = 2.5  # Speed of the logo

# LED mask stuff
proxy = get_dbus_proxy()  # The proxy to the dbus interface
possible_led_positions = np.argwhere(led_mask[:, :, 0])  # All possible positions for the logo to be in

# Get the left slanted border
left_border = get_border_indices(top=False, bottom=False, left=True, right=False)
left_border_xs = [idx[1] for idx in left_border]  # Only the x values.
left_border_ys = [idx[0] for idx in left_border]  # Only the y values. y values are from 1 to led_width.

m = (led_height - 2) / (led_width - 1)  # The slope of the curve, slight adjustment for a better fit
left_border_normal_vector = [1 / np.sqrt(1 + m**2), m / np.sqrt(1 + m**2)]  # The normal vector to the curve at origin
left_border_offset = 0  # How many pixels to ignore from the border

# os.putenv('SDL_VIDEODRIVER', 'dummy')  # Comment this out to see the gui window (for testing)
def main(ignore_boundary=False, fps=fps, SPEED=SPEED):
    pygame.display.init()
    exit = False

    # Settings
    # SIZE = width, height = 800, 600  # Resolution. (4:3)!
    SIZE = width, height = led_width, led_height
    speed_scale = 2* SPEED / 800
    BG_COLOR = (0, 0, 0)  # Background color in RGB
    fullscreen = False  # Fullscreen

    global logo
    logo = pygame.transform.scale(logo, scale_factor)
    clock = pygame.time.Clock()
    img_size = logo.get_rect().size

    screen = pygame.display.set_mode(SIZE)

    pygame.display.set_caption('DVD Corner')
    if fullscreen:
        DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)

    # Get a random starting position
    # x = randint(50, width-60)
    # y = randint(50, height-60)
    start = np.random.choice(possible_led_positions.shape[0], 1)[0]
    x, y = possible_led_positions[start][::-1]  # x and y are reversed in the led_mask
    x_speed = y_speed = speed_scale * width
    speed = np.linalg.norm([x_speed, y_speed])


    def move(x, y):
        screen.blit(logo, (x, y))

    # The main loop
    print(f"Starting the DVD logo animation at x={x}, y={y}. Ignore boundary: {ignore_boundary}. Speed: {speed}")
    while exit == False:
        screen.fill(BG_COLOR)  # Clear the screen
        
        # If we are at the top or the right border, simply reverse the y_speed/ x_speed
        if (x + img_size[0] >= width):  # If we are at the right border
            # print(f"Collision detected at right border.")  #DEBUG
            x_speed = -x_speed if x_speed > 0 else x_speed
        elif (y <= 0):  # If we are at the top border
            # print(f"Collision detected at top border.")  #DEBUG
            y_speed = -y_speed if y_speed < 0 else y_speed

        # Detect the left border collision
        elif (not ignore_boundary) and (int(y) in left_border_ys) and (x <= left_border_xs[left_border_ys.index(int(y))] - left_border_offset):
            # print(f"Collision detected at x={x}, y={y}")  # DEBUG
            # Get the movement vector
            movement_vector = [x_speed / speed, y_speed / speed]

            # Calculate the angle of incidence
            angle_incidence = np.arccos(np.dot(movement_vector, left_border_normal_vector))
            
            # New speeds
            x_speed = speed * np.cos(2 * angle_incidence)
            y_speed = speed * np.sin(2 * angle_incidence)

        # Edge cases
        elif (x <= 0):  # Handling the left most extreme
            # print(f"Collision detected at extreme left border.")  # DEBUG
            x_speed = -x_speed if x_speed < 0 else x_speed
        elif (y + img_size[1] >= height):  # Handling the bottom most extreme
            # print(f"Collision detected at extreme bottom border.")  # DEBUG
            y_speed = -y_speed if y_speed > 0 else y_speed

        
        x += x_speed
        y += y_speed
        move(x, y)
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

        # Show the current frame
        pygame_surface = pygame.surfarray.array3d(screen).swapaxes(0, 1)
        binary_image = pygame_surface[..., 0]  # We only need one channel
        display_image(binary_image, proxy)
        time.sleep(1/fps)

    pygame.quit()


def parse_args():
    parser = argparse.ArgumentParser(description="Bouncing DVD logo animation for Anime Matrix using PyGame.")
    parser.add_argument("--ignore_boundary", action="store_true", help="If set, the logo will not collide with the slanted boundary of the Anime Matrix display. Default: False.")
    parser.add_argument("--fps", type=int, default=fps, help="Frames per second for the animation. Default: 30.")
    parser.add_argument("--speed", type=int, default=SPEED, help="Speed of the logo (in pixels/frame). Default: 2.5.")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(
        ignore_boundary=args.ignore_boundary,
        fps=args.fps,
        SPEED=args.speed
    )