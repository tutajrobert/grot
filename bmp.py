from PIL import Image, ImageCms
import numpy
import math
import prep
import solver
import sys
import version

vers = version.get()

def open(im_name):
    
    #Welcome message
    print("")
    print("GRoT> ver. " + vers + ", [Graficzny Rozwiązywacz Tarcz]")
    print("..............................................")
    
    #Image opening and size check
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
    return math.sqrt(((color[0] - ref_color[0]) ** 2) + \
                     ((color[1] - ref_color[1]) ** 2) + \
                     ((color[2] - ref_color[2]) ** 2))

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

def node_check(coords, ndict):
    #Check if node with x, y coordinates is already included in ndict
    for n in ndict:
        if ndict[n] == [coords[0], coords[1]]:
            return n

def create_geom(im_data):
    print("")

    nmerge_list = []
    im_array, width, height = im_data[0], im_data[1], im_data[2]
    
    for i in range(height):
        nmerge_list.append({})
        
        #Progress text in percents
        sys.stdout.write("\r" + 
            "Bitmap to finite elements model translation [" + 
            str(round(((i + 1) / height) * 100, 2)) + 
            " %]")
        sys.stdout.flush()
              
        for j in range(width):
            elist = []
            matched_color = color_check(im_array[i][j], lab_colors)
            if matched_color is not "white":

                """
                Checking if node coordinates are already assigned to
                node number. If yes : use old number, if no create new one
                merged_dictionary = {**dict1, **dict2}
                """
                
                #node 1
                n1 = node_check([j % width, i], 
                                {**nmerge_list[i], **nmerge_list[i - 1]})
                if n1 == None:
                    e1 = n.add(j % width, i)
                    elist.append(e1)
                    nmerge_list[i][e1] = [j % width, i]
                else:
                    elist.append(n1)
                    nmerge_list[i][n1] = [j % width, i]

                #node 2
                n2 = node_check([(j % width) + 1, i], 
                                {**nmerge_list[i], **nmerge_list[i - 1]})
                if n2 == None:
                    e2 = n.add((j % width) + 1, i)
                    elist.append(e2)
                    nmerge_list[i][e2] = [(j % width) + 1, i]
                else:
                    elist.append(n2)
                    nmerge_list[i][n2] = [(j % width) + 1, i]

                #node 3
                n3 = node_check([(j % width) + 1, i + 1], 
                                 {**nmerge_list[i], **nmerge_list[i - 1]})
                if n3 == None:
                    e3 = n.add((j % width) + 1, i + 1)
                    elist.append(e3)
                    nmerge_list[i][e3] = [(j % width) + 1, i + 1]
                else:
                    elist.append(n3)
                    nmerge_list[i][n3] = [(j % width) + 1, i + 1]
                
                #node 4
                n4 = node_check([j % width, i + 1], 
                                {**nmerge_list[i], **nmerge_list[i - 1]})
                if n4 == None:
                    e4 = n.add(j % width, i + 1)
                    elist.append(e4)
                    nmerge_list[i][e4] = [j % width, i + 1]
                else:
                    elist.append(n4)
                    nmerge_list[i][n4] = [j % width, i + 1]

                e.update(n.store())
                e.add(elist[3], elist[2], elist[1], elist[0])

                #Checking which node should go to bc list
                if (matched_color is not "white") and (matched_color is not "cyan"):
                    bc_dict[matched_color].append(n.check(j % width, i))
                    bc_dict[matched_color].append(n.check((j % width) + 1, i))
                    bc_dict[matched_color].append(n.check((j % width) + 1, i + 1))
                    bc_dict[matched_color].append(n.check(j % width, i + 1))
    
    #Rest of colors: black, magenta and brown can be used for different bc or property assignment
    
    #Nodes and elements info
    print("")
    n.short_info()
    e.short_info()
    
    print_list = ""
    for color in bc_dict:
        if len(bc_dict[color]) > 0:
            print_list += "[" + str(color) + " : " + str(int(len(bc_dict[color]) / 4)) + "] "
    print("Prepared boundaries applied to eles: " + print_list)
    
    """
    Hardcoded colors for supports
    Red     support in X direction
    Green   support in Y direction
    Blue    support in Z (in-plane) direction
    Nice and simple pattern, don't you think so?
    """
    
    c.support(bc_dict["blue"])
    if len(bc_dict["blue"]) > 0:
        blue_n = len(bc_dict["blue"])
        print("Blue boundary [fixed support] applied to [" + str(blue_n) + "] nodes")
    c.support(bc_dict["red"], 0, 1)
    if len(bc_dict["red"]) > 0:
        red_n = len(bc_dict["red"])
        print("Red boundary [in x-dir support] applied to [" + str(red_n) + "] nodes")
    c.support(bc_dict["green"], 1, 0)    
    if len(bc_dict["green"]) > 0:
        green_n = len(bc_dict["green"])
        print("Green boundary [in y-dir support] applied to [" + str(green_n) + "] nodes")    
    #Return nodes, eles, constraints and boundaries
    return [n, e, c, bc_dict]