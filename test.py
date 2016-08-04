import bmp, prep, tools, solver

t = tools.timer()

geom = bmp.create_geom()
nodes = geom[0].store()
eles = geom[1].store()
c = geom[2]
bc_dict = geom[3]
    
    
"""n = prep.nodes()
nodes = n.addlist([(0, 0), (1, 0), (1, 1), (0, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1)])
n.info()

e = prep.elements(nodes)
elements = e.addlist([(1, 2, 3, 4), (3, 5, 6, 4), (5, 7, 8, 6), (7, 9, 10, 8)])
e.info()
"""
m = prep.materials(eles)
m.add("steel")
elements = m.assignall(1)
#m.info()

h = prep.thicks(eles)
h.add(1)
elements = h.assignall(1)
#h.info()

#c = prep.constraints()
c.load(bc_dict["magenta"], x = 1, y = 0)
#cons = c.support([1, 2, 3, 4])
#c.info()
cons = c.store()

d = solver.build(nodes, eles, cons)
sol = d.gauss_linear()

print(sol)
print("Solving time:", t.check())
