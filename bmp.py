"""BMP to FE model translation module"""

import math
import os
import sys
import io
import numpy
from PIL import Image, ImageCms
from .prep import constraints, elements, nodes
from functools import lru_cache

def load_im(im_string):
    imgObject = io.BytesIO(im_string)
    image = Image.open(imgObject)
    return process_im(image)

def open_im(im_name, im_path):
    """Opens and crops BMP file. Returns image numpy array and image size"""
    path = "projects" + os.sep + im_name #default path for image is "projects" directory
    if im_path != False:
        path = im_path + os.sep + im_name
    image = Image.open(path)
    return process_im(image)

def process_im(image):
    #Image cropping
    pix = numpy.asarray(image)
    pix = pix[:, :, 0:3] #drop the alpha channel
    idx = numpy.where(pix - 255)[0:2] #drop the color when finding edges
    box = list(map(min, idx))[::-1] + list(map(max, idx))[::-1] #box of non-white pixels
    box[2] += 1
    box[3] += 1
    image = image.crop(box)

    #Size check
    width = image.size[0]
    height = image.size[1]

    #RGB to Lab color profile conversion
    srgb_profile = ImageCms.createProfile("sRGB")
    lab_profile = ImageCms.createProfile("LAB")
    rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(
        srgb_profile, lab_profile, "RGB", "LAB"
        )
    im_lab = ImageCms.applyTransform(image, rgb2lab_transform)
    im_array = numpy.array(im_lab, dtype='int64')

    image.close()
    return[im_array, width, height]

#Dictionary of hardcoded reference Lab colors

LAB_COLORS = {
    "white" : [255, 0, 0],
    "black" : [0, 0, 0],
    "red" : [138, 81, 70],
    "green" : [224, 177, 81],
    "blue" : [75, 68, 144],
    "cyan" : [231, 205, 241],
    "magenta" : [153, 94, 195],
    "brown" : [89, 26, 45]
    }

COLORS = ["white", "black", "red", "green", "blue", "cyan", "magenta", "brown"]

def color_distance(color, ref_color):
    """Returns Euclidean distance value in Lab color space"""
    return math.sqrt(((color[0] - ref_color[0]) ** 2) + \
                     ((color[1] - ref_color[1]) ** 2) + \
                     ((color[2] - ref_color[2]) ** 2))

lru_cache(None, False)
def color_check(color):
    """Checks and returns reference color closest to given"""
    min_distance = 100000000
    matched_color = None
    for color_name, values in LAB_COLORS.items():
        cur_dist = color_distance(color, values)
        if cur_dist < min_distance:
            min_distance = cur_dist
            matched_color = color_name
    return matched_color

#Colors used as boundary conditions
#Just need to know that "cyan" is used as model body and "white" is used for background

BC_DICT = {cname : [] for cname in COLORS}
PROB_DICT = {cname : [] for cname in COLORS if cname not in ("white", "cyan")}

#Starting BMP to FEM model translation

NODES = nodes()
ELES = elements(NODES.store())
CONS = constraints()


def create_geom(im_data):
    """Creates FE model"""
    elist = []
    node_dict = {}
    im_array, width, height = im_data[0], im_data[1], im_data[2]

    def node_proc(j, i, counter):
        """Checking if node coordinates are already assigned to node number.
        If yes : use old number, if no create new merged_dictionary = {**dict1, **dict2}"""
        node = node_dict.get((j,i))
        if node is None:
            ele = NODES.add(j, i)
            elist.append(ele)
            node_dict[(j, i)] = ele
        else:
            elist.append(node)

    for i in range(height):

        #Progress text in percents
        sys.stdout.write("\r" + "Bitmap to finite elements model translation [" + \
                         str(round(((i + 1) / height) * 100, 2)) + " %]")
        sys.stdout.flush()

        for j in range(width):
            elist = []
            match_color = color_check(tuple(im_array[i][j]))
            if match_color != "white":
                node_proc(j % width, i, i)
                node_proc((j % width) + 1, i, i)
                node_proc((j % width) + 1, i + 1, i)
                node_proc(j % width, i + 1, i)

                ELES.update(NODES.store())
                ELES.add(elist[3], elist[2], elist[1], elist[0])

                #Checking which node should go to bc dict
                if match_color not in ["white", "cyan"]:
                    BC_DICT[match_color].append(NODES.check(j % width, i))
                    BC_DICT[match_color].append(NODES.check((j % width) + 1, i))
                    BC_DICT[match_color].append(NODES.check((j % width) + 1, i + 1))
                    BC_DICT[match_color].append(NODES.check(j % width, i + 1))
                    PROB_DICT[match_color].append(ELES.get(elist[3], elist[2], elist[1], elist[0]))

    #Image, nodes, elements, boundaries info text
    print("\nCalculated object size: [{} x {}]".format(width, height))
    NODES.short_info()
    ELES.short_info()
    im_data = None

    print_list = ""
    for color in BC_DICT:
        if BC_DICT[color]:
            print_list += "[" + str(color) + " : " + str(int(len(BC_DICT[color]) / 4)) + "] "
    print("Prepared boundaries applied to eles: " + print_list)

    #Hardcoded colors for supports: red in X dir, green in Y dir, blue in X and Y dirs

    support_colors = ["red", "green", "blue"]
    support_types = {"red" : "X", "green" : "Y", "blue" : "X, Y"}
    CONS.support(BC_DICT["blue"])
    CONS.support(BC_DICT["red"], 0, 1)
    CONS.support(BC_DICT["green"], 1, 0)
    for color in support_colors:
        if BC_DICT[color]:
            color_len = len(list(set(BC_DICT[color])))
            print(color.capitalize() + " boundary [" + support_types[color] + \
                  " support] applied to [" + str(color_len) + "] nodes")

    return [NODES.number(), ELES, CONS, BC_DICT, PROB_DICT]
