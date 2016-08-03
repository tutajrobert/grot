from PIL import Image, ImageCms
import numpy
import math
import prep

im = Image.open("im.bmp")
width = im.size[0]
height = im.size[1]

#RGB to Lab conversion

srgb_profile = ImageCms.createProfile("sRGB")
lab_profile  = ImageCms.createProfile("LAB")

rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(
    srgb_profile, lab_profile, "RGB", "LAB"
	)

im_lab = ImageCms.applyTransform(
    im, rgb2lab_transform
	)

im_array = numpy.array(im_lab, dtype='int64')

#dictionary of reference Lab colors

lab_colors = {
    "white" : [255, 0, 0],
	"black" : [0, 0, 0],
	"red" : [138, 81, 70],
	"green" : [224, 177, 81],
	"blue" : [75, 68, 144],
	"cyan" : [231, 205, 241],
	"magenta" : [153, 94, 195],
	"brown" : [89, 26, 45]
	}
	
def color_distance(color, ref_color):
    #euclidean distance
    return math.sqrt(((color[0] - ref_color[0]) ** 2) + ((color[1] - ref_color[1]) ** 2) + ((color[2] - ref_color[2]) ** 2))

def color_check(color, lab_colors):
    #check which reference color in colors dictionary is the closest to given
    dist_list = []
    color_list = []
    for i in lab_colors:
        dist_list.append(color_distance(color, lab_colors[i]))
        color_list.append(i)
    return color_list[dist_list.index(min(dist_list))]
	
bc_list = 	{
    "black" : [],
	"red" : [],
	"green" : [],
	"blue" : [],
	"magenta" : [],
	"brown" : []
    }

n = prep.nodes()

for i in range(height):
    for j in range(width):
        elist = []
        matched_color = color_check(im_array[i][j], lab_colors)
        if matched_color is not "white":
            if n.check(j % width, i) -- None:
                n.add(j % width, i)
            else:
                elist.append(n)
            ###n.addlist[(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            if matched_color is not "cyan":
                bc_list[matched_color].append([i, j])
                
print(bc_list)