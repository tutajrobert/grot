from .mlib import mdict

#Units for further use
units = {"nm" : 1e-9,
         "um" : 1e-6,
         "mm" : 1e-3,
         "cm" : 1e-2,
         "dm" : 1e-1,
         "m"  : 1e0,
         "km" : 1e3}

class nodes():
#Class contains total number of nodes in nnum and node properties dict ndict
    def __init__(self):
        self.ndict = {}
        self.coord_dict = {}
        self.nnum = 0

    def add(self, x, y):
    #Adds a node of x, y coordinates as a dictionary item with key of node number
        self.nnum += 1
        self.ndict[self.nnum] = [x, y]
        self.coord_dict[(x, y)] = self.nnum
        return self.nnum

    def check(self, x, y):
    #Check if node with x, y coordinates is already included in ndict
        return self.coord_dict.get((x, y))

    def store(self):
    #Just returns dict of nodes
        return self.ndict

    def info(self):
    #Prints number of nodes and nodes dict
        print("# nodes info")
        print("number of nodes: " + str(self.nnum))
        print("nnum", ":", "[xcoord, ycoord]")
        for n in self.ndict:
            print("n" + str(n), ":", self.ndict[n])
        print("")

    def short_info(self):
    #Prints only nodes number
        #print("# nodes info")
        print("Created [" + str(self.nnum) + "] nodes")
        #print("")
        
    def number(self):
        return self.nnum

class elements():
#Class contains total number of elements in enum and element properties dict edict
    def __init__(self, ndict):
            self.edict = {}
            self.coord_dict = {}
            self.enum = 0
            self.ndict = ndict

    def add(self, n1, n2, n3, n4):
    #Adds four nodes rectangle element. Takes nodes dictionaries and nodes elements
        self.enum += 1
        self.edict[self.enum] = [self.ndict[n4],
                                 n1, n2, n3, n4,
                                 0, 0, 0, 0, 0]
        self.coord_dict[(n1, n2, n3, n4)] = self.enum
        return self.edict

    def get(self, n1, n2, n3, n4):
    #Finds and returns element number given by four nodes
        return self.coord_dict.get((n1, n2, n3, n4))

    def info(self):
    #Prints number of elements and elements list
        print("# elements info")
        print("number of elements: " + str(self.enum))
        print("enum", ":", "[n1, n2, n3, n4]")
        for e in self.edict:
            print("e" + str(e), ":", self.edict[e][1:5])
        print("")

    def update(self, ndict):
    #Rewrites dict of nodes with new one
        self.ndict = ndict

    def store(self):
    #Just returns dict of elements
        return self.edict

    def short_info(self):
    #Prints only elements number
        #print("# elements info")
        print("Created [" + str(self.enum) + "] elements")
        #print("")

class materials():
#Class contains materials data and element to which materials are assigned  
    def __init__(self, edict):
        self.edict = edict
        self.mnum = 0
        self.mat = {}
        self.mnames = {}
        self.unit = ""
        self.scale = 0

    def add(self, name):
    #Adds material by name to prep from mlib.py
        self.mnum += 1
        self.mat[self.mnum] = mdict()[name]
        self.mnames[self.mnum] = name

    def assignall(self, mnum):
    #Assign added material to all elements
        for e in self.edict:
            self.edict[e][5] = self.mat[mnum][0]
            self.edict[e][6] = self.mat[mnum][1]
            self.edict[e][8] = self.mat[mnum][2]
            self.edict[e][9] = self.mat[mnum][3]
        print("Property of all eles set to", "[" + str(self.mnames[mnum]) + "]", 
              "(" + str(self.mat[mnum][0] / 1e9) + " GPa,",
              str(self.mat[mnum][1]) + ")")
        return self.edict

    def assignplast(self, elist):
        #print("Assign plasticity")
        #print(elist)
        for i in range(len(elist)):
            #pass
            self.edict[elist[i]][5] *= self.edict[elist[i]][9]
            self.edict[elist[i]][6] = .4999
        #return self.edict

    def info(self):
    #Prints material list
        print("# materials info")
        for m in self.mat:
            print("m" + str(m), self.mnames[m], ":", 
                   str(int(self.mat[m][0] / 1e9)) + "e+9 GPa,", 
                   round(self.mat[m][1], 2))  
        print("")

    def set_unit(self, unit):
    #Scaling nodal dimensions as Young Modulus E change (it is a trick rather)
        for e in self.edict:
            self.edict[e][5] = self.edict[e][5] * (units[unit] ** 2)
        print("Unit system changed to", "[" + str(unit) + "]")
        self.unit = unit

    def set_scale(self, scale):
    #Scaling nodal dimensions as Young Modulus E change
        #for e in self.edict:
        #    self.edict[e][8] = self.edict[e][8] * (scale ** 2)
        print("Standard nodal dimension set to", "[" + str(scale) + " " + self.unit+ "]")
        self.scale = scale

    def get_unit(self):
        return [self.unit, self.scale]
        
    def get_prop(self, mnum):
        return [self.mat[mnum][0] * (units[self.unit] ** 2), self.mat[mnum][1], self.mat[mnum][2], self.mat[mnum][3]]

class thicks():
#Class contains elements thicknesses
    def __init__(self, edict, mats):
        self.edict = edict
        self.hnum = 0
        self.hdict = {}
        self.unit, self.scale = mats.get_unit()

    def add(self, thickness):
    #Add thickness and property number 
        self.hnum += 1
        self.hdict[self.hnum] = [thickness]

    def assignall(self, hnum):
    #Assign prevoiusly added thickness property to all elements
        for e in self.edict:
            self.edict[e][7] = self.hdict[hnum][0]# * self.scale
        print("Thickness of all eles set to", 
              "[" + str(self.hdict[hnum][0]) + " " + self.unit + "]")
        return self.edict

    def assignlist(self, elist, hnum):
    #Assign prevoiusly added thickness property to list of elements
        for e in elist:
            self.edict[e][7] = self.hdict[hnum][0]
        return self.edict

    def info(self):
    #Prints thickness list
        print("# thicknesses info")
        #print("hnum", ":", "value")
        for h in self.hdict:
            print("h" + str(h), ":", self.hdict[h][0])  
        print("")

class constraints():
#Class for creating boundaries
    def __init__(self):
        self.loads = {}
        self.supports = {}
        self.cdict = {}

    def support(self, nlist, x = 0, y = 0):
    #Add a constraint in node
        for n in nlist:
            if x == 0:
                self.supports[(n * 2) - 2] = 0
            if y == 0:
                self.supports[(n * 2) - 1] = 0
        self.cdict.update(self.supports)
        return self.cdict  

    def load(self, nlist, x = 0, y = 0):
    #Add nodal load
        force_xcount, force_ycount = 0, 0
        #Need to create unique entries only list
        nlist = list(set(nlist))
        for n in nlist:
            if x != 0:
                self.loads[(n * 2) - 2] = (x / len(nlist))
                force_xcount += 1
            if y != 0:
                self.loads[(n * 2) - 1] = (y / len(nlist))
                force_ycount += 1
        self.cdict.update(self.loads)
        print("Applied force vector",
              "(" + "%.1e" % x + " N, " + "%.1e" % y +" N)", 
              "distributed to", 
              "[" + str(max([force_xcount, force_ycount])) + "]", 
              "nodes")
        return self.cdict

    def store(self):
    #Just returns dict of constraints
        return self.cdict

    def info(self):
    #Prints constraints dict
        print("# boundary conditions info")
        print("{dof : value, ...}")
        print(self.cdict) 
        print("")

    def short_info(self):
        print("# boundary conditions info")
        print(self.cdict) 