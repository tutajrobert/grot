from mlib import *

ndict = {}
	
class nodes():
  #Class contains total number of nodes in nnum and node properties dict ndict
  def __init__(self):
    self.ndict = {}
    self.nnum = 0    

  def add(self, x, y):
  #Adds a node of x, y coordinates as a dictionary item with key of node number
    self.nnum += 1
    self.ndict[self.nnum] = [x, y]
    #ndict = self.ndict 
    return self.ndict
    
  def addlist(self, nlist):
  #Adds a list of nodes the same manner as add function above
    for n in nlist:
      self.nnum += 1
      self.ndict[self.nnum] = [n[0], n[1]]
    #ndict = self.ndict
    return self.ndict

  def check(self, coord):
    for n in self.ndict:
      if self.ndict[n] == coord
        return n
      else:
        return None

  def info(self):
  #Prints number of nodes and nodes dict
    print("# NODES info")
    print("Total number of nodes: " + str(self.nnum))
    print("nnum", ":", "[xcoord, ycoord]")
    for n in self.ndict:
      print("n" + str(n), ":", self.ndict[n])
    print("")

class elements():
  #Class contains total number of elements in enum and element properties dict edict
  def __init__(self, ndict):
    self.edict = {}
    self.enum = 0
    self.ndict = ndict
    
  def add(self, n1, n2, n3, n4):
  #Adds four nodes rectangle element. Takes nodes dictionaries and nodes elements
    self.enum += 1
    self.edict[self.enum] = [self.ndict[n1], self.ndict[n2], self.ndict[n3], self.ndict[4], n1, n2, n3, n4]
    return self.edict
    
  def addlist(self, elist):
  #Adds a list of elements the same manner as add function above
    for e in elist:
      self.enum += 1
      self.edict[self.enum] = [self.ndict[e[0]], self.ndict[e[1]], self.ndict[e[2]], self.ndict[e[3]], e[0], e[1], e[2], e[3]]
    return self.edict
    
  def info(self):
  #Prints number of elements and elements list
    print("# ELEMENTS info")
    print("Total number of elements: " + str(self.enum))
    print("enum", ":", "[n1, n2, n3, n4]")
    for e in self.edict:
      print("e" + str(e), ":", self.edict[e][4:8])
    print("")
    
  def infoall(self):
    print(self.edict)

class materials():
  def __init__(self, edict):
    #Class contains materials data and element to which materials are assigned
    self.edict = edict
    self.mnum = 0
    self.mat = {}
    self.mnames = {}
  
  def add(self, name):
  #Adds material by name to prep from mlib.py
    self.mnum += 1
    self.mat[self.mnum] = mdict()[name]
    self.mnames[self.mnum] = name
  
  def assignall(self, mnum):
  #Assign added material to all elements
    for e in self.edict:
      self.edict[e].append(self.mat[mnum][0])
      self.edict[e].append(self.mat[mnum][1])
    return self.edict
    
  def info(self):
  #Prints material list
    print("# MATERIALS info")
    print("mnum mname", ":", "E, v")
    for m in self.mat:
      print("m" + str(m), self.mnames[m], ":", round(self.mat[m][0] / 1e9, 2), "e+9,", round(self.mat[m][1], 2))  
    print("")

class thicks():
  #Class contains elements thicknesses
  def __init__(self, edict):
    self.edict = edict
    self.hnum = 0
    self.hdict = {}
    
  #Add thickness and property number  
  def add(self, thickness):
    self.hnum += 1
    self.hdict[self.hnum] = [thickness]
    
  def assignall(self, hnum):
    for e in self.edict:
      self.edict[e].append(self.hdict[hnum][0])
    return self.edict
   
  def assignsingle(self, enum, hnum):
    self.edict[enum].append(self.hdict[hnum][0])
    return self.edict
    
  def assignlist(self, elist, hnum):
    for e in elist:
      self.edict[e].append(self.hdict[hnum])
    return self.edict
    
  def info(self):
  #Prints thickness list
    print("# THICKNESSES info")
    print("hnum", ":", "value")
    for h in self.hdict:
      print("h" + str(h), ":", self.hdict[h])  
    print("")    

class constraints():
  def __init__(self):
    self.loads = {}
    self.supports = {}
    self.cdict = {}
  
  def support(self, nlist, x = 0, y = 0):
    for n in nlist:
      if x == 0:
        self.supports[(n * 2) - 2] = 0
      if y == 0:
        self.supports[(n * 2) - 1] = 0
    self.cdict.update(self.supports)
    return self.cdict  
      
  def load(self, nlist, x = 0, y = 0):
    for n in nlist:
      if x != 0:
        self.loads[(n * 2) - 2] = x
      if y != 0:
        self.loads[(n * 2) - 1] = y
    self.cdict.update(self.loads)
    return self.cdict
    
  def info(self):
  #Prints constraints dict
    print("# BOUNDARY CONDITIONS info")
    print("{dof : value, ...}")
    print(self.cdict) 
    print("")            
