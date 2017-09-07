import math
import numpy

def results(res_matrix, res_name, counter):
    if res_name == "eps_x":
        return [res_matrix[0][counter][0], "Normal XX component of strain tensor"]

    elif res_name == "eps_y":
        return [res_matrix[0][counter][1], "Normal YY component of strain tensor"]
        
    elif res_name == "gamma_xy":
        return [res_matrix[0][counter][2], "Shear XY component of strain tensor"]
    
    elif res_name == "sig_x":
        return [res_matrix[1][counter][0], "Normal XX component of stress tensor"]

    elif res_name == "sig_y":
        return [res_matrix[1][counter][1], "Normal YY component of stress tensor"]
        
    elif res_name == "tau_xy":
        return [res_matrix[1][counter][2], "Shear XY component of stress tensor"]
        
    elif res_name == "huber":
        huber = math.sqrt((res_matrix[2][counter][0] ** 2) + (res_matrix[2][counter][1] ** 2) - (res_matrix[2][counter][0] * res_matrix[2][counter][1]))
        return [huber, "Huber equivalent stress"]
        
    elif res_name == "sign_huber":
        huber = math.sqrt((res_matrix[2][counter][0] ** 2) + (res_matrix[2][counter][1] ** 2) - (res_matrix[2][counter][0] * res_matrix[2][counter][1]))
        sign = numpy.sign(res_matrix[2][counter][0] + res_matrix[2][counter][1])    
        sign_huber = sign * huber           
        return [sign_huber, "Signed Huber equivalent stress"]
        
    elif res_name == "princ1":
        return [res_matrix[2][counter][0], "First principal stress"]
        
    elif res_name == "princ2":
        return [res_matrix[2][counter][1], "Second principal stress"]
        
    elif res_name == "tau_max":
        return [res_matrix[2][counter][2], "Maximum shear stress"]
    else:
        pass
