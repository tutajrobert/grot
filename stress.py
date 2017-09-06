import math
import numpy

def results(res_matrix, res_name, counter):
    if res_name == "eps_x":
        return [res_matrix[0][counter][0], "Normal XX component of strain tensor"]

    elif res_name == "eps_y":
        return [res_matrix[0][counter][1], "Normal YY component of strain tensor"]
        
    elif res_name == "gamma_xy":
        return [res_matrix[0][counter][2], "Shear XY component of strain tensor"]
    
    if res_name == "sig_x":
        return [res_matrix[1][counter][0], "Normal XX component of stress tensor"]

    elif res_name == "sig_y":
        return [res_matrix[1][counter][1], "Normal YY component of stress tensor"]
        
    elif res_name == "tau_xy":
        return [res_matrix[1][counter][2], "Shear XY component of stress tensor"]
    
    elif res_name == "tau_max":
        sigy = res_matrix[1][counter][1]
        sigx = res_matrix[1][counter][0]
        tauxy = res_matrix[1][counter][2] 
        taumax = math.sqrt((((sigx - sigy) / 2) ** 2) + (tauxy ** 2))
        return [taumax, "Maximum shear stress"]
        
    elif res_name == "huber":
        sigy = res_matrix[1][counter][1]
        sigx = res_matrix[1][counter][0]
        tauxy = res_matrix[1][counter][2]    
        huber = math.sqrt((sigx ** 2) + (sigy ** 2) + (3 * (tauxy ** 2)))
        return [huber, "Huber equivalent stress"]
        
    elif res_name == "sign_huber":
        sigy = res_matrix[1][counter][1]
        sigx = res_matrix[1][counter][0]
        tauxy = res_matrix[1][counter][2] 
        taumax = math.sqrt((((sigx - sigy) / 2) ** 2) + (tauxy ** 2))
        sig1 = ((sigx + sigy) / 2) + taumax
        sig2 = ((sigx + sigy) / 2) - taumax
        sign = numpy.sign(sig1 + sig2)    
        sign_huber = sign * math.sqrt((sigx ** 2) + (sigy ** 2) + (3 * (tauxy ** 2)))                
        return [sign_huber, "Signed Huber equivalent stress"]
    else:
        pass