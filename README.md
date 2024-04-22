# Fractal Mosaic Generator
## Description
The program recursively generates mosaics as you zoom in. First, the user is given a single image mosaic, they can then use the mouse wheel to zoom into the preferred region. Upon zooming in, the program will eventually replace images present on the screen with their composition, giving an illusion of infinite depth.

![Output Example](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeGY1b2t2MnI0bWI5NGxpNWVvZnU5OGw0d2Vid3U4MzJoYXR3cXY3aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/aGfvcX3JxD0wf7ox68/giphy-downsized-large.gif)

The program uses regular mosaics as bulding blocks, which can either be loaded or generated before the visuals are displayed. Written in Python, using Pillow and Tkinter.
## Usage
* You should put the images you want to use into the `images` directory
* To configure the program, you can change constants at the top of `main.py`
* For the first launch, set `LOAD_IMAGES` to `False`, it will force the program to compile images upon starting
* After the initial launch, you should set `LOAD_IMAGES` back to `True`
