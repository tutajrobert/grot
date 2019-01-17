import math
import numpy

def all_res():
    names = []
    return names

def results(res_matrix, res_name, counter, E, v):
    if res_name == "eps_x":
        return [res_matrix[0][counter][0], "Normal XX component of strain tensor"]

    elif res_name == "eps_y":
        return [res_matrix[0][counter][1], "Normal YY component of strain tensor"]

    elif res_name == "eps_z":
        ezz = (res_matrix[1][counter][0] + res_matrix[1][counter][1]) * -v / E
        return [ezz, "Normal ZZ component of strain tensor"]

    elif res_name == "gamma_xy":
        return [2*res_matrix[0][counter][2], "Shear XY component of strain tensor"]

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

    elif res_name == "sig_1":
        return [res_matrix[2][counter][0], "First principal stress"]

    elif res_name == "sig_2":
        return [res_matrix[2][counter][1], "Second principal stress"]

    elif res_name == "tau_max":
        return [res_matrix[2][counter][2], "Maximum shear stress"]

    elif res_name == "eps_1":
        return [res_matrix[3][counter][0], "First principal strain"]

    elif res_name == "eps_2":
        return [res_matrix[3][counter][1], "Second principal strain"]

    elif res_name == "gamma_max":
        return [2*res_matrix[3][counter][2], "Maximum shear strain"]

    elif res_name == "eff_strain":
        exx = res_matrix[0][counter][0]
        eyy = res_matrix[0][counter][1]
        ezz = (res_matrix[1][counter][0] + res_matrix[1][counter][1]) * -v / E
        exy = res_matrix[0][counter][2]
        eff_strain = (1 / (math.sqrt(2) * (1 + v))) * math.sqrt(((exx - eyy)**2 + (eyy - ezz)**2 + (ezz - exx)**2) + ((3/2)*(exy**2)))
        return [eff_strain, "Effective strain"]
		
    elif res_name == "theta":
        return [res_matrix[2][counter][3] * 180 / math.pi, "Principal stress orientation angle"]
    elif res_name == "theta_n":
        return [res_matrix[3][counter][3] * 180 / math.pi, "Principal strain orientation angle"]
    elif res_name == "inv_1":
        return [res_matrix[2][counter][0] + res_matrix[2][counter][1], "First invariant of stress tensor"]

    elif res_name == "inv_2":
        return [res_matrix[2][counter][0] * res_matrix[2][counter][1], "Second invariant of stress tensor"]
    
    elif res_name == "pl_strain":
        return [res_matrix[4][counter][0], "Plastic part of effective strain"]
 
    elif res_name == "res_stress":
        return [res_matrix[4][counter][1], "Residual Huber equivalent stress"]

    elif res_name == "tot_strain":
        return [res_matrix[4][counter][2], "Total effective strain"]
 
    elif res_name == "plex":
        return [res_matrix[4][counter][3], "plex"]
        
    elif res_name == "pley":
        return [res_matrix[4][counter][4], "pley"]

    elif res_name == "plexy":
        return [res_matrix[4][counter][5], "plexy"]
        
    elif res_name == "plez":
        return [res_matrix[4][counter][6], "plez"]
 
    elif res_name == "bstress":
        exx = res_matrix[0][counter][0] - res_matrix[4][counter][3]
        eyy = res_matrix[0][counter][1] - res_matrix[4][counter][4]
        exy = res_matrix[0][counter][2] - res_matrix[4][counter][5]
        #sxx = (E / (1 - (v**2))) * (exx + (v * eyy))
        #syy = (E / (1 - (v**2))) * (eyy + (v * exx))
        #ezz = ((sxx + syy) * -v / E) - res_matrix[4][counter][6]
        #strains_t = [exx, eyy, exy]
        #fc = E / (1 - (v ** 2))
           
        #slist = numpy.array(
        #    [[fc, fc * v, 0],
        #     [fc * v, fc, 0],
        #     [0, 0, fc * ((1 - v)/ 2)]])
                     
        #s = (numpy.dot(slist, strains_t))
        #ezz = ((s[0] + s[1]) * -v / E)# - res_matrix[4][counter][6]
        #ezz = ((res_matrix[1][counter][0] + res_matrix[1][counter][1]) * -v / E) - res_matrix[4][counter][6]
        v = .3
        ezz = -((exx * v) + (eyy * v))
        eff_strain = (1 / (math.sqrt(2) * (1 + v))) * math.sqrt(((exx - eyy)**2 + (eyy - ezz)**2 + (ezz - exx)**2) + ((3/2)*(exy**2)))
        #plstrain = res_matrix[4][counter][0]
        value = 205e3 * eff_strain
        return [value, "Back stress"]
    else:
        pass
