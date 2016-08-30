import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
from matplotlib.collections import PatchCollection
import math
import numpy
import tools

class prepare():
    def __init__(self, nodes, elements, results):
        self.nodes = nodes
        self.eles = elements
        self.res = results
    
    def disp_tot(self):
        
        """
        Matplotlib script for resultant displacement view
        One element == one colour, so element solution
        """
    
        colors = []
        xs = [self.nodes[i][0] for i in self.nodes]
        ys = [-self.nodes[i][1] for i in self.nodes]
        zs = []
        for i in range(0, len(self.res), 2):
            zs.append(math.sqrt((self.res[i] ** 2) + (self.res[i + 1] ** 2)))
        
        fig, ax = plt.subplots()
        patch_list = []
        
        min_x, min_y = self.eles[1][0][0], -self.eles[1][0][1]
        max_x, max_y = min_x, min_y
        
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
    
            #Rectangle of vertex in (x, y) and given width and height
            patch_list.append(patches.Rectangle((min(xlist), -min(ylist)), 1.0, -1.0))
            
            min_x = tools.min_search(min(xlist), min_x)
            min_y = tools.min_search(-max(ylist), min_y)            
            max_x = tools.max_search(max(xlist), max_x)
            max_y = tools.max_search(-min(ylist), max_y)
            
            dof1 = (self.eles[i][4] * 2) - 2
            dof2 = (self.eles[i][5] * 2) - 2
            dof3 = (self.eles[i][6] * 2) - 2
            dof4 = (self.eles[i][7] * 2) - 2
            dofs = [dof1, dof1 + 1, dof2, dof2 + 1, dof3, dof3 + 1, dof4, dof4 + 1]
            
            colors.append((self.res[dofs[0]] + self.res[dofs[2]] + self.res[dofs[4]] + self.res[dofs[6]]) / 4)
        
        diff_x = max_x - min_x
        diff_y = max_y - min_y
        sum_x = max_x + min_x
        sum_y = max_y + min_y

        if diff_x > diff_y:
         		max_y = (sum_y / 2) + (diff_x / 2)
         		min_y = (sum_y / 2) - (diff_x / 2)
         		
        else:
         		max_x = (sum_x / 2) + (diff_y / 2)
         		min_x = (sum_x / 2) - (diff_y / 2)

        p = PatchCollection(patch_list, cmap=cm.jet, alpha=0.5)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        plt.colorbar(p)
        plt.xlim(min_x - 1, max_x + 1)
        plt.ylim(min_y - 1, max_y + 1)
        plt.grid()
        plt.show()