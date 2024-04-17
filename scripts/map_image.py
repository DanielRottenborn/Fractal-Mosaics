import numpy as np
import scipy.cluster
import scipy
from colorsys import rgb_to_hls, hls_to_rgb, rgb_to_hsv, hsv_to_rgb
from PIL import ImageStat


def map_image(original, list_of_composed):
    pass


def get_average_color_stat(image):
    stat = ImageStat.Stat(image)
    r, g, b = map(int, stat.mean)
    return r, g, b


def get_average_color(image):
    pixels = image.load()
    w, h = image.size
    r, g, b = 0, 0, 0
    amount = w * h
    for i in range(w):
        for j in range(h):
            r += pixels[i, j][0]
            g += pixels[i, j][1]
            b += pixels[i, j][2]

    return r//amount, g//amount, b//amount


def get_frequent_color(image):
    w, h = image.size
    colors = image.getcolors(w * h)
    most_frequent_pixel = max(colors, key=lambda x: x[0])
    return most_frequent_pixel[1]


def most_frequent_color_cluster(image):
    num_clusters = 7

    ar = np.asarray(image)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))

    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    color = tuple([int(c) / 255 for c in peak])

    return color


def find_closest(color, colors, weights=(1, 1, 1), mode='rgb'):
    new_colors = list(colors)[:]
    if mode == 'hls':
        color = rgb_to_hls(*tuple(i/255 for i in color))
        new_colors = [rgb_to_hls(*tuple(i/255 for i in c)) for c in new_colors]

    elif mode == 'hsv':
        color = rgb_to_hsv(*tuple(i/255 for i in color))
        new_colors = [rgb_to_hsv(*tuple(i/255 for i in c)) for c in new_colors]

    closest_color = min(new_colors, key=lambda x: sum((abs(color[i] - x[i]) * weights[i] for i in range(2))))

    if mode == 'hls':
        closest_color = hls_to_rgb(*closest_color)
        closest_color = tuple(round(n*255) for n in closest_color)
        return closest_color

    elif mode == 'hsv':
        closest_color = hsv_to_rgb(*closest_color)
        closest_color = tuple(round(n*255) for n in closest_color)
        return closest_color
    return closest_color


def map_image_test(original, list_of_composed, parts=4, function=get_average_color_stat):
    # returns list of composed images put over original divided by partsXparts
    original = original.image

    resx = original.width // parts
    resy = original.height // parts
    cropped_parts_of_original = [[original.crop((x*resx, y*resy, (x+1)*resx, (y+1)*resy)) for x in range(parts)] for y in range(parts)]

    cropped_parts_with_color = [list(map(lambda x: [x, function(x)], row)) for row in cropped_parts_of_original]
    dict_of_composed_with_colors = {x.get_short_color(function): x for x in list_of_composed}

    list_of_ready_images = [[0] * parts for _ in range(parts)]

    for i in range(len(cropped_parts_with_color)):
        for j in range(len(cropped_parts_with_color[i])):
            list_of_ready_images[j][i] = dict_of_composed_with_colors[find_closest(cropped_parts_with_color[i][j][1], dict_of_composed_with_colors.keys())]

    return list_of_ready_images
