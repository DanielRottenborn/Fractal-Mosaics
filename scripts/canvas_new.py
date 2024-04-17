from PIL import Image
from math import log


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


class InfiniteCanvas:
    def __init__(self, root_image, output_width=1920, output_height=1080, max_re_render_object_count=4):
        self.output_width = output_width
        self.output_height = output_height

        self.root_image = root_image
        # self.partition_count = len(root_image.composition)  # add property for partition count in image class
        self.partition_count = 4

        self.canvas_width = self.root_image.width
        self.canvas_height = self.root_image.height

        self.cam_zoom = 1
        self.max_re_render_object_count = max_re_render_object_count
        # self.global_zoom =
        # self.local_zoom =
        self.recursion_depth = max(0, int(log(self.cam_zoom * max_re_render_object_count, self.partition_count)))

        print(self.recursion_depth)


InfiniteCanvas(Image.new('RGB', (1920, 1080)))
