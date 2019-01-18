import stress, copy, os

def search(eles, strains, material, flags_list, old_strains, load_step, load_inc, pstrains):
    criterium = "huber"
    elist = []

    residuals = [0]
    
    for enum in range(1, len(eles)):
        plast_value = eles[enum][11]
        if enum not in flags_list:
            E, v = material.get_prop(1)[0], material.get_prop(1)[1]
            value = stress.results(strains, criterium, enum - 1, E, v)
            old_value = stress.results(old_strains, criterium, enum - 1, E, v)[0]
            if value is not None:
                if value[0] >= plast_value:
                    elist.append(enum)
                    flags_list.append(enum)
                    residuals.append(old_value / plast_value)
    if len(residuals) > 1:
        residuals.pop(0)
    #print(min(residuals), max(residuals), sum(residuals)/len(residuals), len(elist), len(flags_list), load_step, load_inc, max(pstrains), sum(pstrains)/len(pstrains))
    return [elist, flags_list, residuals]
    #return [material.assignplast(elist), flags_list]
    
def check(eles, strains, material, flags_list, old_strains, load_step, load_inc, pstrains, allresiduals, proj_name):
    criterium = "huber"
    elist = []
    
    residuals = [0]
    eprint = []
    flags = copy.copy(flags_list)
    
    for enum in range(1, len(eles)):
        plast_value = eles[enum][11]
        if enum not in flags_list:
            E, v = material.get_prop(1)[0], material.get_prop(1)[1]
            value = stress.results(strains, criterium, enum - 1, E, v)
            old_value = stress.results(old_strains, criterium, enum - 1, E, v)[0]
            if value is not None:
                if value[0] >= plast_value:
                    eprint.append(enum)
                    flags.append(enum)
                    residuals.append(old_value / plast_value)
                    allresiduals.append(old_value / plast_value)
    if len(residuals) > 1:
        residuals.pop(0)
    
    s0 = " "
    s1 = str(round(min(residuals), 4))
    s2 = str(round(max(residuals), 4))
    s3 = str(round(sum(residuals)/len(residuals), 4))
    s4 = str(len(elist))
    s5 = str(len(flags_list))
    s6 = str(round(load_step, 4))
    s7 = str(round(load_inc, 4))
    s8 = str(round(max(pstrains), 4))
    s9 = str(round(sum(pstrains)/len(pstrains), 4))

    if not os.path.exists("results" + os.sep + proj_name):
        os.makedirs("results" + os.sep + proj_name)
    file = open("results" + os.sep + proj_name + os.sep + "plast.txt", "a") 
    line = s1 + s0 + s2 + s0 + s3 + s0 + s4 + s0 + s5 + s0 + s6 + s0 + s7 + s0 + s8 + s0 + s9
    file.write(line + "\n")
    file.close()
    
    return allresiduals