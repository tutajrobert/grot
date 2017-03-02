import bmp, prep, tools, solver, postpro, deformed, gallery, version, os

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
        if (keyword in input_lines[i][0]) and ("#" not in input_lines[i][0]):
            return input_lines[i][1:]
        #else:
            #return None

proj_name = ksearch("project")[0]            
            
im = bmp.open(ksearch("bmp")[0])
geom = bmp.create_geom(im)

nodes = geom[0].store()
eles = geom[1].store()
c = geom[2]
bc_dict = geom[3]

m = prep.materials(eles)
m.add(ksearch("mat")[0])
m.assignall(1)
m.set_unit(ksearch("unit")[0])
m.set_scale(float(ksearch("scale")[0]))

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

state = ksearch("problem")[0]
sol = solver.build(nodes, eles, cons, state)
if ksearch("solver")[0] == "direct":
    disp = sol.direct()
elif ksearch("solver")[0] == "lsqs":
    disp = sol.least_squares()
elif ksearch("solver")[0] == "cholesky":
    disp = sol.cholesky()
strains = sol.strains_calc(disp)

gallery_input_file = ""

for i in input_file_lines:
    if i[0] != "#":
        gallery_input_file += i + "<br>"

results_list = []
				 
results_names = {"x" : "Displacement in X direction",
                 "y" : "Displacement in Y direction",
				 "mag" : "Displacement magnitude",
				 "eps_x" : "Normal XX component of strain tensor",
				 "eps_y" : "Normal YY component of strain tensor",
				 "gamma_xy" : "Shear XY component of strain tensor",
				 "sig_x" : "Normal XX component of stress tensor",
				 "sig_y" : "Normal YY component of stress tensor",
				 "tau_xy" : "Shear XY component of stress tensor",
				 "huber" : "Huber equivalent stress",
				 "sign_huber" : "Signed Huber equivalent stress",
				 "deformed" : "Deformed plot (displacement magnitude)"}

desc_list = []
				 
res_d = ksearch("disp")
if res_d is not None:
    post = postpro.prepare(nodes, eles, disp)
for i in range(0, len(res_d)):
    post.save_dresults(res_d[i], proj_name)
    results_list.append("disp_" + res_d[i] + ".png")
    desc_list.append(results_names[res_d[i]])

def_scale = ksearch("deformed")[0]
if def_scale is not None:
    post3 = deformed.prepare(nodes, eles, disp, float(def_scale))
    post3.save_deformed("deformed", proj_name)
    results_list.append("deformed" + ".png")
    desc_list.append(results_names["deformed"])	
	
res_s = ksearch("stress")
if res_s is not None:
    post2 = postpro.prepare(nodes, eles, strains)
for i in range(0, len(res_s)):
    post2.save_sresults(res_s[i], proj_name)
    results_list.append(res_s[i] + ".png")
    desc_list.append(results_names[res_s[i]])

gallery.save_gallery(proj_name, results_list, desc_list, gallery_input_file, version.get())	
	
print("")
print("Task finished in", t.check())