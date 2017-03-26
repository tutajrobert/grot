import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
import matplotlib.colors as clr
from matplotlib import rc
import os
from matplotlib.collections import PatchCollection
import math
import numpy
import tools
import version

vers = version.get()

#Matplotlib style functions
patch_line = 0.15
alpha = 1.0
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 11
plt.rcParams["font.weight"] = 100
#plt.rcParams["font.variant"] = "small-caps"
plt.rcParams["text.hinting_factor"] = 1
#plt.rcParams["figure.facecolor"] = "gray"
plt.rcParams["patch.linewidth"] = patch_line
plt.rcParams["legend.fontsize"] = 10

def minmax(colors, eles):

    """
    Min and max scatter plotting
    """
        
    #Max
    max_value = max(colors)              
    max_string = "%.3e" % max_value
    
    max_index = colors.index(max_value) + 1
    xlist_max = [eles[max_index][i][0] for i in range(0, 4)]
    ylist_max = [eles[max_index][i][1] for i in range(0, 4)]
    
    x_pos_max = sum(xlist_max) / 4
    y_pos_max = - sum(ylist_max) / 4
    
    #Min
    min_value = min(colors)
    min_string = "%.3e" % min_value
    
    min_index = colors.index(min_value) + 1
    xlist_min = [eles[min_index][i][0] for i in range(0, 4)]
    ylist_min = [eles[min_index][i][1] for i in range(0, 4)]
    
    x_pos_min = sum(xlist_min) / 4
    y_pos_min = - sum(ylist_min) / 4
    
    return(x_pos_max, y_pos_max, max_string, x_pos_min, y_pos_min, min_string)
    
    """
    End of min and max scatter plotting
    """

def discrete_cmap(N, base_cmap=None):
    #Create an N-bin discrete colormap from the specified input map
    
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(numpy.linspace(1 - (1 / N), 1 / N, N))
    color_list[3] = [.906, .906, .906, 1.]
    #For edge colors retrieving
    # 0 is for max
    # 1 is for min
    # 2 is for min label
    down_up = [base(numpy.linspace(1 - (0.2 / N), 0.2 / N, N))[0],
              base(numpy.linspace(1 - (0.2 / N), 0.2 / N, N))[-1],
              base(numpy.linspace(1 - (0.2 / N), 0.2 / N, N))[-1]]
    
              
    cmap_name = base.name + str(N)
    #if (type(base) is str) or (type(base) is None):
    return [clr.LinearSegmentedColormap.from_list(cmap_name, color_list, N), down_up[0], down_up[1], down_up[2]]
    #else:
    #    return [base.from_list(cmap_name, color_list, N), down_up[0], down_up[1]]

