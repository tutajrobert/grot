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
e = prep.elements(n.store())
c = prep.constraints()

for i in range(height):
    for j in range(width):
        elist = []
        matched_color = color_check(im_array[i][j], lab_colors)
        if matched_color is not "white":

            n1 = n.check(j % width, i)
            if n1 == None:
                e1 = n.add(j % width, i)
                elist.append(e1)
            else:
                elist.append(n1)

            n2 = n.check((j % width) + 1, i)
            if n2 == None:
                e2 = n.add((j % width) + 1, i)
                elist.append(e2)
            else:
                elist.append(n2)
				
            n3 = n.check((j % width) + 1, i + 1)
            if n3 == None:
                e3 = n.add((j % width) + 1, i + 1)
                elist.append(e3)
            else:
                elist.append(n3)
				
            n4 = n.check(j % width, i + 1)
            if n4 == None:
                e4 = n.add(j % width, i + 1)
                elist.append(e4)
            else:
                elist.append(n4)
			
            e.update(n.store())
            e.add(elist[0], elist[1], elist[2], elist[3])
			
            if (matched_color is not "white") and (matched_color is not "cyan"):
                bc_list[matched_color].append(n.check(j % width, i))
                bc_list[matched_color].append(n.check((j % width) + 1, i))
                bc_list[matched_color].append(n.check((j % width) + 1, i + 1))
                bc_list[matched_color].append(n.check(j % width, i + 1))
n.info()
e.info()				
print(bc_list)