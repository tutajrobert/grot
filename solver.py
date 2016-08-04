import gauss, numpy

class build():
  def __init__(self, nodes, elements, constraints):
    self.nodes = nodes
    self.eles = elements
    self.cons = constraints
    self.gklist = []
    self.clist = []
    self.flist = []

    zerolist = []
    for i in range(len(self.nodes) * 2):
      zerolist.append(0)
    for i in range(len(self.nodes) * 2):
      self.gklist.append(list(zerolist))
      self.clist.append(0)
    
    for e in self.eles:
      ele = self.eles[e]  
      
      """xs, ys = [], []
      
      for i in range(0, 4):
        xs.append(ele[i][0])
        ys.append(ele[i][1])
        
      a = max(xs) - min(xs)
      b = max(ys) - min(ys)"""
      
      E = ele[8]
      v = ele[9]
      h = ele[10]
      
      G = E / (2 * (1 + v))
      
      dof1 = (ele[4] * 2) - 2
      dof2 = (ele[5] * 2) - 2
      dof3 = (ele[6] * 2) - 2
      dof4 = (ele[7] * 2) - 2
      dofs = [dof1, dof1 + 1, dof2, dof2 + 1, dof3, dof3 + 1, dof4, dof4 + 1]      
      
      p = (E * h) / (12 * (1 - (v ** 2)))
      
      k11 = p * 2 * (3 - v)
      k22, k33, k44, k55, k66, k77, k88 = k11, k11, k11, k11, k11, k11, k11
      k15 = p * 1.5 * (1 - v)
      k27, k36, k48, k72, k63, k84, k51 = k15, k15, k15, k15, k15, k15, k15
      k16 = p * 1.5 * (1 - (3 * v))
      k28, k35, k47, k82, k53, k74, k61 = k16, k16, k16, k16, k16, k16, k16
      k17 = p * (-1.5) * (1 - (3 * v))
      k25, k38, k46, k52, k83, k64, k71 = k17, k17, k17, k17, k17, k17, k17
      k18 = p * (-1.5) * (1 - v)
      k26, k37, k45, k62, k73, k54, k81 = k18, k18, k18, k18, k18, k18, k18
      k12 = p * 2 * v
      k34, k21, k43 = k12, k12, k12
      k13 = p * (-3 - v)
      k31, k24, k42 = k13, k13, k13
      k14 = p * (-3 + v)
      k41, k23, k32 = k14, k14, k14
      k56 = p * (-3 - v)
      k65, k78, k87 = k56, k56, k56
      k57 = p * 2 * v
      k75, k68, k86 = k57, k57, k57
      k58 = p * (-3 + v)
      k85, k67, k76 = k58, k58, k58
      
      klist = [[k11, k12, k13, k14, k15, k16, k17, k18],
               [k21, k22, k23, k24, k25, k26, k27, k28],
               [k31, k32, k33, k34, k35, k36, k37, k38],
               [k41, k42, k43, k44, k45, k46, k47, k48],
               [k51, k52, k53, k54, k55, k56, k57, k58],
               [k61, k62, k63, k64, k65, k66, k67, k68],
               [k71, k72, k73, k74, k75, k76, k77, k78],
               [k81, k82, k83, k84, k85, k86, k87, k88]]
      
      for i in range(8):
        for j in range(8):
          self.gklist[dofs[i]][dofs[j]] += klist[i][j]
  
    for c in self.cons:
      if self.cons[c] != 0:
        self.clist[c] = self.cons[c]
      elif self.cons[c] == 0:
        self.gklist[c] = list(zerolist)
        for i in range(len(zerolist)):
          self.gklist[i][c] = 0
        self.gklist[c][c] = 1
    #self.gklist = numpy.array(self.gklist)
    #self.clist = numpy.array(self.clist)  

  def gauss_linear(self):
    """for i in range(len(self.clist)):
      self.gklist[i].append(self.clist[i])
    self.dlist = gauss.eliminate(self.gklist)
    return self.dlist"""
    self.dlist = numpy.linalg.solve(self.gklist, self.clist)        
    if numpy.allclose(numpy.dot(self.gklist, self.dlist), self.clist) == True:
      return self.dlist

  """def least_squares(self):           
    self.dlist = numpy.linalg.lstsq(self.gklist, self.clist)        
    return self.dlist[0]"""