class prepare():
    def __init__(self, nodes, elements, results):
        self.nodes = nodes
        self.eles = elements
        self.res = results
        self.ncol = 7
        self.init_cmap = "coolwarm_r"
    
    def save_dresults(self, results, proj_name):
        
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
            xlist = [self.eles[i][j][0] for j in range(0, 4)]
            ylist = [self.eles[i][j][1] for j in range(0, 4)]
    
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
            if results == "x":
                colors.append(0.25 * (self.res[dofs[0]] + 
                                      self.res[dofs[2]] + 
                                      self.res[dofs[4]] + 
                                      self.res[dofs[6]]))
                plt.title("Displacement in X direction")
            elif results == "y":
                colors.append(0.25 * (self.res[dofs[1]] + 
                                      self.res[dofs[3]] + 
                                      self.res[dofs[5]] + 
                                      self.res[dofs[7]]))
                plt.title("Displacement in Y direction")
                
            elif results == "mag":
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
        dis_cmap = cmap = discrete_cmap(self.ncol, self.init_cmap)[0]
        
        p = PatchCollection(patch_list, cmap = dis_cmap, alpha = alpha)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        
        #Plotting min/max
        minmax_data = minmax(colors, self.eles)
        
        x_pos_max = minmax_data[0]
        y_pos_max = minmax_data[1]
        max_string = minmax_data[2]
        x_pos_min = minmax_data[3]
        y_pos_min = minmax_data[4]
        min_string = minmax_data[5]
        
        logo_legend = plt.scatter(1e6, 1e6, marker = "None", label = "GRoT> ver. " + vers)
        
        #markers border width change
        plt.rcParams["patch.linewidth"] = 0.5
        if float(min_string) < 0 and float(max_string) >= 0:
            max_legend = plt.scatter(x_pos_max, y_pos_max, marker = "^", c = "white", s = 52, label = "max:  " + str(max_string))
        else:
            max_legend = plt.scatter(x_pos_max, y_pos_max, marker = "^", c = "white", s = 52, label = "max: " + str(max_string))
        min_legend = plt.scatter(x_pos_min, y_pos_min, marker = "v", c = "white", s = 52, label = "min: " + str(min_string))
        plt.rcParams["patch.linewidth"] = patch_line
        
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
        
        legend_down = plt.legend(handles = [logo_legend], loc = 4, scatterpoints = 1)
        frame = legend_down.get_frame()
        frame.set_edgecolor("white")
        
        plt.gca().add_artist(legend_down)
        
        legend = ax.legend(handles = [max_legend, min_legend], loc = 1, scatterpoints = 1)
        
        legend.get_texts()[0].set_color(discrete_cmap(self.ncol, self.init_cmap)[3])
        legend.get_texts()[1].set_color(discrete_cmap(self.ncol, self.init_cmap)[1])
        
        frame = legend.get_frame()
        frame.set_edgecolor("white")
        if not os.path.exists("results" + os.sep + proj_name):
            os.makedirs("results" + os.sep + proj_name)
        plt.savefig("results" + os.sep + proj_name + os.sep + "disp_" + results + ".png", DPI = 600)
        
        print("Saved results file", "[" + "disp_" + results + ".png] to results" + os.sep + proj_name + os.sep)
        
        
    def save_sresults(self, results, proj_name):
        
        """
        Matplotlib script for results viewing
        One element == one colour, so element solution
        """
    
        colors = []
        xs = [self.nodes[i][0] for i in self.nodes]
        ys = [-self.nodes[i][1] for i in self.nodes]
        
        fig, ax = plt.subplots()
        #ax.set_axis_bgcolor((0.0, 0.0, 0.0))
        patch_list = []
        
        min_x, min_y = self.eles[1][0][0], -self.eles[1][0][1]
        max_x, max_y = min_x, min_y
        
        counter = -1
        
        #Nodes coordinates storing
        for i in self.eles:
            counter += 1
            xlist = [self.eles[i][j][0] for j in range(0, 4)]
            ylist = [self.eles[i][j][1] for j in range(0, 4)]
    
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
            
            elif results == "tau_max":
                sigy = self.res[1][counter][1]
                sigx = self.res[1][counter][0]
                tauxy = self.res[1][counter][2] 
                taumax = math.sqrt((((sigx - sigy) / 2) ** 2) + (tauxy ** 2))
                colors.append(taumax)
                plt.title("Maximum shear stress")               
                
            elif results == "huber":
                sigy = self.res[1][counter][1]
                sigx = self.res[1][counter][0]
                tauxy = self.res[1][counter][2]    
                huber = math.sqrt((sigx ** 2) + (sigy ** 2) + (3 * (tauxy ** 2)))
                colors.append(huber)
                plt.title("Huber equivalent stress")
                
            elif results == "sign_huber":
                sigy = self.res[1][counter][1]
                sigx = self.res[1][counter][0]
                tauxy = self.res[1][counter][2] 
                taumax = math.sqrt((((sigx - sigy) / 2) ** 2) + (tauxy ** 2))
                sig1 = ((sigx + sigy) / 2) + taumax
                sig2 = ((sigx + sigy) / 2) - taumax
                sign = numpy.sign(sig1 + sig2)    
                sign_huber = sign * math.sqrt((sigx ** 2) + (sigy ** 2) + (3 * (tauxy ** 2)))                
                colors.append(sign_huber)
                plt.title("Signed Huber equivalent stress")
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
        dis_cmap = cmap=discrete_cmap(self.ncol, self.init_cmap)[0]
        
        #Hardcoded colors of color bar extensions
        #cmap.set_over([0.64705884,  0., 0.14901961, 1.])
        #cmap.set_under([0.19215687, 0.21176471, 0.58431375, 1.])
        cmap.set_over(discrete_cmap(self.ncol, self.init_cmap)[2])
        cmap.set_under(discrete_cmap(self.ncol, self.init_cmap)[1])
		
        p = PatchCollection(patch_list, cmap = dis_cmap, alpha = alpha)
        p.set_array(numpy.array(colors))
        ax.add_collection(p)
        
        #Plotting min/max
        minmax_data = minmax(colors, self.eles)
        
        x_pos_max = minmax_data[0]
        y_pos_max = minmax_data[1]
        max_string = minmax_data[2]
        x_pos_min = minmax_data[3]
        y_pos_min = minmax_data[4]
        min_string = minmax_data[5]
        
        logo_legend = plt.scatter(1e6, 1e6, marker = "None", label = "GRoT> ver. " + vers)
        
        plt.rcParams["patch.linewidth"] = 0.5
        if float(min_string) < 0 and float(max_string) >=	 0:
            max_legend = plt.scatter(x_pos_max, y_pos_max, marker = "^", c = "white", s = 52, label = "max:  " + str(max_string))
        else:
            max_legend = plt.scatter(x_pos_max, y_pos_max, marker = "^", c = "white", s = 52, label = "max: " + str(max_string))
        min_legend = plt.scatter(x_pos_min, y_pos_min, marker = "v", c = "white", s = 52, label = "min: " + str(min_string))
        plt.rcParams["patch.linewidth"] = patch_line
        
        #Color bar limits set to (mean + 2 * standard deviation)
        cbar_lim = [numpy.mean(colors) -  (2 * numpy.std(colors)),
                    numpy.mean(colors) + (2 * numpy.std(colors))]
            
        if (results == "sign_huber"):
            cbar_lim = [0 -  (2 * numpy.std(colors)),
                        0 + (2 * numpy.std(colors))]
        
        if (numpy.mean(colors) + (2 * numpy.std(colors))) >= float(max_string) and \
            (numpy.mean(colors) - (2 * numpy.std(colors))) > float(min_string):
            
            cbar_lim[1] = 1.0005 * float(max_string)
            cbar = plt.colorbar(p,
                                ticks = numpy.linspace(cbar_lim[0], 
                                                       cbar_lim[1], 
                                                       1 + self.ncol), 
                                extend='min')

            
        elif (numpy.mean(colors) - (2 * numpy.std(colors))) < float(min_string) and \
            (numpy.mean(colors) + (2 * numpy.std(colors))) <= float(max_string):
            
            cbar_lim[0] = 0.9995 * float(min_string)       
            cbar = plt.colorbar(p,
                                ticks = numpy.linspace(cbar_lim[0], 
                                                       cbar_lim[1], 
                                                       1 + self.ncol), 
                                extend='max')                
        
        else:
            cbar = plt.colorbar(p,
                                ticks = numpy.linspace(cbar_lim[0],
                                                       cbar_lim[1], 
                                                       1 + self.ncol), 
                                extend='both')
        
        if (results == "huber") and (numpy.mean(colors) - (2 * numpy.std(colors))) < 0:
            cbar_lim[0] = 0
                
        p.set_clim(cbar_lim)
        
        plt.xlim(min_x - 1, max_x + 1)
        plt.ylim(min_y - 1, max_y + 1)
        
        ax.axes.xaxis.set_ticks([])
        ax.axes.yaxis.set_ticks([])
        
        legend_down = plt.legend(handles = [logo_legend], loc = 4, scatterpoints = 1)
        frame = legend_down.get_frame()
        frame.set_edgecolor("white")
        
        plt.gca().add_artist(legend_down)
        
        legend = ax.legend(handles = [max_legend, min_legend], loc = 1, scatterpoints = 1)
        
        legend.get_texts()[0].set_color(discrete_cmap(self.ncol, self.init_cmap)[3])
        legend.get_texts()[1].set_color(discrete_cmap(self.ncol, self.init_cmap)[1])
        
        frame = legend.get_frame()
        frame.set_edgecolor("white")
        #plt.grid()
        if not os.path.exists("results" + os.sep + proj_name):
            os.makedirs("results" + os.sep + proj_name)
        plt.savefig("results" + os.sep + proj_name + os.sep + results + ".png", DPI = 600)
        
        print("Saved results file", "[" + results + ".png] to results" + os.sep + proj_name + os.sep)
