# Anime-Matrix

Pixel-perfect Anime Matrix GIFs created using Inkscape. These animations have been tested with both Windows and Linux (specifically, Kubuntu 20.04) on ROG Zephyrus G14 (2021). 

## On Windows

1) Import the GIF in the Anime Matrix section of Armoury Crate. You don't need the `.cfg` files.
2) Rotate until the little arrow on the right is completely out of the view.

## On Linux

1. Make sure you have `asusctl` installed. Refer to [https://asus-linux.org/](https://asus-linux.org/) for more details.
2. Move the GIF and the `.cfg` files to `/home/<username>/.config/rog/`. Update the path inside the `.cfg` file to include your username.
3. If you have `asusctl` installed correctly, you should now be able to trigger the anime matrix animation by running `asusd-user` from a terminal.

## Create your own

The template I used is included inside `Template/`. This is a modification of the template used by [Josh Walsh](https://blog.joshwalsh.me/asus-anime-matrix/). When opened inside InkScape, you will see two layers, namely `bg` and `Layer 1`. By default, `bg` is set to be transparent so that the grid drawn underneath is visible. Each of the squares in this grid correspond to exactly one of the LEDs on the back panel. So, as long as you draw using these squares, the final product will look 'clean' and sharp with no blurring. 

Make sure to turn the opacity of the `bg` layer to 100 when you are finished drawing. Now export to PNG using the exact export settings shown in the included screenshot. You can create your own GIFs frame by frame and then combining into a single GIF file using `ffmpeg` or a similar program. 

## Attribution

Please attribute/link back to this repo if you find this helpful. Have fun! :)
