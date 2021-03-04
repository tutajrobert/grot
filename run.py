import os
import sys
import bmp
import prep
import tools
import solver
import postpro
import deformed
import gallery
import version
import prob

#start timer
TIME = tools.timer()

#welcome message
print("")
print("GRoT> ver. " + version.get() + ", [Graficzny Rozwiązywacz Tarcz]")
print("................................................\n")

#read input file into list
INP_FILE = open("input.txt", "r")
INP_FILE_LINES = INP_FILE.readlines()

INP_LINES = []

#create list of lines and words with no end line symbols
for i in range(len(INP_FILE_LINES)):
    INP_LINES.append(INP_FILE_LINES[i].rstrip().split(" "))

INP_FILE.close()

def ksearch(keyword):
    for i in range(len(INP_LINES)):
        if (keyword in INP_LINES[i][0]) and ("#" not in INP_LINES[i]):
            return INP_LINES[i][1:]
    return [None]

PROJ_NAME = ksearch("project")[0]

IMAGE = bmp.open_im(ksearch("bmp")[0])
GEOM = bmp.create_geom(IMAGE)

NODES = GEOM[0]
ELES = GEOM[1].store()
CONS = GEOM[2]
BC_DICT = GEOM[3]
PROB_DICT = GEOM[4]

IMAGE, GEOM = None, None

MAT = prep.materials(ELES)
MAT.add(ksearch("mat")[0])
MAT.assignall(1)
MAT.set_unit(ksearch("unit")[0])
MAT.set_scale(float(ksearch("scale")[0]))
SCALE = float(ksearch("scale")[0])

THICKS = prep.thicks(ELES, MAT)
THICKS.add(float(ksearch("thickness")[0]))
THICKS.assignall(1)

loads_list = []
for i in range(len(INP_LINES)):
    if "load" in INP_LINES[i][0]:
        loads_list.append(i)

for i in range(len(loads_list)):
    CONS.load(BC_DICT[INP_LINES[loads_list[i]][5]],
              x=float(INP_LINES[loads_list[i]][2]),
              y=float(INP_LINES[loads_list[i]][4]))

constraints = CONS.store()
CONS, BC_DICT = None, None

STATE = ksearch("problem")[0]
SOL = solver.Build(NODES, ELES, constraints, STATE, load_inc=1.0, scale=SCALE)
NODES, constraints = None, None

if not os.path.exists("results" + os.sep + PROJ_NAME):
    os.makedirs("results" + os.sep + PROJ_NAME)

disp = SOL.direct()
strains = SOL.strains_calc(disp)

print("")
gallery_input_file = ""

for i in INP_FILE_LINES:
    if (i[0] != "#") and (len(i) != 1):
        gallery_input_file += "<code>" + i + "</code><br>"

probe_color = ksearch("probe")[0]
prob.write(probe_color, PROB_DICT, strains, PROJ_NAME, MAT)

results_list = []
desc_list = []

res_d = ksearch("disp")
if res_d is not None:
    post = postpro.Prepare(ELES, disp)

for i in range(0, len(res_d)):
    sys.stdout.write("\r" + "Plotted displacements results [" + str(i + 1) + \
                     " of " + str(len(res_d)) + "] to results" + os.sep + PROJ_NAME + os.sep)
    sys.stdout.flush()
    res_name = post.save_dresults(res_d[i], PROJ_NAME)
    results_list.append("disp_" + res_d[i] + ".png")
    desc_list.append(res_name)
post = None
print("")

res_s = ksearch("stress")
if res_s[0] is not None:
    post2 = postpro.Prepare(ELES, strains)
    for i in range(0, len(res_s)):
        sys.stdout.write("\r" + "Plotted stress and strains results [" + str(i + 1) + " of " + \
                         str(len(res_s)) + "] to results" + os.sep + PROJ_NAME + os.sep)
        sys.stdout.flush()
        res_name = post2.save_sresults(res_s[i], PROJ_NAME)
        results_list.append(res_s[i] + ".png")
        desc_list.append(res_name)
    print("")
post2 = None

def_scale = ksearch("deformed")[0]
if def_scale is not None:
    post3 = deformed.Prepare(ELES, disp, float(def_scale))
    res_name = post3.save_deformed("deformed", PROJ_NAME)
    results_list.append("deformed" + ".png")
    desc_list.append(res_name)
post3 = None
disp = None

gallery.save_gallery(PROJ_NAME, results_list, desc_list, gallery_input_file, version.get())
gallery_path = "results" + os.sep + PROJ_NAME + os.sep + PROJ_NAME + "_gallery.html"

print("")
print("Task finished in", TIME.check())
