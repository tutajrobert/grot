def mdict():
    """
    Material dictionary. m[mat name] = [young modulus,
                                        poisson ratio,
                                        yield stress,
                                        tangent modulus / young modulus]
    """

    m = {}
    m["steel"] = [205e9, 0.3, 235, .04]
    m["alu"] = [80e9, 0.26, 160, .09]
    m["titan"] = [110e9, 0.32, 650, .06]
    return m