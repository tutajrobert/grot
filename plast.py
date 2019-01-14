import stress

def search(eles, strains, material, flags_list):
    criterium = "huber"
    elist = []

    for enum in range(1, len(eles)):
        plast_value = eles[enum][11]
        if enum not in flags_list:
            E, v = material.get_prop(1)[0], material.get_prop(1)[1]
            value = stress.results(strains, criterium, enum - 1, E, v)
            if value is not None:
                if value[0] >= plast_value:
                    elist.append(enum)
                    flags_list.append(enum)
    return [elist, flags_list]
    #return [material.assignplast(elist), flags_list]