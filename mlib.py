def mdict():
    #Material dictionary. m[mat name] = [young modulus, poisson ratio]
    m = {}
    m["steel"] = [205e9, 0.3]
    m["alu"] = [8e10, 0.26]
    return m