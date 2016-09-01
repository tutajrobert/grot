from PIL import Image, ImageCms
import numpy
import math
import prep
import solver

def open(im_name):
    #Image opening and size check
    
    #Welcome message
    print("")
    print("GRoT> ver. 0.1")
    print("FEM 2d plates solver operating on bitmap files")
    
    im = Image.open(im_name)
    width = im.size[0]
    height = im.size[1]

    #RGB to Lab conversion

    srgb_profile = ImageCms.createProfile("sRGB")
    lab_profile  = ImageCms.createProfile("LAB")

    rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(
        srgb_profile, lab_profile, "RGB", "LAB"
	    )

    im_lab = ImageCms.applyTransform(im, rgb2lab_transform)

    im_array = numpy.array(im_lab, dtype='int64')
    
    return[im_array, width, height]

"""
Dictionary of reference Lab colors
these below are hardcoded
"""

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
    #Euclidean distance in Lab color space
    return math.sqrt(((color[0] - ref_color[0]) ** 2) + ((color[1] - ref_color[1]) ** 2) + ((color[2] - ref_color[2]) ** 2))

def color_check(color, lab_colors):
    #Check which reference color in colors dictionary is the closest to given
    dist_list = []
    color_list = []
    for i in lab_colors:
        dist_list.append(color_distance(color, lab_colors[i]))
        color_list.append(i)
    return color_list[dist_list.index(min(dist_list))]

"""
Colors used as boundary conditions
Just need to know that "cyan" is used as model body
and "white" is used for background
"""

bc_dict = 	{
    "black" : [],
	"red" : [],
	"green" : [],
	"blue" : [],
	"magenta" : [],
	"brown" : []
    }

#Starting BMP to fem model translation

n = prep.nodes()
e = prep.elements(n.store())
c = prep.constraints()

def create_geom(im_data):
    im_array, width, height = im_data[0], im_data[1], im_data[2]
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
                e.add(elist[3], elist[2], elist[1], elist[0])

                #Checking which node should go to bc list
                if (matched_color is not "white") and (matched_color is not "cyan"):
                    bc_dict[matched_color].append(n.check(j % width, i))
                    bc_dict[matched_color].append(n.check((j % width) + 1, i))
                    bc_dict[matched_color].append(n.check((j % width) + 1, i + 1))
                    bc_dict[matched_color].append(n.check(j % width, i + 1))             

    """
    Hardcoded colors for supports
    Red     support in X direction
    Green   support in Y direction
    Blue    support in Z (in-plane) direction
    Nice and simple pattern, don't you think so?
    """
    
    c.support(bc_dict["blue"])
    c.support(bc_dict["red"], 0, 1)
    c.support(bc_dict["green"], 1, 0)
    
    #Rest of colors: black, magenta and brown can be used for different bc or property assignment
    
    print("")
    print("Bitmap to finite elements model translated")
    #print("")
    
    n.short_info()
    e.short_info()
    
    #Boundary conditions summary echo
    
    #print("# boundaries info")
    print_list = ""
    for color in bc_dict:
        if len(bc_dict[color]) > 0:
            print_list += "[" + str(color) + " : " + str(len(bc_dict[color])) + "] "
    print("Prepared following boundaries:" + print_list)
            #print(color, ":", len(bc_dict[color]), "eles")
    #print("")
    
    #Nodes, eles, constraints and boundaries
    return [n, e, c, bc_dict]