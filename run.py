import bmp, prep, tools, solver, postpro

#start timer
t = tools.timer()

#read input file into list
input_file = open("input.txt", "r")
input_file_lines = input_file.readlines()

input_lines = []

#create list of lines and words with no end line symbols
for i in range(len(input_file_lines)):
    input_lines.append(input_file_lines[i].rstrip().split(" "))

def ksearch(keyword):
    for i in range(len(input_lines)):
        if keyword in input_lines[i][0]:
            return input_lines[i][1:]
        #else:
            #return None
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

sol = solver.build(nodes, eles, cons)
if ksearch("solver")[0] == "direct":
    disp = sol.direct()
elif ksearch("solver")[1] == "lsqs":
    disp = sol.least_squares()
strains = sol.strains_calc(disp)

res_d = ksearch("disp")
if res_d is not None:
    post = postpro.prepare(nodes, eles, disp)
for i in range(0, len(res_d)):
    post.save_dresults(res_d[i])

res_s = ksearch("stress")
if res_s is not None:
    post2 = postpro.prepare(nodes, eles, strains)
for i in range(0, len(res_d)):
    post2.save_sresults(res_s[i])
    

print("")
print("Task finished in", t.check())