import stress, numpy
criterium = "huber"
limit = 235

def store(disp, strains):
    return None
    
class prepare():
    def __init__(self, disp, strains):
        self.disp = disp
        self.strains = strains
        #self.pstrains = pstrains

    def store(self, disp, strains):
        print("Store")
        self.disp += disp
        for i in range(len(self.strains)):
            for j in range(len(self.strains[i])):
                for k in range(3): #the 3. is principal angle, not to be scaled
                    self.strains[i][j][k] += strains[i][j][k]

        return [self.disp, self.strains]
        
    def halfstep(self, strains):
        print("Half")
        for i in range(len(self.strains)):
            for j in range(len(self.strains[i])):
                for k in range(3): #the 3. is principal angle, not to be scaled
                    strains[i][j][k] = self.strains[i][j][k] + strains[i][j][k]

        return strains
        
    def first_step(self):
        values = []
        
        for enum in range(1, len(self.strains[1])):
            value = stress.results(self.strains, criterium, enum)
            values.append(value[0])
        max_value = max(values)

        if max_value <= limit:
            return limit / max_value
        else:
            factor = (limit / max_value) * 1.0
            
            self.disp *= factor
        
            for i in range(len(self.strains)):
                for j in range(len(self.strains[i])):
                    for k in range(3): #the 3. is principal angle, not to be scaled
                        self.strains[i][j][k] *= factor
            return factor