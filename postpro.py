import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
from matplotlib.collections import PatchCollection
import math
import numpy
import tools

plt.rcParams["font.family"] = "monospace"
plt.rcParams["font.size"] = 10
plt.rcParams["font.weight"] = 100
plt.rcParams["font.variant"] = "small-caps"
plt.rcParams["xtick.major.size"] = 0
plt.rcParams["ytick.major.size"] = 0
plt.rcParams["text.hinting_factor"] = 1
plt.rcParams["figure.facecolor"] = "white"

class prepare():
    def __init__(self, nodes, elements, results):
        self.nodes = nodes
        self.eles = elements
        self.res = results
    
    def save_dresults(self, results):
        
        """
        Matplotlib script for results viewing
        One element == one colour, so element solution
        """
    
        colors = []
        xs = [self.nodes[i][0] for i in self.nodes]
        ys = [-self.nodes[i][1] for i in self.nodes]
        
        fig, ax = plt.subplots()
        patch_list = []
        
        min_x, min_y = self.eles[1][0][0], -self.eles[1][0][1]
        max_x, max_y = min_x, min_y
        
        #Nodes coordinates storing
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
            
            
            #Axes limits searching
            min_x = tools.min_search(min(xlist), min_x)
            min_y = tools.min_search(-max(ylist), min_y)            
            max_x = tools.max_search(max(xlist), max_x)
            max_y = tools.max_search(-min(ylist), max_y)
            
            #Displacement results storing
            dof1 = (self.eles[i][4] * 2) - 2
            dof2 = (self.eles[i][5] * 2) - 2
            dof3 = (self.eles[i][6] * 2) - 2
            dof4 = (self.eles[i][7] * 2) - 2
            dofs = [dof1, dof1 + 1, dof2, dof2 + 1, dof3, dof3 + 1, dof4, dof4 + 1]
            
            #Results choosing
            if results == "disp_x":
                colors.append(0.25 * (self.res[dofs[0]] + 
                                      self.res[dofs[2]] + 
                                      self.res[dofs[4]] + 
                                      self.res[dofs[6]]))
                plt.title("Displacement in X direction")
            elif results == "disp_y":
                colors.append(0.25 * (self.res[dofs[1]] + 
                                      self.res[dofs[3]] + 
                                      self.res[dofs[5]] + 
                                      self.res[dofs[7]]))
                plt.title("Displacement in Y direction")
                
            elif results == "disp_mag":
                colors.append(0.25 * (math.sqrt((self.res[dofs[0]] ** 2) + (self.res[dofs[1]] ** 2)) + 
                                       math.sqrt((self.res[dofs[2]] ** 2) + (self.res[dofs[3]] ** 2)) +
                                       math.sqrt((self.res[dofs[4]] ** 2) + (self.res[dofs[5]] ** 2)) +
                                       math.sqrt((self.res[dofs[6]] ** 2) + (self.res[dofs[7]] ** 2))))
                plt.title("Displacement magnitude")
        
        #Axes range
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

        #Matplotlib functions
        col_map = cm.get_cmap("coolwarm")
        p = PatchCollection(patch_list, cmap=col_map)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        plt.colorbar(p)
        plt.xlim(min_x - 1, max_x + 1)
        plt.ylim(min_y - 1, max_y + 1)
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
        plt.grid()
        #plt.show()
        plt.savefig(results + ".png", DPI = 600)
        
        print("Saved results file", "[" + results + ".png]")
        
        
    def save_sresults(self, results):
        
        """
        Matplotlib script for results viewing
        One element == one colour, so element solution
        """
    
        colors = []
        xs = [self.nodes[i][0] for i in self.nodes]
        ys = [-self.nodes[i][1] for i in self.nodes]
        
        fig, ax = plt.subplots()
        patch_list = []
        
        min_x, min_y = self.eles[1][0][0], -self.eles[1][0][1]
        max_x, max_y = min_x, min_y
        
        counter = -1
        
        #Nodes coordinates storing
        for i in self.eles:
            counter += 1
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
            
            #Axes limits searching
            min_x = tools.min_search(min(xlist), min_x)
            min_y = tools.min_search(-max(ylist), min_y)            
            max_x = tools.max_search(max(xlist), max_x)
            max_y = tools.max_search(-min(ylist), max_y)
            
            #Results choosing
            if results == "strn_x":
                colors.append(self.res[counter][0])
                plt.title("Normal XX component of strains tensor")

            elif results == "strn_y":
                colors.append(self.res[counter][1])
                plt.title("Normal YY component of strains tensor")
                
            elif results == "strn_xy":
                colors.append(self.res[counter][2])
                plt.title("Shear XY component of strains tensor")
        
        #Axes range
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

        #Matplotlib functions
        col_map = cm.get_cmap("coolwarm")
        p = PatchCollection(patch_list, cmap=col_map)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        plt.colorbar(p)
        plt.xlim(min_x - 1, max_x + 1)
        plt.ylim(min_y - 1, max_y + 1)
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
        plt.grid()
        #plt.show()
        plt.savefig(results + ".png", DPI = 600)
        
        print("Saved results file", "[" + results + ".png]")