"""Iterative procedure of plasticity module"""

import stress

CRITERIUM = "huber"

def search(eles, strains, flags_list):
    """Checks if element in plastic"""
    criterium = "huber"
    elist = []

    for enum in range(1, len(eles)):
        plast_value = eles[enum][11]
        if enum not in flags_list:
            value = stress.results(strains, criterium, enum - 1)
            if value is not None:
                if value[0] >= plast_value:
                    elist.append(enum)
                    flags_list.append(enum)
    return [elist, flags_list]

class Prepare():
    def __init__(self, disp, strains, eles):
        self.disp = disp
        self.strains = strains
        self.eles = eles
        self.pstrains = []
        for j in range(len(self.strains[0])):
            self.pstrains.append([])
            for k in range(7):
                self.pstrains[j].append(0)
            self.pstrains[j][2] += stress.results(strains, "eff_strain", (j))[0]

    def out(self):
        pstrains_eff = []
        for j in range(len(self.strains[0])):
            if pstrains_eff != 0:
                pstrains_eff.append(self.pstrains[j][0])
        return [self.disp, self.strains, pstrains_eff]

    def store(self, material, disp, strains, flags_list):
        self.disp += disp
        for i in range(len(self.strains)):
            for j in range(len(self.strains[i])):
                for k in range(len(self.strains[i][j])): #5. is princ angle, not to be scaled
                    if k < 5:
                        self.strains[i][j][k] += strains[i][j][k]
        for j in range(len(self.pstrains)):
            self.pstrains[j][2] += stress.results(strains, "eff_strain", (j))[0]
        for j in range(len(self.pstrains)):
            if j + 1 in flags_list:
                value = stress.results(strains, "eff_strain", (j))[0]
                self.pstrains[j][0] += value
                value *= material.get_prop(1)[3] * material.get_prop(1)[0]
                self.pstrains[j][1] += value
                self.pstrains[j][3] += strains[0][j][0]
                self.pstrains[j][4] += strains[0][j][1]
                self.pstrains[j][5] += strains[0][j][2]
                self.pstrains[j][6] += stress.results(strains, "eps_z", (j))[0]
        return [self.disp, self.strains]

    def residual_disp(self, disp_el):
        """Residual displacement equals to total disp minus elastic disp. Rather trick"""
        res_disp = []
        for i in range(len(self.disp)):
            res_disp.append(self.disp[i] - disp_el[i])
        return res_disp

    def residual_strains(self, strains_el):
        """Residual strains equals to total strains minus elastic strains. Rather trick
        There is a possibility that it is not in confirmity with tensorial rules"""
        for i in range(len(strains_el)):
            for j in range(len(strains_el[i])):
                for k in range(len(self.strains[i][j])): #5. is princ angle, not to be scaled
                    if k < 5:
                        strains_el[i][j][k] = self.strains[i][j][k] - strains_el[i][j][k]
        return strains_el

    def store_plstrain(self, strains):
        """Cumulate plastic strains to total strains"""
        strains.append(self.pstrains)
        return strains

    def halfstep(self, strains):
        """Cumulate strains in a halfstep"""
        for i in range(len(self.strains)):
            for j in range(len(self.strains[i])):
                for k in range(len(self.strains[i][j])): #5. is princ angle, not to be scaled
                    if k < 5:
                        strains[i][j][k] = self.strains[i][j][k] + strains[i][j][k]
        return strains

    def first_step(self, material):
        """Scaling load increment to achieve first plastic strain"""
        limit = material.get_prop(1)[2]
        values = []

        for enum in range(1, len(self.strains[1])):
            value = stress.results(self.strains, CRITERIUM, enum)
            values.append(value[0])
        max_value = max(values)

        if max_value <= limit:
            return limit / max_value
        factor = (limit / max_value) * 1.0
        self.disp *= factor

        for i in range(len(self.strains)):
            for j in range(len(self.strains[i])):
                for k in range(len(self.strains[i][j])): #5. is princ angle, not to be scaled
                    if k < 5:
                        self.strains[i][j][k] *= factor
        for j in range(len(self.strains[i])):
            self.pstrains[j][2] *= factor
        return factor
