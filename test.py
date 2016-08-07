import bmp, prep, tools, solver, postpro

t = tools.timer()

geom = bmp.create_geom()

nodes = geom[0].store()
eles = geom[1].store()
c = geom[2]
bc_dict = geom[3]
    
m = prep.materials(eles)
m.add("steel")
m.assignall(1)

h = prep.thicks(eles)
h.add(1)
h.assignall(1)

c.load(bc_dict["magenta"], x = 1, y = 0)
cons = c.store()

sol = solver.build(nodes, eles, cons)
res = sol.gauss_linear()

post = postpro.prepare(nodes, eles, res)
post.nod_disp()

print("Solving time:", t.check())