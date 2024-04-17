from PIL import Image, ImageTk
from math import inf, floor


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


class InfiniteCanvas:
    def __init__(self, width=1920, height=1080, min_detailed_size=40):
        self.width = width
        self.height = height
        self.min_detailed_size = min_detailed_size
        self.canvas = Image.new('RGB', (width, height))

        self.resized_images = {}  # <image_name, resized_image>

        self.cam_zoom = 1
        self.prev_cam_zoom = 1  # crutch
        self.cam_x = width // 2
        self.cam_y = height // 2
        self.cam_min_x = 0
        self.cam_max_x = 0
        self.cam_min_y = 0
        self.cam_max_y = 0

        self.update_cam_bounds()

    def update_cam_bounds(self):
        self.cam_min_x = self.cam_x - self.width / 2
        self.cam_max_x = self.cam_x + self.width / 2
        self.cam_min_y = self.cam_y - self.height / 2
        self.cam_max_y = self.cam_y + self.height / 2

    def set_cam_zoom(self, zoom):
        self.prev_cam_zoom = self.cam_zoom
        # self.cam_x *= zoom / self.cam_zoom
        # self.cam_y *= zoom / self.cam_zoom
        self.cam_zoom = zoom if zoom > 0 else 1 / inf

    def set_cam_pos(self, cam_x, cam_y):
        self.cam_x += ((self.cam_x + cam_x - self.width / 2) * (self.cam_zoom / self.prev_cam_zoom) - (
                    self.cam_x + cam_x - self.width / 2))
        self.cam_y += ((self.cam_y + cam_y - self.height / 2) * (self.cam_zoom / self.prev_cam_zoom) - (
                    self.cam_y + cam_y - self.height / 2))
        self.update_cam_bounds()

    def to_canvas(self, value):
        return value * self.cam_zoom

    def to_camera(self, value):
        return value / self.cam_zoom

    def should_be_detailed(self, width, height):
        return width > self.min_detailed_size or height > self.min_detailed_size

    def draw_image(self, image, x, y, width, height):
        if self.should_be_detailed(width, height):
            len_x = len(image.composition)
            len_y = len(image.composition[0])
            min_x_index = clamp(floor((self.cam_min_x - x) * len_x / width), 0, len_x - 1)
            min_y_index = clamp(floor((self.cam_min_y - y) * len_y / height), 0, len_y - 1)
            max_x_index = clamp(floor((self.cam_max_x - x) * len_x / width), 0, len_x - 1)
            max_y_index = clamp(floor((self.cam_max_y - y) * len_y / height), 0, len_y - 1)

            for i in range(min_x_index, max_x_index + 1):
                for j in range(min_y_index, max_y_index + 1):
                    self.draw_image(image.composition[i][j],
                                    x + width * i / len_x, y + height * j / len_y,
                                    width / len_x, height / len_y)

        else:
            if image.name not in self.resized_images.keys():
                self.resized_images[image.name] = image.final_pixels.resize(
                    (round(width), round(height)), 4)  # 4 HERE MEANS THE ALGO FOR RESIZING, 4 LOOKS GOOD WORKS FAST

            self.canvas.paste(self.resized_images[image.name],
                              (round(x - self.cam_min_x), round(y - self.cam_min_y)),
                              )

    def show(self, image):
        self.generate_image(image)
        self.canvas.show()

    def generate_image(self, image):
        self.draw_image(image, 0, 0, self.to_canvas(image.width), self.to_canvas(image.height))
        self.resized_images = {}

    def stretch_image(self, x, y):
        self.canvas = self.canvas.resize((x, y))

    def change_width_height(self, w, h):
        self.width = w
        self.height = h

    def get_tkinter_image(self):
        return ImageTk.PhotoImage(self.canvas)

    def animate(self, image, frames, zoom_step):
        for i in range(frames):
            self.draw_image(image, 0, 0, self.to_canvas(image.width), self.to_canvas(image.height))
            self.canvas.save(r"animation\{}.jpg".format(i))
            self.set_cam_zoom(self.cam_zoom * zoom_step)
            print("{} done".format(i))

# def drag(self, cam_x, cam_y):
#     self.cam_x += (cam_x - 1600/2) * 0.05
#     self.cam_y += (cam_y - 900/2) * 0.05
#     self.update_cam_bounds()
