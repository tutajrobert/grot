import numpy
import sys
import math

class build():
    def __init__(self, nodes, elements, constraints, state):
        self.nodes = nodes
        self.eles = elements
        self.cons = constraints
        self.counter = 0
        self.state = state

        #Preparing global stiffnes matrix initially filled with zeros
        zerolist = numpy.zeros(len(self.nodes) * 2)
        self.gklist = numpy.zeros((len(self.nodes) * 2, len(self.nodes) * 2))	
        self.clist = numpy.zeros(len(self.nodes) * 2)
        """
        For every element of model calculating:
        kirchhoff modulus G
        ele stiffnes matrix klist      
        """
        
        print("")
        
        for e in self.eles:
            self.counter += 1
        
            #Progress text in percents
            sys.stdout.write("\r" + 
            "Building global stiffnes matrix [" + 
            str(round(((self.counter) / len(self.eles)) * 100, 2)) + 
            " %]")
            sys.stdout.flush()
        
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
            dofs = numpy.array([dof1, dof1 + 1, dof2, dof2 + 1, dof3, dof3 + 1, dof4, dof4 + 1]) 
      
            #Global stiffness element preparation
			
            
            #For plane strain
            if self.state == "planestrain":
                E = E / (1 - (v**2))
                v = v / (1 - v)
            		
            p = (E * h) / (12 * (1 - (v ** 2)))
            q = (E * h) / (1 - v)
    
            k11 = p * 2 * (3 - v)
            k15 = p * (-3 + v)
            k12 = q / 8
            k16 = -q / 8
            k17 = p * 2 * v    
            k18 = p * 1.5 * (1 - (3 * v))        
            k13 = p * (-3 - v)
            k14 = p * 1.5 * (-1 + (3 * v))
      
            klist = numpy.array(
                     [[k11, k12, k13, k14, k15, k16, k17, k18],
                      [k12, k11, k18, k17, k16, k15, k14, k13],
                      [k13, k18, k11, k16, k17, k14, k15, k12],
                      [k14, k17, k16, k11, k18, k13, k12, k15],
                      [k15, k16, k17, k18, k11, k12, k13, k14],
                      [k16, k15, k14, k13, k12, k11, k18, k17],
                      [k17, k14, k15, k12, k13, k18, k11, k16],
                      [k18, k13, k12, k15, k14, k17, k16, k11]])
      
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
        
        klist = None
		
        for c in self.cons:
            if self.cons[c] != 0:
                self.clist[c] = self.cons[c]
            elif self.cons[c] == 0:
                self.gklist[c] = zerolist
                for i in range(len(zerolist)):
                    self.gklist[i][c] = 0
                self.gklist[c][c] = 1

        print("")
        print("Built", "[" + str(len(self.gklist[0])), "x", 
              str(len(self.gklist[0])) + "]", "matrix")
        #print("Storing reserved", "[" + str(round((len(self.gklist[0]) ** 2) * (sys.getsizeof(self.gklist[0][0]) / 1e6), 1)) + "]", "Mbytes of memory")
        print("Storing reserved", "[" + str(round((sys.getsizeof(self.gklist) / 1e6), 1)) + "]", "Mbytes of memory")
    
    def direct(self):
    #Solve linear equations system built above with direct method
        print("Solving... (this may take a while)")
        self.dlist = numpy.linalg.solve(self.gklist, self.clist)
        print(self.dlist.dtype)
        self.gklist, self.clist = None, None
        print("Succesfully and directly solved system of linear equations")
        return self.dlist

    def least_squares(self):
    #Solve linear equations system built above with iterative least squares method (really long)
        print("Solving... (this may take a while)")
        self.dlist = numpy.linalg.lstsq(self.gklist, self.clist)
        self.gklist, self.clist = None, None
        print("Succesfully calculated nodal displacements with least sqaures method [residual : " + str(self.dlist[1]) + "]")
        return self.dlist[0]
		
    def cholesky(self):
    #Solve linear equations system built above with cholesky decomposition method
        print("Decomposing global stiffness matrix using Cholesky method")
        L = numpy.linalg.cholesky(self.gklist)
        self.gklist = None
        LH = L.T.conj()
        print("Solving... (this may take a while)")
        y = numpy.linalg.solve(L, self.clist)
        L = None
        self.dlist = numpy.linalg.solve(LH, y)
        return self.dlist		

    def strains_calc(self, disp_res):
    #Reduced integration for strains

        blist = numpy.array(
                [[.5, -.5, -.5, .5, 0, 0, 0, 0],
                 [0, 0, 0, 0, -.5, -.5, .5, .5],
                 [-.5, -.5, .5, .5, .5, -.5, -.5, .5]])
        
        strains = []
        
        #Displacement results storing
        for i in self.eles:
            
            dof1 = (self.eles[i][4] * 2) - 2
            dof2 = (self.eles[i][5] * 2) - 2
            dof3 = (self.eles[i][6] * 2) - 2
            dof4 = (self.eles[i][7] * 2) - 2
            dofs = numpy.array(
                   [dof1, dof1 + 1, 
                    dof2, dof2 + 1, 
                    dof3, dof3 + 1, 
                    dof4, dof4 + 1])
            
            disp_list = numpy.array(
                        [disp_res[dofs[2]],
                         disp_res[dofs[0]],
                         disp_res[dofs[6]],
                         disp_res[dofs[4]],
                         disp_res[dofs[3]],
                         disp_res[dofs[1]],
                         disp_res[dofs[7]],
                         disp_res[dofs[5]]])
            
            strains.append(numpy.dot(blist, 
                    numpy.matrix.transpose(disp_list))
                )
        
        #Reduced integration for stresses
        stresses = []
        counter = -1 #counter for synchronize with strains
        
        for i in self.eles:
        
            counter += 1
            E = self.eles[i][8]
            v = self.eles[i][9]        
            fc = E / (1 - (v ** 2))
            
            slist = numpy.array(
                    [[fc, fc * v, 0],
                     [fc * v, fc, 0],
                     [0, 0, fc * ((1 - v) / 2)]])
                     
            stresses.append(numpy.dot(slist, strains[counter]))
        print("Calculated strain and stress tensors (reduced 1-point integration)")
        print("")
        
        return(strains, stresses)
