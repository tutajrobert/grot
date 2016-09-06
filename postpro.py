import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
from matplotlib.collections import PatchCollection
import math
import numpy
import tools

#Matplotlib style functions
plt.rcParams["font.family"] = "monospace"
plt.rcParams["font.size"] = 10
plt.rcParams["font.weight"] = 100
plt.rcParams["font.variant"] = "small-caps"
plt.rcParams["xtick.major.size"] = 0
plt.rcParams["ytick.major.size"] = 0
plt.rcParams["text.hinting_factor"] = 1
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["patch.linewidth"] = 0.5

def discrete_cmap(N, base_cmap=None):
    #Create an N-bin discrete colormap from the specified input map
    
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(numpy.linspace(1 - (1 / N), 1 / N, N))
    
    """
    For edge colors retrieving
    down_up = [base(numpy.linspace(1, 0, N))[0],
              base(numpy.linspace(1, 0, N))[-1]]
    """
              
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

class prepare():
    def __init__(self, nodes, elements, results):
        self.nodes = nodes
        self.eles = elements
        self.res = results
        self.ncol = 9
        self.init_cmap = "RdYlBu"
    
    def save_dresults(self, results):
        
        """
        Matplotlib script for results viewing
        One element == one colour, so element solution
        """
    
        colors = []
        xs = [self.nodes[i][0] for i in self.nodes]
        ys = [-self.nodes[i][1] for i in self.nodes]
        
        fig, ax = plt.subplots()
        #ax.set_axis_bgcolor((1, 1, 1))
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
            patch_list.append(patches.Rectangle((min(xlist), 
                                                -min(ylist)), 
                                                1.0, 
                                                -1.0))
            
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
            
            #Results choosing and preparing
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
                colors.append(0.25 * (math.sqrt((self.res[dofs[0]] ** 2) + 
                                                (self.res[dofs[1]] ** 2)) + 
                                      math.sqrt((self.res[dofs[2]] ** 2) + 
                                                (self.res[dofs[3]] ** 2)) +
                                      math.sqrt((self.res[dofs[4]] ** 2) + 
                                                (self.res[dofs[5]] ** 2)) +
                                      math.sqrt((self.res[dofs[6]] ** 2) + 
                                                (self.res[dofs[7]] ** 2))))
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
        dis_cmap = cmap=discrete_cmap(self.ncol, self.init_cmap)
        
        p = PatchCollection(patch_list, cmap = dis_cmap)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        
        cbar_lim = [min(colors), max(colors)]
        cbar = plt.colorbar(p, alpha = 0.8,
                            ticks = numpy.linspace(cbar_lim[0], 
                                                   cbar_lim[1], 
                                                   1 + self.ncol), 
                            )
        p.set_clim(cbar_lim)
        
        plt.xlim(min_x - 1, max_x + 1)
        plt.ylim(min_y - 1, max_y + 1)
        
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
        
        #plt.grid()
        
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
            patch_list.append(patches.Rectangle((min(xlist), 
                                                -min(ylist)), 
                                                1.0, 
                                                -1.0))
            
            #Axes limits searching
            min_x = tools.min_search(min(xlist), min_x)
            min_y = tools.min_search(-max(ylist), min_y)            
            max_x = tools.max_search(max(xlist), max_x)
            max_y = tools.max_search(-min(ylist), max_y)
            
            #Results choosing and preparing
            if results == "eps_x":
                colors.append(self.res[0][counter][0])
                plt.title("Normal XX component of strain tensor")

            elif results == "eps_y":
                colors.append(self.res[0][counter][1])
                plt.title("Normal YY component of strain tensor")
                
            elif results == "gamma_xy":
                colors.append(self.res[0][counter][2])
                plt.title("Shear XY component of strain tensor")
            
            if results == "sig_x":
                colors.append(self.res[1][counter][0])
                plt.title("Normal XX component of stress tensor")

            elif results == "sig_y":
                colors.append(self.res[1][counter][1])
                plt.title("Normal YY component of stress tensor")
                
            elif results == "tau_xy":
                colors.append(self.res[1][counter][2])
                plt.title("Shear XY component of stress tensor")       
        
            else:
                pass
                
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
        dis_cmap = cmap=discrete_cmap(self.ncol, self.init_cmap)
        #Hardcoded colors of color bar extensions
        cmap.set_over([0.64705884,  0., 0.14901961, 1.])
        cmap.set_under([0.19215687, 0.21176471, 0.58431375, 1.])
        
        p = PatchCollection(patch_list, cmap = dis_cmap)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        
        cbar_lim = [numpy.mean(colors) - numpy.std(colors),
                    numpy.mean(colors) + numpy.std(colors)]
        cbar = plt.colorbar(p, alpha = 0.8,
                            ticks = numpy.linspace(cbar_lim[0], 
                                                   cbar_lim[1], 
                                                   1 + self.ncol), 
                            extend='both')
        p.set_clim(cbar_lim)
        
        plt.xlim(min_x - 1, max_x + 1)
        plt.ylim(min_y - 1, max_y + 1)
        
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
        
        #plt.grid()
        
        plt.savefig(results + ".png", DPI = 600)
        
        print("Saved results file", "[" + results + ".png]")