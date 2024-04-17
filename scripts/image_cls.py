from PIL import Image
import os
import pickle


class ImageWithComp:
    def __init__(self, image_path, load_original=True, width=1920, height=1080):
        self.name = image_path.split('\\')[-1]
        self.width = width
        self.height = height
        if load_original:
            self.image = Image.open(image_path).convert('RGB').resize((width, height))
        else:
            self.image = None
        self.final_pixels = Image.new("RGB", (width, height), (0, 0, 0))

        self.resized_small = None
        # self.final_pixels = self.image.copy()
        # self.picture_to_show = self.image
        self.all_images = {}  # dict of all images {name: image_class}

        self.composition = []
        self.done_to_depth = 0

        self.shortColor = -1  # -1 if it doesn't exist, maybe should be changed to something else in the future

    def reset_images(self, path):
        self.image = Image.open(path + "\\" + self.name).convert('RGB').resize((self.width, self.height))
        self.final_pixels = Image.new("RGB", (self.width, self.height), (0, 0, 0))

    def make_pixels(self, lookup):
        resx = self.width // (len(self.composition))
        resy = self.height // (len(self.composition))
        for x in range(len(self.composition)):
            for y in range(len(self.composition[x])):
                if self.composition[x][y].name not in lookup.keys():
                    lookup[self.composition[x][y].name] = self.composition[x][y].image.resize((resx, resy))
                self.final_pixels.paste(lookup[self.composition[x][y].name], (x*resx, y*resy))

    def make_pixels_from_final(self, lookup):
        resx = self.width // (len(self.composition))
        resy = self.height // (len(self.composition))
        for x in range(len(self.composition)):
            for y in range(len(self.composition[x])):
                if self.composition[x][y].name not in lookup.keys():
                    lookup[self.composition[x][y].name] = self.composition[x][y].final_pixels.resize((resx, resy))
                self.final_pixels.paste(lookup[self.composition[x][y].name], (x * resx, y * resy))

    def update_original_image(self):
        # make original image divided image
        self.image = self.final_pixels.copy()

    # def update_to_show(self):
    #     self.picture_to_show = self.final_pixels

    def write_to_file(self, path_to_txt):
        with open(path_to_txt, 'a') as file:
            file.write(self.name + '\n')
            for row in self.composition:
                for image in row:
                    file.write(image.name + '?')
                file.write('\n')
            file.write('\n')

    def read_from_file(self, path_to_txt, all_images):
        self.composition = []
        dict = {image.name: image for image in all_images}
        with open(path_to_txt, 'r') as file:
            lines = file.readlines()
            start = lines.index(self.name + '\n')
            lines = lines[start + 1:]
            end = lines.index('\n')
            lines = lines[:end]
            for line in lines:
                line = line.split("?")[:-1]
                self.composition.append([dict[name.strip()] for name in line])

    def save_compiled_image(self, path):
        name = ''.join(self.name.split('.')[:-1]) + "_compiled"
        ext = '.' + self.name.split('.')[-1]
        self.final_pixels.save(path + "\\" + name + ext)

    def read_compiled_image(self, path, make_if_dn_exist=True, save_if_dn_exist=True):
        name = ''.join(self.name.split('.')[:-1]) + "_compiled"
        ext = '.' + self.name.split('.')[-1]
        path_with_name = path + "\\" + name + ext
        if os.path.exists(path_with_name):
            self.final_pixels = Image.open(path_with_name).convert('RGB').resize((self.width, self.height))
        elif make_if_dn_exist:
            self.make_pixels()
            if save_if_dn_exist:
                self.save_compiled_image(path)

    ''' Stores average color of this image, if its not created, creates it
        This function can be improved to pass in user functions, but not now
    '''
    def get_short_color(self, func):
        if self.shortColor == -1:
            self.shortColor = func(self.image)
        return self.shortColor

    def write_to_file_pickle(self, path_to_txt):
        path_to_txt += "\\" + self.name.strip('.')[:-1]
        self.image = None
        self.final_pixels = None
        self.resized_small = {}
        self.all_images = {}

        for row in self.composition:
            for i in range(len(row)):
                row[i] = row[i].name

        with open(path_to_txt, 'wb') as file:
            pickle.dump(self, file)

    def after_pickle(self, all_images):
        dict = {image.name: image for image in all_images}
        for row in self.composition:
            for i in range(len(row)):
                row[i] = dict[row[i]]


def clear_file(txt_path):
    with open(txt_path, 'w') as file:
        file.write('')
