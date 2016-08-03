import prep, tools, solver

t = tools.timer()

n = prep.nodes()
nodes = n.addlist([(0, 0), (4, 0), (4, 4), (0, 4), (8, 0), (8, 4), (12, 0), (12, 4)])
n.info()

n.check([0, 0])

e = prep.elements(nodes)
elements = e.addlist([(1, 2, 3, 4), (3, 5, 6, 4), (5, 7, 8, 6)])
e.info()

m = prep.materials(elements)
m.add("steel")
elements = m.assignall(1)
m.info()

h = prep.thicks(elements)
h.add(0.05)
elements = h.assignall(1)
h.info()

c = prep.constraints()
c.load([8], x = 0, y = -1e8)
cons = c.support([1, 4])
c.info()

d = solver.build(nodes, elements, cons)
sol = d.gauss_linear()

print(sol)
print("Solving time:", t.check())
