"""Solver module"""

import math
import sys
import numpy
import scipy.sparse
import scipy.sparse.linalg

class Build():
    """Big class. To build, update, solve, alter and postprocess stiffness matrix and results
    STRUCTURE OF SOLVER'S RESULTS RETURN CALL:
    disp_results: long vector of disp results in form of [x1, y1, x2, y2, x3, y3, x4, y4...]
    stress_results: [strains, stresses, principal_stress, principal_strains]
        strains: elemental results in form of lists [l1, l2, l3, l4, l5, l6, l7, l8...]
        stresses elemental results in form of lists [l1, l2, l3, l4, l5, l6, l7, l8...]
        principal stresses elemental results in form of lists [l1, l2, l3, l4, l5, l6, l7...]
        principal strains elemental results in form of lists [l1, l2, l3, l4, l5, l6, l7...]
        all above lists are in form [rx, ry, rxz] or [r1, r2, r12max, rz, reff, rangle]
    in short: res[0][60][2] is strains, element number 60, xy value of strain"""

    def __init__(self, nnum, elements, constraints, state, load_inc, scale):
        self.nnum = nnum
        self.eles = elements
        self.cons = constraints
        self.state = state
        self.scale = scale
        self.counter = 0
        self.dlist = []

        #Preparing global stiffnes matrix initially filled with zeros
        self.clist = numpy.zeros(self.nnum * 2)
        self.gklist = scipy.sparse.lil_matrix((self.nnum * 2, self.nnum * 2))

        #For every element of model calculating: kirchhoff modulus G, ele stiffnes matrix klist
        print("")

        for e in self.eles:
            self.counter += 1
            #Progress text in percents
            sys.stdout.write("\r" + "Building global stiffnes matrix [" + \
                             str(round(((self.counter) / len(self.eles)) * 100, 1)) + " %]")
            sys.stdout.flush()

            #Element material parameters
            ele = self.eles[e]
            E = ele[5]
            v = ele[6]
            h = ele[7]
            #For plane strain
            if self.state == "planestrain":
                E = E / (1 - (v**2))
                v = v / (1 - v)

            dofs = self.dofs_org(ele)

            klist = self.stiff_matrix(E, v, h)
            #Aggregation of global stiffnes matrix gklist
            for i in range(8):
                for j in range(8):
                    self.gklist[dofs[i], dofs[j]] += klist[i][j]
        size = str(2 * self.nnum)
        print("\nBuilt", "[" + size, "x", size + "]", "matrix")
        klist = None
        self.constraints_apply(load_inc)
        print("Applied Dirichlet boundary conditions")

    @staticmethod
    def stiff_matrix(E, v, h):
        """Element stiffness element preparation"""
        p = (E * h) / (12 * (1 - (v ** 2)))
        q = (E * h) / (1 - v)
        k11 = p * 2 * (3 - v)
        k15 = p * (-3 + v)
        k12 = q / 8
        k16 = -k12
        k17 = p * 2 * v
        k18 = p * 1.5 * (1 - (3 * v))
        k13 = p * (-3 - v)
        k14 = -k18

        #Element stiffnes matrix
        klist = numpy.array([[k11, k12, k13, k14, k15, k16, k17, k18],
                             [k12, k11, k18, k17, k16, k15, k14, k13],
                             [k13, k18, k11, k16, k17, k14, k15, k12],
                             [k14, k17, k16, k11, k18, k13, k12, k15],
                             [k15, k16, k17, k18, k11, k12, k13, k14],
                             [k16, k15, k14, k13, k12, k11, k18, k17],
                             [k17, k14, k15, k12, k13, k18, k11, k16],
                             [k18, k13, k12, k15, k14, k17, k16, k11]])
        return klist

    @staticmethod
    def dofs_org(ele):
        """Degree of freedoms are in unknown order, thus needed lines below"""
        dof1 = (ele[1] * 2) - 2
        dof2 = (ele[2] * 2) - 2
        dof3 = (ele[3] * 2) - 2
        dof4 = (ele[4] * 2) - 2
        dofs = numpy.array([dof1, dof1 + 1, dof2, dof2 + 1, dof3, dof3 + 1, dof4, dof4 + 1])
        return dofs

    def constraints_apply(self, load_inc):
        """Constraints application procedure"""
        #Application of constraints:
        #for forces (value != 0) direct entry into forces matrix
        #for supports (value == 0) apply procedure of installation of the homogeneous bc
            #set row c in gklist to 0
            #set column c in gklist to 0
            #set diagonal elements c in gklist to 1
            #set element c in flist to 0
        for c in self.cons:
            if self.cons[c] != 0:
                self.clist[c] = self.cons[c] * load_inc
            elif self.cons[c] == 0:
                self.gklist[c, :] = 0
                self.gklist[:, c] = 0
                self.gklist[c, c] = 1

    def direct(self):
        """Solves linear equations system with direct method. Returns displacements"""
        print("\nSolving... (this may take a while)")
        self.dlist = scipy.sparse.linalg.spsolve(self.gklist.tocsr(), self.clist)
        self.gklist, self.clist = None, None
        print("Succesfully and directly solved system of linear equations")
        return self.dlist

    def strains_calc(self, disp_res, msg=1):
        """Reduced integration for strains"""
        sc = self.scale
        #43
        #12
        #eta --++
        #dzeta +--+
        eta = 1 / math.sqrt(3)
        dzeta = 1 / math.sqrt(3)
        etas = [eta, -eta]
        dzetas = [dzeta, -dzeta]
        #Shape function
        def shapefunc(eta, dzeta):
            blist = numpy.array([[.5*(1-eta)/sc, -.5*(1-eta)/sc, -.5*(1+eta)/sc, .5*(1+eta)/sc, 0, 0, 0, 0],
                                [0, 0, 0, 0, -.5*(1+dzeta)/sc, -.5*(1-dzeta)/sc, .5*(1-dzeta)/sc, .5*(1+dzeta)/sc],
                                [-.5*(1+dzeta)/sc, -.5*(1-dzeta)/sc, .5*(1-dzeta)/sc, .5*(1+dzeta)/sc, 
                                 .5*(1-eta)/sc, -.5*(1-eta)/sc, -.5*(1+eta)/sc, .5*(1+eta)/sc]])
            return blist
        
        strains = []
        #Displacement results storing reorganization
        for i in self.eles:
            dofs = self.dofs_org(self.eles[i])
            disp_list = numpy.array([disp_res[dofs[2]], disp_res[dofs[0]],
                                     disp_res[dofs[6]], disp_res[dofs[4]],
                                     disp_res[dofs[3]], disp_res[dofs[1]],
                                     disp_res[dofs[7]], disp_res[dofs[5]]])

            #Strains calculation
            strains_gauss = [[], [], [], []]
            gauss_counter = 0
            for eta in etas:
                for dzeta in dzetas:
                    strains_gauss[gauss_counter].append(numpy.dot(shapefunc(eta, dzeta), numpy.matrix.transpose(disp_list)))
                    gauss_counter += 1
            #print(strains_gauss[0][0] + strains_gauss[1][0])
            strains.append(.25*(strains_gauss[0][0] + strains_gauss[1][0] + strains_gauss[2][0] + strains_gauss[3][0]))

        #Reduced integration for stresses
        stresses = []
        counter = -1 #counter for synchronize with strains
        for i in self.eles:
            counter += 1
            E = self.eles[i][5]
            v = self.eles[i][6]
            fc = E / (1 - (v ** 2))
            #Constitutive matrix
            slist = numpy.array([[fc, fc * v, 0],
                                 [fc * v, fc, 0],
                                 [0, 0, fc * ((1 - v)/ 2)]])
            stresses.append(numpy.dot(slist, strains[counter]))

        def zdir(i):
            """Additional Z direction strains and stress analytical calculation"""
            eps_x = strains[i][0]
            eps_y = strains[i][1]
            eps_xy = strains[i][2]
            if self.state == "planestress":
                eps_z = (stresses[i][0] + stresses[i][1]) * -v / E
                sig_z = 0
            elif self.state == "planestrain":
                eps_z = 0
                sig_z = (E / (1 - (v**2))) * (eps_x + eps_z) * -v
            eff_strain = (1 / (math.sqrt(2) * (1 + v))) * \
                         math.sqrt(((eps_x - eps_y)**2 + (eps_y - eps_z)**2 + \
                                    (eps_z - eps_x)**2) + ((3/2)*(eps_xy**2)))
            return [eps_z, sig_z, eff_strain]

        def principals(st):
            """Principal stress and strain in 2D problem (3D in reality, so small error here)"""
            part1 = 0.5 * (st[i][0] + st[i][1])
            part2 = math.sqrt(((0.5 * (st[i][0] - st[i][1])) ** 2) + st[i][2] ** 2)
            princ_1 = part1 + part2
            princ_2 = part1 - part2
            tau_max = 0.5 * (princ_1 - princ_2)
            if st[i][0] == st[i][1]:
                theta_princ = 0
            else:
                theta_princ = 0.5 * numpy.arctan((2 * st[i][2]) / (st[i][0] - st[i][1]))
            return [princ_1, princ_2, tau_max, theta_princ]

        misc_stresses = [] #miscelanous stresses: principals and angle, Z direction
        misc_strains = [] #miscelanous strains: principals and angle, effective, Z direction
        for i in range(len(self.eles)):
            zres = zdir(i)
            sig_z = zres[1]
            eps_z, eff_strain = zres[0], zres[2]
            princ = principals(stresses)
            misc_stresses.append([princ[0], princ[1], princ[2], sig_z, 0, princ[3]])
            princ = principals(strains)
            misc_strains.append([princ[0], princ[1], princ[2], eps_z, eff_strain, princ[3]])

        if msg == 1:
            print("Calculated strain and stress tensors (reduced 1-point integration)")
        return([strains, stresses, misc_stresses, misc_strains])
