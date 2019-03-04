"""Stress and strains transformation (postprocessing) module"""

import math
import numpy

def all_res():
    """Returns names of all possible results"""
    names = []
    return names

def results(res_matrix, res_name, counter):
    """Stress and strains calculation"""
    if res_name == "eps_x":
        return [res_matrix[0][counter][0], "Normal XX component of strain tensor"]

    if res_name == "eps_y":
        return [res_matrix[0][counter][1], "Normal YY component of strain tensor"]

    if res_name == "eps_z":
        return [res_matrix[3][counter][3], "Normal ZZ component of strain tensor"]

    if res_name == "gamma_xy":
        return [2*res_matrix[0][counter][2], "Shear XY component of strain tensor"]

    if res_name == "sig_x":
        return [res_matrix[1][counter][0], "Normal XX component of stress tensor"]

    if res_name == "sig_y":
        return [res_matrix[1][counter][1], "Normal YY component of stress tensor"]

    if res_name == "sig_z":
        return [res_matrix[2][counter][3], "Normal ZZ component of stress tensor"]

    if res_name == "tau_xy":
        return [res_matrix[1][counter][2], "Shear XY component of stress tensor"]

    if res_name == "huber":
        #sxx = res_matrix[1][counter][0]
        #syy = res_matrix[1][counter][1]
        #sxy = res_matrix[1][counter][2]
        #szz = res_matrix[2][counter][3]
        huber = math.sqrt((res_matrix[2][counter][0] ** 2) + \
                          (res_matrix[2][counter][1] ** 2) - \
                          (res_matrix[2][counter][0] * res_matrix[2][counter][1]))
        #huber = math.sqrt(.5 * (((sxx - syy)**2) + ((syy - szz)**2) + \
        #                  ((szz - sxx)**2)) + (3 * (sxy**2)))
        return [huber, "Huber equivalent stress"]

    if res_name == "sign_huber":
        #sxx = res_matrix[1][counter][0]
        #syy = res_matrix[1][counter][1]
        #sxy = res_matrix[1][counter][2]
        #szz = res_matrix[2][counter][3]
        huber = math.sqrt((res_matrix[2][counter][0] ** 2) + \
                          (res_matrix[2][counter][1] ** 2) - \
                          (res_matrix[2][counter][0] * res_matrix[2][counter][1]))
        #huber = math.sqrt(.5 * (((sxx - syy)**2) + ((syy - szz)**2) + \
        #                  ((szz - sxx)**2)) + (3 * (sxy**2)))
        sign = numpy.sign(res_matrix[2][counter][0] + res_matrix[2][counter][1])
        sign_huber = sign * huber
        return [sign_huber, "Signed Huber equivalent stress"]

    if res_name == "sig_1":
        return [res_matrix[2][counter][0], "First principal stress"]

    if res_name == "sig_2":
        return [res_matrix[2][counter][1], "Second principal stress"]

    if res_name == "tau_max":
        return [res_matrix[2][counter][2], "Maximum shear stress"]

    if res_name == "eps_1":
        return [res_matrix[3][counter][0], "First principal strain"]

    if res_name == "eps_2":
        return [res_matrix[3][counter][1], "Second principal strain"]

    if res_name == "gamma_max":
        return [2*res_matrix[3][counter][2], "Maximum shear strain"]

    if res_name == "eff_strain":
        return [res_matrix[3][counter][4], "Effective strain"]

    if res_name == "theta":
        return [res_matrix[2][counter][5] * 180 / math.pi, "Principal stress orientation angle"]

    if res_name == "theta_n":
        return [res_matrix[3][counter][5] * 180 / math.pi, "Principal strain orientation angle"]

    if res_name == "inv_1":
        return [res_matrix[2][counter][0] + res_matrix[2][counter][1],
                "First invariant of stress tensor"]

    if res_name == "inv_2":
        return [res_matrix[2][counter][0] * res_matrix[2][counter][1],
                "Second invariant of stress tensor"]

    if res_name == "pl_strain":
        return [res_matrix[4][counter][0], "Plastic part of effective strain"]

    if res_name == "h_stress":
        return [res_matrix[4][counter][1], "Hardening Huber equivalent stress"]

    if res_name == "epl_x":
        return [res_matrix[4][counter][3], "Plastic XX component of strain tensor"]

    if res_name == "epl_y":
        return [res_matrix[4][counter][4], "Plastic YY component of strain tensor"]

    if res_name == "epl_xy":
        return [res_matrix[4][counter][5], "Plastic XY component of strain tensor"]

    if res_name == "epl_z":
        return [res_matrix[4][counter][6], "Plastic ZZ component of strain tensor"]
