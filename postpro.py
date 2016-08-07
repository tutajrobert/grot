import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
from matplotlib.collections import PatchCollection
import math
import numpy
import scipy.interpolate

class prepare():
    def __init__(self, nodes, elements, results):
        self.nodes = nodes
        self.eles = elements
        self.res = results
    
    def nod_disp(self):
        xs = [self.nodes[i][0] for i in self.nodes]
        ys = [-self.nodes[i][1] for i in self.nodes]
        zs = []
        for i in range(0, len(self.res), 2):
            zs.append(math.sqrt((self.res[i] ** 2) + (self.res[i + 1] ** 2)))
        
        fig, ax = plt.subplots()
        patch_list = []
        print(self.eles)
        for i in self.eles:
            xlist, ylist = [], []
            xlist.append(self.eles[i][0][0])
            xlist.append(self.eles[i][1][0])
            xlist.append(self.eles[i][2][0])
            xlist.append(self.eles[i][3][0])
            ylist.append(self.eles[i][0][1])
            ylist.append(self.eles[i][1][1])
            ylist.append(self.eles[i][2][1])
            ylist.append(self.eles[i][3][1])
            patch_list.append(
                patches.Rectangle(
                    (min(xlist), -min(ylist)),   # (x,y)
                    1.0,          # width
                    1.0
                    )
                )
        colors = 100*numpy.random.rand(len(patch_list))
        p = PatchCollection(patch_list, cmap=cm.jet, alpha=0.4)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        plt.colorbar(p)
        plt.plot([0,10],[0,-10])
        plt.show()