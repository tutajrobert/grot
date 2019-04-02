"""Probe function for elements results checking"""

import os
import stress

NAMES = ["elem_num", "eps_x", "eps_y", "eps_z", "gamma_xy", "sig_x", "sig_y", "tau_xy", "huber",
         "sign_huber", "sig_1", "sig_2", "tau_max", "eps_1", "eps_2", "gamma_max", "theta", "inv_1",
         "inv_2"]

TBL_2_PRNT = []
def write(color, eprobes_dict, strains, proj_name, material):
    """Writes file with results"""
    if not os.path.exists("results" + os.sep + proj_name):
        os.makedirs("results" + os.sep + proj_name)
    file = open("results" + os.sep + proj_name + os.sep + "eres.txt", "w")
    TBL_2_PRNT.append(NAMES)
    for e in eprobes_dict[color]:
        res_table = []
        res_table.append((7 - int(len(str(e)) / 2)) * " " + str(e))
        for name in NAMES[1:]:
            E = material.get_prop(1)[0]
            v = material.get_prop(1)[1]
            value = stress.results(strains, name, e - 1)
            if value is not None:
                if str(value[0])[0] == "-":
                    res_table.append("{0:.{1}e}".format(value[0], 6))
                else:
                    res_table.append(" {0:.{1}e}".format(value[0], 6))
            else:
                res_table.append("0")
        TBL_2_PRNT.append(res_table)
    for j in range(len(TBL_2_PRNT[0])):
        line = ""
        for i in range(len(TBL_2_PRNT)):
            line += TBL_2_PRNT[i][j]
            line += (16 - len(TBL_2_PRNT[i][j])) * " "
        file.write(line + "\n")
    file.close()
    print("Saved probed results", "[" + "e_res" + ".txt] to results" + os.sep + proj_name + os.sep)
    