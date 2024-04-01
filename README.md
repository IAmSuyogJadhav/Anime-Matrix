# Anime-Matrix

Pixel-perfect Anime Matrix GIFs created using Inkscape. These animations have been tested with both Windows and Linux (specifically, Kubuntu 20.04) on ROG Zephyrus G14 (2021). 

## Usage
### For static animations:
The static animations are GIF files that can be directly used on the Anime Matrix display on both Linux and Windows.

<details>
<summary><b>On Windows</b></summary>

1) Import the GIF in the Anime Matrix section of Armoury Crate. You don't need the `.cfg` files.
2) Rotate until the little arrow on the right is completely out of the view.
</details>

<details>
<summary><b>On Linux</b></summary>

1. Make sure you have `asusctl` installed. Refer to [https://asus-linux.org/](https://asus-linux.org/) for more details.
2. Move the GIF and the `.cfg` files to `/home/<username>/.config/rog/`. Update the path inside the `.cfg` file to include your username.
3. If you have `asusctl` installed correctly, you should now be able to trigger the anime matrix animation by running `asusd-user` from a terminal.
</details>

<br />
Available static animations:

> **Dino**
The chrome dino game, with the dino jumping over cacti. Perfect loop.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Hg-VG-xjqqM/0.jpg)](https://www.youtube.com/watch?v=Hg-VG-xjqqM)


### For dynamic animations (e.g., DVD):
The dynamic animations are scripted using Python and can be run on the Anime Matrix display on Linux only. The following animations are available as of now:

> **DVD**
Plays the endless bouncing DVD logo animation.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/yZYN438pxEk/0.jpg)](https://www.youtube.com/watch?v=yZYN438pxEk)

1. Navigate to the `DVD` directory and run:
    ```bash
    pip install -r requirements.txt
    ```
    to install the required packages.

2. Make sure no animation is already running:
   ```bash
    pkill asusd-user
    ```
3. Then run:
    ```bash
    python run_dvd.py
    ```
    to start the animation. Alternatively, you can create an alias for the above command in your `.bashrc` or `.bash_aliases` file for easy access.

4. By default, the DVD logo will be bound between the middle slanted boundary and the top, right edges of the Anime Matrix display. This might look a bit clunky to some. If you would rather the logo collide with the vertical or horizontal edges only, you can call the above script with `--ignore_boundary` flag. Run `python run_dvd.py --help` for more options.

5. Sometimes, the DVD logo might get stuck in a corner. You will need to re-run the script to fix this.

## Create your own

The template I used for static animations is included inside `Template/`. This is a modification of the template used by [Josh Walsh](https://blog.joshwalsh.me/asus-anime-matrix/). When opened inside InkScape, you will see two layers, namely `bg` and `Layer 1`. By default, `bg` is set to be transparent so that the grid drawn underneath is visible. Each of the squares in this grid correspond to exactly one of the LEDs on the back panel. So, as long as you draw using these squares, the final product will look 'clean' and sharp with no blurring. 

Make sure to turn the opacity of the `bg` layer to 100 when you are finished drawing. Now export to PNG using the exact export settings shown in the included screenshot. You can create your own GIFs frame by frame and then combine into a single GIF file using `ffmpeg` or a similar program. 

## Attribution

Please attribute/link back to this repo if you find this helpful. Have fun! :)
