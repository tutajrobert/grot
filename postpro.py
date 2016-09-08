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
plt.rcParams["legend.fontsize"] = 9

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
        #ax.set_axis_bgcolor((0.96, 0.96, 0.96))
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
        
        p = PatchCollection(patch_list, cmap = dis_cmap, alpha = 0.9)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        
        cbar_lim = [min(colors), max(colors)]
        cbar = plt.colorbar(p,
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
        #ax.set_axis_bgcolor((0.96, 0.96, 0.96))
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
                
            elif results == "huber":
                colors.append(math.sqrt((math.sqrt(self.res[1][counter][0] ** 2 + self.res[1][counter][1] ** 2) ** 2) + 
                              (3 * (self.res[1][counter][2] ** 2))))
                plt.title("Huber equivalent stress")
        
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
        
        p = PatchCollection(patch_list, cmap = dis_cmap, alpha = 0.9)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        
        """
        Min and max scatter plotting
        """
        
        #Max
        max_value = max(colors)
        max_string = ""
        max_screator = str(max_value)
        scounter = 0
        for i in range(len(max_screator)):
            if scounter < 4:
                if ((max_screator[i] == "0") or (max_screator[i] == ".")) and (scounter == 0):
                    max_string += max_screator[i]
                elif (max_screator[i] == "0") and (scounter != 0):
                    max_string += max_screator[i]
                    scounter += 1
                elif (max_screator[i] == ".") and (scounter != 0):
                    max_string += max_screator[i]
                else:
                    max_string += max_screator[i]
                    scounter += 1
        max_string 
        max_index = colors.index(max_value) + 1
        xlist, ylist = [], []
        xlist.append(self.eles[max_index][0][0])
        xlist.append(self.eles[max_index][1][0])
        xlist.append(self.eles[max_index][2][0])
        xlist.append(self.eles[max_index][3][0])
        ylist.append(self.eles[max_index][0][1])
        ylist.append(self.eles[max_index][1][1])
        ylist.append(self.eles[max_index][2][1])
        ylist.append(self.eles[max_index][3][1])
        
        x_pos_max = sum(xlist) / 4
        y_pos_max = - sum(ylist) / 4
        
        #Min
        min_value = min(colors)
        min_string = ""
        min_screator = str(min_value)
        scounter = 0
        for i in range(len(min_screator)):
            if scounter < 4:
                if ((min_screator[i] == "0") or (min_screator[i] == ".") or (min_screator[i] == "-")) and (scounter == 0):
                    min_string += min_screator[i]
                elif (min_screator[i] == "0") and (scounter != 0):
                    min_string += min_screator[i]
                    scounter += 1
                elif (min_screator[i] == ".") and (scounter != 0):
                    min_string += min_screator[i]
                else:
                    min_string += min_screator[i]
                    scounter += 1
        min_string 
        min_index = colors.index(min_value) + 1
        xlist, ylist = [], []
        xlist.append(self.eles[min_index][0][0])
        xlist.append(self.eles[min_index][1][0])
        xlist.append(self.eles[min_index][2][0])
        xlist.append(self.eles[min_index][3][0])
        ylist.append(self.eles[min_index][0][1])
        ylist.append(self.eles[min_index][1][1])
        ylist.append(self.eles[min_index][2][1])
        ylist.append(self.eles[min_index][3][1])
        
        x_pos_min = sum(xlist) / 4
        y_pos_min = - sum(ylist) / 4
        
        #Plotting
        if min_value < 0:
            plt.scatter(x_pos_max, y_pos_max, marker = "^", c = "white", s = 52, label = "max:  " + str(max_string))
        else:
            plt.scatter(x_pos_max, y_pos_max, marker = "^", c = "white", s = 52, label = "max: " + str(max_string))
        plt.scatter(x_pos_min, y_pos_min, marker = "v", c = "white", s = 52, label = "min: " + str(min_string))
        
        """
        End of min and max scatter plotting
        """
        
        #Color bar limits set to (mean + 2 * standard deviation)
        cbar_lim = [numpy.mean(colors) -  (2 * numpy.std(colors)),
                    numpy.mean(colors) + (2 * numpy.std(colors))]
                
        cbar = plt.colorbar(p,
                            ticks = numpy.linspace(cbar_lim[0], 
                                                   cbar_lim[1], 
                                                   1 + self.ncol), 
                            extend='both')
        
        if results == "huber":
            cbar_lim = [numpy.mean(colors) -  (2 * numpy.std(colors)),
                        numpy.mean(colors) + (2 * numpy.std(colors))]
            if numpy.mean(colors) -  (2 * numpy.std(colors)) < 0:
                cbar_lim = [0,
                            numpy.mean(colors) + (2 * numpy.std(colors))]
                
        p.set_clim(cbar_lim)
        
        plt.xlim(min_x - 1, max_x + 1)
        plt.ylim(min_y - 1, max_y + 1)
        
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
        
        legend = ax.legend(loc = "best", scatterpoints = 1)
        
        legend.get_texts()[0].set_color([0.64705884,  0., 0.14901961, 1.])
        legend.get_texts()[1].set_color([0.19215687, 0.21176471, 0.58431375, 1.])
        
        frame = legend.get_frame()
        frame.set_edgecolor("white")
        #plt.grid()
        
        plt.savefig(results + ".png", DPI = 1200)
        
        print("Saved results file", "[" + results + ".png]")