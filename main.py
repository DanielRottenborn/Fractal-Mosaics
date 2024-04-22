from scripts import image_cls, canvas_cls, map_image, gui
from math import ceil
import ctypes
import os
import pickle
import time

ctypes.windll.user32.SetProcessDPIAware()

txt_path = os.path.abspath("") + "\\" + "images.txt"
path = os.path.abspath("images")  # path to the directory with images
compiled_path = path + '\\' + 'compiled'
pickle_path = path + '\\' + 'pickled'

SECOND_ROUND = False  # compile images with two layers of depth
path_second = path + '\\' + 'compiled2'

USE_PICKLE = True
LOAD_IMAGES = False  # <--- You should set this to False for images to compile
MAKE_IF_DOESNT_EXIST = True
NUMBER_OF_PARTS = 128  # how many image parts should the program use to build an image (both rows and columns)
RES_X_WINDOW = 1920
RES_Y_WINDOW = 1080
RES_X_IMAGE = 1920
RES_Y_IMAGE = 1080

RES_X_WINDOW = ceil(RES_X_WINDOW / NUMBER_OF_PARTS) * NUMBER_OF_PARTS
RES_Y_WINDOW = ceil(RES_Y_WINDOW / NUMBER_OF_PARTS) * NUMBER_OF_PARTS
RES_X_IMAGE = ceil(RES_X_IMAGE / NUMBER_OF_PARTS) * NUMBER_OF_PARTS
RES_Y_IMAGE = ceil(RES_Y_IMAGE / NUMBER_OF_PARTS) * NUMBER_OF_PARTS


def load_images(load_original):
    for image in os.listdir(path):
        if not (os.path.isdir(path + '\\' + image) or image.split('.')[-1] == 'txt'):  # mb modify this later
            lst.append(image_cls.ImageWithComp(os.path.abspath(path + '\\' + image), load_original, RES_X_IMAGE, RES_Y_IMAGE))
            print(f"image {len(lst)} loaded")


def update_lst_with_pickle():
    lst = []

    for txt in os.listdir(pickle_path):
        with open(pickle_path + "\\" + txt, "rb") as file:
            lst.append(pickle.load(file))
            if not LOAD_IMAGES:
                lst[-1].reset_images(path)
            else:
                lst[-1].read_compiled_image(compiled_path, make_if_dn_exist=MAKE_IF_DOESNT_EXIST, save_if_dn_exist=True)
            print(len(lst), "done loading from pickle")

    for image in lst:
        image.after_pickle(lst)

    return lst


if not os.path.isdir(compiled_path):
    os.mkdir(compiled_path)

if not os.path.isdir(path_second):
    os.mkdir(path_second)

if not os.path.isdir(pickle_path):
    os.mkdir(pickle_path)

lst = []

# CAN COMMENT EVERYTHING UNDER AFTER SAVED
if not LOAD_IMAGES:
    load_images(True)

    print("composing started")
    for i in range(len(lst)):
        lst[i].composition = map_image.map_image_test(lst[i], lst[:i] + lst[i+1:], parts=NUMBER_OF_PARTS)
        # lst[i].write_to_file(txt_path)
        print(f"image {i} done")
    print("composition done")

    if not USE_PICKLE:
        image_cls.clear_file(txt_path)
        for image in lst:
            image.write_to_file(txt_path)
    else:
        for image in lst:
            image.write_to_file_pickle(pickle_path)

        lst = update_lst_with_pickle()

    print("saving done")

    t = time.time()
    for image in lst:
        t1 = time.time()

        lookup = {}
        image.make_pixels(lookup)
        image.save_compiled_image(compiled_path)

        print("first round done and saved", time.time() - t1)

    if SECOND_ROUND:
        t1 = time.time()

        for image in lst:
            t1 = time.time()

            lookup = {}
            image.make_pixels_from_final(lookup)
            image.save_compiled_image(path_second)

        print("second round done and saved", time.time() - t1)

    print("making compiled images done and save", time.time() - t)
else:
    if not USE_PICKLE:
        load_images(False)
        # LOAD VERSION
        t = time.time()
        for image in lst:
            t1 = time.time()
            image.read_from_file(txt_path, lst)
            image.read_compiled_image(compiled_path, make_if_dn_exist=MAKE_IF_DOESNT_EXIST, save_if_dn_exist=True)
            print("one more done", time.time() - t1)
        print("loading images done")
        print(time.time() - t)
    else:
        t = time.time()
        lst = update_lst_with_pickle()
        print(time.time() - t)

infiniteCanvas = canvas_cls.InfiniteCanvas(RES_X_WINDOW, RES_Y_WINDOW, min_detailed_size=3000)

a = gui.GuiCanvas(infiniteCanvas, lst[4], RES_X_WINDOW, RES_Y_WINDOW)
a.main_loop()

""" RESIZING PARAMETERS
sample 0
0.002990245819091797
sample 1
0.010106086730957031
sample 2
0.00397181510925293
sample 3
0.007009744644165039
sample 4
0.0029554367065429688
sample 5
0.004953861236572266
"""