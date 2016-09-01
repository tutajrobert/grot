import numpy.linalg

class build():
    def __init__(self, nodes, elements, constraints):
        self.nodes = nodes
        self.eles = elements
        self.cons = constraints
        self.gklist = [] #global stiffnes matrix
        self.clist = [] #constraints list
        self.flist = [] #forces matrix (right)

        #Preparing global stiffnes matrix initially filled with zeros
        zerolist = []
        for i in range(len(self.nodes) * 2):
            zerolist.append(0)
        for i in range(len(self.nodes) * 2):
            self.gklist.append(list(zerolist))
            self.clist.append(0)
    
        """
        For every element of model calculating:
        kirchhoff modulus G
        ele stiffnes matrix klist      
        """
        
        for e in self.eles:
            ele = self.eles[e]  
      
            E = ele[8]
            v = ele[9]
            h = ele[10]
      
            G = E / (2 * (1 + v))
      
            #Degree of freedoms are in unknown order, thus needed lines below
            dof1 = (ele[4] * 2) - 2
            dof2 = (ele[5] * 2) - 2
            dof3 = (ele[6] * 2) - 2
            dof4 = (ele[7] * 2) - 2
            dofs = [dof1, dof1 + 1, dof2, dof2 + 1, dof3, dof3 + 1, dof4, dof4 + 1]      
      
            #Global stiffness element preparation
            p = (E * h) / (12 * (1 - (v ** 2)))
            q = (E * h) / (1 - v)
    
            k11 = p * 2 * (3 - v)
            k22, k33, k44, k55, k66, k77, k88 = k11, k11, k11, k11, k11, k11, k11
    
            k15 = p * (-3 + v)
            k62, k51, k26, k37, k73, k48, k84 = k15, k15, k15, k15, k15, k15, k15
    
            k12 = q / 8
            k74, k21, k83, k65, k56, k47, k38 = k12, k12, k12, k12, k12, k12, k12
    
            k16 = -q / 8
            k61, k52, k25, k43, k34, k87, k78 = k16, k16, k16, k16, k16, k16, k16    
    
            k17 = p * 2 * v
            k71, k42, k24, k35, k53, k86, k68 = k17, k17, k17, k17, k17, k17, k17
    
            k18 = p * 1.5 * (1 - (3 * v))
            k23, k32, k45, k67, k76, k54, k81 = k18, k18, k18, k18, k18, k18, k18
        
            k13 = p * (-3 - v)
            k31, k28, k46, k57, k64, k75, k82 = k13, k13, k13, k13, k13, k13, k13

            k14 = p * 1.5 * (-1 + (3 * v))
            k41, k63, k72, k85, k58, k36, k27 = k14, k14, k14, k14, k14, k14, k14
      
            klist = [[k11, k12, k13, k14, k15, k16, k17, k18],
                     [k21, k22, k23, k24, k25, k26, k27, k28],
                     [k31, k32, k33, k34, k35, k36, k37, k38],
                     [k41, k42, k43, k44, k45, k46, k47, k48],
                     [k51, k52, k53, k54, k55, k56, k57, k58],
                     [k61, k62, k63, k64, k65, k66, k67, k68],
                     [k71, k72, k73, k74, k75, k76, k77, k78],
                     [k81, k82, k83, k84, k85, k86, k87, k88]]
      
            #Aggregation of global stiffnes matrix gklist
            for i in range(8):
                for j in range(8):
                    self.gklist[dofs[i]][dofs[j]] += klist[i][j]
        
        """
        Application of constraints:
        for forces (value != 0) direct entry into forces matrix
        for supports (value == 0) apply procedure of installation of the homogeneous bc
            set row c in gklist to 0
            set column c in gklist to 0
            set diagonal elements c in gklist to 1
            set element c in flist to 0
        """
        
        for c in self.cons:
            if self.cons[c] != 0:
                self.clist[c] = self.cons[c]
            elif self.cons[c] == 0:
                self.gklist[c] = list(zerolist)
                for i in range(len(zerolist)):
                    self.gklist[i][c] = 0
                self.gklist[c][c] = 1

        print("Built", len(self.gklist[0]), "x", 
              len(self.gklist[0]), "global stiffnes matrix")

    def direct(self):
    #Solve linear equations system built above with direct method
        self.dlist = numpy.linalg.solve(self.gklist, self.clist)
        print("Succesfully calculated nodal displacements")
        return self.dlist

    def least_squares(self):
    #Solve linear equations system built above with iterative least squares method
        self.dlist = numpy.linalg.lstsq(self.gklist, self.clist)        
        return self.dlist[0]