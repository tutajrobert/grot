import gc, bmp, prep, tools, solver, postpro, deformed, gallery, version, os, subprocess, sys, prob, plast, iter

#start timer
t = tools.timer()

#read input file into list
input_file = open("input.txt", "r")
input_file_lines = input_file.readlines()

input_lines = []

#create list of lines and words with no end line symbols
for i in range(len(input_file_lines)):
    input_lines.append(input_file_lines[i].rstrip().split(" "))

input_file.close()

def ksearch(keyword):
    for i in range(len(input_lines)):
        if (keyword in input_lines[i][0]) and ("#" not in input_lines[i]):
            return input_lines[i][1:]
    return [None]

proj_name = ksearch("project")[0]
            
im = bmp.open(ksearch("bmp")[0])
geom = bmp.create_geom(im)

nodes = geom[0].store()
eles = geom[1].store()
c = geom[2]
bc_dict = geom[3]
eprobes_dict = geom[4]

im, geom = None, None

m = prep.materials(eles)
m.add(ksearch("mat")[0])
m.assignall(1)
m.set_unit(ksearch("unit")[0])
m.set_scale(float(ksearch("scale")[0]))
scale = float(ksearch("scale")[0])

h = prep.thicks(eles, m)
h.add(float(ksearch("thickness")[0]))
h.assignall(1)

loads_list = []
for i in range(len(input_lines)):
    if "load" in input_lines[i][0]:
        loads_list.append(i)

for i in range(len(loads_list)):
    c.load(bc_dict[input_lines[loads_list[i]][5]], 
           x = float(input_lines[loads_list[i]][2]), 
           y = float(input_lines[loads_list[i]][4]))

cons = c.store()
c, bc_dict = None, None

state = ksearch("problem")[0]
sol = solver.build(nodes, eles, cons, state, load_inc = 1.0, scale = scale)
nodes, cons = None, None

if ksearch("plast")[0] != "yes":
    if ksearch("solver")[0] == "direct":
        disp = sol.direct()
    elif ksearch("solver")[0] == "lsqs":
        disp = sol.least_squares()
    elif ksearch("solver")[0] == "cholesky":
        disp = sol.cholesky()
    strains = sol.strains_calc(disp)

##########
if ksearch("plast")[0] == "yes":
    disp = sol.direct_plast()
    strains = sol.strains_calc(disp, msg = 0)
    iter_res = iter.prepare(disp, strains)
    step_factor = iter_res.first_step()
if (ksearch("plast")[0] == "yes") and (step_factor < 1):
    load_step = step_factor
    steps_num = int(ksearch("plast")[1])
    load_inc = (1 - step_factor) / (steps_num)
    flags_list = []
    eles_list = []
    for i in range(steps_num):
        load_step += load_inc
        
        #RK2
        sol.plast_update([], load_inc / 2.0)
        disp = sol.direct_plast()
        strains = sol.strains_calc(disp, msg = 0)
        halfstep_strains = iter_res.halfstep(strains)
        plast_res = plast.search(eles, halfstep_strains, m, flags_list)
        eles_list = plast_res[0]
        #eles = plast_res[0]
        flags_list = plast_res[1]
        print("plast" + str(load_step))
        state = ksearch("problem")[0]
        sol.plast_update(eles_list, load_inc)
        m.assignplast(eles_list)
        disp = sol.direct_plast()
        strains = sol.strains_calc(disp, msg = 0)
        final_results = iter_res.store(disp, strains, flags_list)
        disp = final_results[0]
        strains = final_results[1]   
    strains = iter_res.store_plstrain(strains)
#############

sol, iter_res, plast = None, None, None
halfstep_strains, plast_res, final_results = None, None, None
gc.collect()

gallery_input_file = ""

for i in input_file_lines:
    if (i[0] != "#") and (len(i) != 1):
        gallery_input_file += "<code>" + i + "</code><br>"

probe_color = ksearch("probe")[0]
prob.write(probe_color, bc_dict, eprobes_dict, disp, strains, proj_name)
        
results_list = []

desc_list = []

res_d = ksearch("disp")
if res_d is not None:
    post = postpro.prepare(eles, disp)
for i in range(0, len(res_d)):
    res_name = post.save_dresults(res_d[i], proj_name)
    results_list.append("disp_" + res_d[i] + ".png")
    desc_list.append(res_name)
post = None

res_s = ksearch("stress")
if res_s[0] is not None:
    post2 = postpro.prepare(eles, strains)
    for i in range(0, len(res_s)):
        res_name = post2.save_sresults(res_s[i], proj_name)
        results_list.append(res_s[i] + ".png")
        desc_list.append(res_name)
post2 = None
strains = None

def_scale = ksearch("deformed")[0]
if def_scale is not None:
    post3 = deformed.prepare(eles, disp, float(def_scale))
    res_name = post3.save_deformed("deformed", proj_name)
    results_list.append("deformed" + ".png")
    desc_list.append(res_name)
post3 = None
eles, disp = None, None

gallery.save_gallery(proj_name, results_list, desc_list, gallery_input_file, version.get())	
gallery_path = "results" + os.sep + proj_name + os.sep + proj_name + "_gallery.html"

print("")
print("Task finished in", t.check())