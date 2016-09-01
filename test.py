import bmp, prep, tools, solver, postpro

t = tools.timer()

im = bmp.open("im.bmp")
geom = bmp.create_geom(im)

nodes = geom[0].store()
eles = geom[1].store()
c = geom[2]
bc_dict = geom[3]

m = prep.materials(eles)
m.add("steel")
m.assignall(1)
m.set_unit("mm")
m.set_scale(5)

h = prep.thicks(eles)
h.add(1)
h.assignall(1)

c.load(bc_dict["magenta"], x = 1, y = 0)
cons = c.store()

sol = solver.build(nodes, eles, cons)
res = sol.direct()

post = postpro.prepare(nodes, eles, res)
post.save_results("disp_x")
post.save_results("disp_y")
post.save_results("disp_mag")

print("Task finished in", t.check())