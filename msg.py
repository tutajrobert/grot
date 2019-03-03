import version

vers = version.get()

def welcome():
    #Welcome message
    print("")
    print("GRoT> ver. " + vers + ", [Graficzny Rozwiązywacz Tarcz]")
    print("................................................\n")

def size(width, height):
    print("")
    print("Calculated object size: [{} x {}]".format(width, height))

def matrixsize(size):
    print("")
    print("Built", "[" + size, "x", size + "]", "matrix")