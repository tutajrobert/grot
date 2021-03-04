def mdict():
    """
    Material dictionary. m[mat name] = [young modulus,
                                        poisson ratio,
                                        yield stress]
    """
    
    m = {}
    m["steel"] = [205e9, 0.3, 235]
    m["alu"] = [80e9, 0.26, 160]
    m["titan"] = [110e9, 0.32, 650]
    return m