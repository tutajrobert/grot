import stress, numpy
criterium = "huber"
    
class prepare():
    def __init__(self, disp, strains, eles):
        self.disp = disp
        self.strains = strains
        self.eles = eles
        self.pstrains = []
        for j in range(len(self.strains[0])):
            self.pstrains.append([])
            for k in range(7):
                self.pstrains[j].append(0)
            E = self.eles[j + 1][8]
            v = self.eles[j + 1][9]
            self.pstrains[j][2] += stress.results(strains, "eff_strain", (j), E, v)[0]
            
    def out(self):
        pstrains_eff = []
        for j in range(len(self.strains[0])):
            if pstrains_eff != 0:
                pstrains_eff.append(self.pstrains[j][0])
        return [self.disp, self.strains, pstrains_eff]
    def store(self, material, disp, strains, flags_list):
        #print("Store")
        self.disp += disp
        for i in range(len(self.strains)):
            for j in range(len(self.strains[i])):
                for k in range(len(self.strains[i][j])): #the 5. is principal angle, not to be scaled
                    if k < 5:
                        self.strains[i][j][k] += strains[i][j][k]
        for j in range(len(self.pstrains)):      
            E = self.eles[j + 1][8]
            v = self.eles[j + 1][9]
            self.pstrains[j][2] += stress.results(strains, "eff_strain", (j), E, v)[0]
        for j in range(len(self.pstrains)):
            if (j + 1) in flags_list:
                E = material.get_prop(1)[3] * material.get_prop(1)[0]
                v = .5
                value = stress.results(strains, "eff_strain", (j), E, v)[0]
                self.pstrains[j][0] += value    
                value *= material.get_prop(1)[3] * material.get_prop(1)[0]
                self.pstrains[j][1] += value
                
                self.pstrains[j][3] += strains[0][j][0]
                self.pstrains[j][4] += strains[0][j][1]
                self.pstrains[j][5] += strains[0][j][2]
                self.pstrains[j][6] += stress.results(strains, "eps_z", (j), E, v)[0]
        return [self.disp, self.strains]
    def residual_disp(self, disp_el):
        res_disp = []
        for i in range(len(self.disp)):
            res_disp.append(self.disp[i] - disp_el[i])
        #(res_disp)
        return res_disp
    def residual_strains(self, strains_el):
       for i in range(len(strains_el)):
            for j in range(len(strains_el[i])):
                for k in range(len(self.strains[i][j])): #the 5. is principal angle, not to be scaled
                    if k < 5:
                        strains_el[i][j][k] = self.strains[i][j][k] - strains_el[i][j][k]
       return strains_el
    def store_plstrain(self, strains):
        strains.append(self.pstrains)
        return strains
    
    def halfstep(self, strains):
        #print("Half")
        for i in range(len(self.strains)):
            for j in range(len(self.strains[i])):
                for k in range(len(self.strains[i][j])): #the 5. is principal angle, not to be scaled
                    if k < 5:
                        strains[i][j][k] = self.strains[i][j][k] + strains[i][j][k]

        return strains
        
    def first_step(self, material):
        limit = material.get_prop(1)[2]
        E = material.get_prop(1)[0]
        v = material.get_prop(1)[1]
        values = []
        
        for enum in range(1, len(self.strains[1])):
            value = stress.results(self.strains, criterium, enum, E, v)
            values.append(value[0])
        max_value = max(values)

        if max_value <= limit:
            return limit / max_value
        else:
            factor = (limit / max_value) * 1.0
            
            self.disp *= factor
        
            for i in range(len(self.strains)):
                for j in range(len(self.strains[i])):
                    for k in range(len(self.strains[i][j])): #the 5. is principal angle, not to be scaled
                        if k < 5:
                            self.strains[i][j][k] *= factor
            for j in range(len(self.strains[i])):
                self.pstrains[j][2] *= factor
            return factor