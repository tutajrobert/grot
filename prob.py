import os
import math
import stress

names = ["elem_num", "eps_x", "eps_y", "eps_z", "gamma_xy", "sig_x", "sig_y", "tau_xy", "huber", "sign_huber", "sig_1", "sig_2", "tau_max",
        "eps_1", "eps_2", "gamma_max", "theta", "inv_1", "inv_2"]
 
table_to_print = [] 
def write(color, bc_dict, eprobes_dict, disp, strains, proj_name, material):
    if not os.path.exists("results" + os.sep + proj_name):
        os.makedirs("results" + os.sep + proj_name)
    file = open("results" + os.sep + proj_name + os.sep + "eres.txt", "w")
    table_to_print.append(names)
    for e in eprobes_dict[color]:
        res_table = []
        res_table.append((7 - int(len(str(e)) / 2)) * " " + str(e))
        for name in names[1:]:
            E = material.get_prop(1)[0]
            v = material.get_prop(1)[1]
            value = stress.results(strains, name, e - 1, E, v)
            if value is not None:
                if str(value[0])[0] == "-":
                    res_table.append("{0:.{1}e}".format(value[0], 6))
                else:
                    res_table.append(" {0:.{1}e}".format(value[0], 6))                
            else:
                res_table.append("0")
        table_to_print.append(res_table)
    for j in range(len(table_to_print[0])):
        line = ""
        for i in range(len(table_to_print)):
            line += table_to_print[i][j]
            line += (16 - len(table_to_print[i][j])) * " "
        file.write(line + "\n")
    file.close()
    print("Saved probed results", "[" + "e_res" + ".txt] to results" + os.sep + proj_name + os.sep)
    
"""
    counter = 0
    for n in bc_dict[color]:
        if counter == 0:
            dof1 = (self.eles[i][4] * 2) - 2
            dof2 = (self.eles[i][5] * 2) - 2
            dof3 = (self.eles[i][6] * 2) - 2
            dof4 = (self.eles[i][7] * 2) - 2
            dofs = [dof1, dof1 + 1, dof2, dof2 + 1, dof3, dof3 + 1, dof4, dof4 + 1]
        counter += 1
        if counter == 3:
            counter = 0
    """