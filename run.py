"""Run"""

import copy
import gc
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
import plast
import msg

#start timer
TIME = tools.timer()

#welcome message
msg.welcome()

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

NODES = GEOM[0].store()
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

if ksearch("plast")[0] != "yes":
    disp = SOL.direct()
    strains = SOL.strains_calc(disp)

##########
if ksearch("plast")[0] == "yes":
    disp = SOL.direct_plast()
    disp_el = copy.copy(disp)
    strains = SOL.strains_calc(disp, msg=0)
    strains_el = copy.deepcopy(strains)
    iter_res = plast.Prepare(disp, strains, ELES)
    step_factor = iter_res.first_step(MAT)

if (ksearch("plast")[0] == "yes") and (step_factor < 1):
    load_step = step_factor
    steps_num = int(ksearch("plast")[1])
    load_inc = (1 - step_factor) / (steps_num)
    flags_list = []
    eles_list = []
    sys.stdout.write("\r" + "Nonlinear plasticity solver iteration [" + str(1) + \
                     " of " + str(steps_num) + "]")
    sys.stdout.flush()

    #file = open("results" + os.sep + PROJ_NAME + os.sep + "plast.txt", "w")
    for i in range(steps_num):
        load_step += load_inc
        check_res = iter_res.out()
        #RK2
        SOL.plast_update([], load_inc / 2.0)
        disp = SOL.direct_plast()
        strains = SOL.strains_calc(disp, msg=0)
        halfstep_strains = iter_res.halfstep(strains)

        plast_res = plast.search(ELES, halfstep_strains, flags_list)

        eles_list = plast_res[0]
        flags_list = plast_res[1]

        sys.stdout.write("\r" + "Nonlinear plasticity solver iteration [" + \
                         str(i + 1) + " of " + str(steps_num) + "]")
        sys.stdout.flush()

        STATE = ksearch("problem")[0]
        SOL.plast_update(eles_list, load_inc)
        MAT.assignplast(eles_list)

        disp = SOL.direct_plast()
        strains = SOL.strains_calc(disp, msg=0)

        final_results = iter_res.store(MAT, disp, strains, flags_list)
        disp = final_results[0]
        strains = final_results[1]

    check_res = iter_res.out()
    strains = iter_res.store_plstrain(strains)
    res_disp = iter_res.residual_disp(disp_el)
    res_strains = iter_res.residual_strains(strains_el)
    print("")
#############

    disp_el, iter_res, plast = None, None, None
    halfstep_strains, plast_res, final_results = None, None, None
gc.collect()

print("")
gallery_input_file = ""

for i in INP_FILE_LINES:
    if (i[0] != "#") and (len(i) != 1):
        gallery_input_file += "<code>" + i + "</code><br>"

probe_color = ksearch("probe")[0]
prob.write(probe_color, BC_DICT, PROB_DICT, disp, strains, PROJ_NAME, MAT)

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

def_scale = ksearch("deformed")[0]
if def_scale is not None:
    post3 = deformed.Prepare(ELES, disp, float(def_scale))
    res_name = post3.save_deformed("deformed", PROJ_NAME)
    results_list.append("deformed" + ".png")
    desc_list.append(res_name)
post3 = None
disp = None

if (ksearch("plast")[0] == "yes") and (step_factor < 1):
    post4 = postpro.Prepare(ELES, res_disp)
    res_name = post4.save_dresults("res", PROJ_NAME)
    results_list.append("disp_res.png")
    desc_list.append(res_name)

    res_name = post2.save_sresults("pl_strain", PROJ_NAME)
    results_list.append("pl_strain" + ".png")
    desc_list.append(res_name)
    res_name = post2.save_sresults("h_stress", PROJ_NAME)
    results_list.append("h_stress" + ".png")
    desc_list.append(res_name)

    res_strains.append(strains[4])

    print("Results of plastic analysis stored in " + \
          "results" + os.sep + PROJ_NAME + os.sep + PROJ_NAME)

gallery.save_gallery(PROJ_NAME, results_list, desc_list, gallery_input_file, version.get())
gallery_path = "results" + os.sep + PROJ_NAME + os.sep + PROJ_NAME + "_gallery.html"

print("")
print("Task finished in", TIME.check())
