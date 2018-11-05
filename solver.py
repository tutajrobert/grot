import numpy
import scipy.sparse
import scipy.sparse.linalg
import sys
import math
import time

class build():
    def __init__(self, nodes, elements, constraints, state, load_inc):
        self.nodes = nodes
        self.eles = elements
        self.cons = constraints
        self.counter = 0
        self.state = state

        #Preparing global stiffnes matrix initially filled with zeros
        self.clist = numpy.zeros(len(self.nodes) * 2)
        self.gklist = scipy.sparse.lil_matrix((len(self.nodes) * 2, len(self.nodes) * 2))

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
                    self.gklist[dofs[i], dofs[j]] += klist[i][j]
        
        """
        Application of constraints:
        for forces (value != 0) direct entry into forces matrix
        for supports (value == 0) apply procedure of installation of the homogeneous bc
            set row c in gklist to 0
            set column c in gklist to 0
            set diagonal elements c in gklist to 1
            set element c in flist to 0
        """
        
        print("")
        print("Built", "[" + str(len(self.nodes) * 2), "x", 
              str(len(self.nodes) * 2) + "]", "matrix")
        
        klist = None
        
        prog_counter = 0
        for c in self.cons:
            #Progress text in percents
            prog_counter += 1
            sys.stdout.write("\r" + 
            "Applying Dirichlet boundary conditions [" + 
            str(round(((prog_counter) / len(self.cons)) * 100, 2)) + 
            " %]")
            sys.stdout.flush()
            
            if self.cons[c] != 0:
                self.clist[c] = self.cons[c] * load_inc
            elif self.cons[c] == 0:
                self.gklist[c, :] = 0
                self.gklist[:, c] = 0
                self.gklist[c, c] = 1
        self.gklist = self.gklist.tocsr()
        print("")
        
        self.cons = None
        
    def direct(self):
    #Solve linear equations system built above with direct method
        print("")
        print("Solving... (this may take a while)")
        self.dlist = scipy.sparse.linalg.spsolve(self.gklist, self.clist)
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
                     [0, 0, fc * ((1 - v)/ 2)]])
                     
            stresses.append(numpy.dot(slist, strains[counter]))
        principals_stress = []
        for i in range(len(self.eles)):        
            princ_1 = 0.5 * (stresses[i][0] + stresses[i][1]) + math.sqrt(((0.5 * (stresses[i][0] - stresses[i][1])) ** 2) + stresses[i][2] ** 2)
            princ_2 = 0.5 * (stresses[i][0] + stresses[i][1]) - math.sqrt(((0.5 * (stresses[i][0] - stresses[i][1])) ** 2) + stresses[i][2] ** 2)
            tau_max = 0.5 * (princ_1 - princ_2)
            if stresses[i][0] == stresses[i][1]:
                theta_princ = 0
            else:
                theta_princ = 0.5 * numpy.arctan((2 * stresses[i][2]) / (stresses[i][0] - stresses[i][1]))
            principals_stress.append([princ_1, princ_2, tau_max, theta_princ])

        principals_strains = []
        for i in range(len(self.eles)):        
            princ_1 = 0.5 * (strains[i][0] + strains[i][1]) + math.sqrt(((0.5 * (strains[i][0] - strains[i][1])) ** 2) + strains[i][2] ** 2)
            princ_2 = 0.5 * (strains[i][0] + strains[i][1]) - math.sqrt(((0.5 * (strains[i][0] - strains[i][1])) ** 2) + strains[i][2] ** 2)
            tau_max = 0.5 * (princ_1 - princ_2)
            if strains[i][0] == strains[i][1]:
                theta_princ = 0
            else:
                theta_princ = 0.5 * numpy.arctan((2 * strains[i][2]) / (strains[i][0] - strains[i][1]))
            principals_strains.append([princ_1, princ_2, tau_max, theta_princ])
        print("Calculated strain and stress tensors (reduced 1-point integration)")
        print("")
        
        return(strains, stresses, principals_stress, principals_strains)

        #STRUCTURE OF SOLVER'S RESULTS RETURN CALL:
            #disp_results: long vector of disp results in form of [x1, y1, x2, y2, x3, y3, x4, y4...]
            
            #stress_results: [strains, stresses, principal_stress, principal_strains]
                #strains: elemental results in form of lists [l1, l2, l3, l4, l5, l6, l7, l8...]
                #stresses elemental results in form of lists [l1, l2, l3, l4, l5, l6, l7, l8...]
                #principal stresses elemental results in form of lists [l1, l2, l3, l4, l5, l6, l7...]
                #principal strains elemental results in form of lists [l1, l2, l3, l4, l5, l6, l7...]
                    #all above lists are in form [rx, ry, rxz] or [r1, r2, r12max, rangle]
             
                #in short: res[0][60][2] is strains, element number 60, xy value of strain 