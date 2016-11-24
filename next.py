"""
NEXT TO DO:

max, min, mean in figures OK

reactions in colors ?
probe in colors ?

reference calc

principal vectors 50%
Huber stress OK
reaction vectors
tension / compression

easy prep

matrix printer ?

check of code
comments and docs
"""

def principal_calc(self, stresses):
#Calculation of principal stresses and directions
    counter = -1
    principal_list = []
    for i in self.eles:
        counter += 1
        sigx = stresses[counter][0]
        sigy = stresses[counter][1]
        tauxy = stresses[counter][2]
        
        princ_part = math.sqrt((((sigx - sigy) / 2) ** 2) + (tauxy ** 2))
        
        if round(((sigx - sigy) / 2), 10) == 0:
            tetap = 1
        else:
            tetap = math.atan(((2 * tauxy) / (sigx - sigy)) / 2)
        tetas = tetap + math.radians(45)
        sig1 = ((sigx + sigy) / 2) + princ_part           
        sig2 = ((sigx + sigy) / 2) - princ_part
        taumax = (sig1 - sig2) / 2
        huber = math.sqrt(((sig1 - sig2) ** 2) / 2)
        
        principal_list.append([sig1, sig2, taumax, tetap, tetas, huber])
    print(principal_list[-1])
    return(principal_list)  