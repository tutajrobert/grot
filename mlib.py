def mdict():
    """
    Material dictionary. m[mat name] = [young modulus,
                                        poisson ratio,
                                        yield stress,
                                        tangent modulus]
    """
    
    m = {}
    m["steel"] = [205e9, 0.3, 235, 0]
    m["alu"] = [80e9, 0.26]
    m["titan"] = [110e9, 0.32]
    return m