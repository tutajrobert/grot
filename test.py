import prep

ndict = prep.nodes()
edict = prep.elements(ndict)

n1 = ndict.add(0, 0)
n2 = ndict.add(1, 0)
n3 = ndict.add(1, 1)
n4 = ndict.add(0, 1)

edict.update(ndict.store())

e1 = edict.add(n1, n2, n3, n4)

edict.get(n1, n2, n3, n4)