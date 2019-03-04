"""Postprocessor module used to plot pictures"""

import math
import os
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as clr
from matplotlib.collections import PatchCollection
import tools
import version
import stress

VERS = version.get()

#Matplotlib style functions
PATCH_LINE = 0.0
ALPHA = 1.0
plt.rcParams["font.family"] = "monospace"
plt.rcParams["font.size"] = 10
plt.rcParams["font.weight"] = 100
plt.rcParams["text.hinting_factor"] = 1
plt.rcParams["patch.linewidth"] = PATCH_LINE
plt.rcParams["legend.fontsize"] = 9

def minmax(colors, eles):
    """Min and max scatter plotting"""
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

def discrete_cmap(ndiv, base_cmap=None):
    """Create an n-bin discrete colormap from the specified input map"""
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(numpy.linspace(1 - (1 / ndiv), 1 / ndiv, ndiv))
    color_list[3] = [.906, .906, .906, 1.]
    #For edge colors retrieving: 0 is for max, 1 is for min, 2 is for min label
    down_up = [base(numpy.linspace(1 - (0.2 / ndiv), 0.2 / ndiv, ndiv))[0],
               base(numpy.linspace(1 - (0.2 / ndiv), 0.2 / ndiv, ndiv))[-1],
               base(numpy.linspace(1 - (0.2 / ndiv), 0.2 / ndiv, ndiv))[-1]]
    cmap_name = base.name + str(ndiv)
    return [clr.LinearSegmentedColormap.from_list(cmap_name, color_list, ndiv),
            down_up[0], down_up[1], down_up[2]]

class Prepare():
    """Prepares whole matplotlib enviroment for postprocessing"""
    def __init__(self, elements, results):
        self.eles = elements
        self.res = results
        self.ncol = 7
        self.init_cmap = "coolwarm_r"
        self.min_x, self.min_y = self.eles[1][0][0], -self.eles[1][0][1]
        self.max_x, self.max_y = self.min_x, self.min_y
        self.elen = len(elements)

        self.patch_list = []
        for i in self.eles:
            xlist = [self.eles[i][j][0] for j in range(0, 4)]
            ylist = [self.eles[i][j][1] for j in range(0, 4)]

            #Rectangle of vertex in (x, y) and given width and height
            self.patch_list.append(patches.Rectangle((min(xlist), -min(ylist)), 1.0, -1.0))

            #Axes limits searching
            self.min_x = tools.min_search(min(xlist), self.min_x)
            self.min_y = tools.min_search(-max(ylist), self.min_y)
            self.max_x = tools.max_search(max(xlist), self.max_x)
            self.max_y = tools.max_search(-min(ylist), self.max_y)

            #Axes range
            diff_x = self.max_x - self.min_x
            diff_y = self.max_y - self.min_y
            sum_x = self.max_x + self.min_x
            sum_y = self.max_y + self.min_y

            if diff_x > diff_y:
                self.max_y = (sum_y / 2) + (diff_x / 2)
                self.min_y = (sum_y / 2) - (diff_x / 2)
            else:
                self.max_x = (sum_x / 2) + (diff_y / 2)
                self.min_x = (sum_x / 2) - (diff_y / 2)

    def save_dresults(self, results, proj_name):
        """Matplotlib script for results viewing
        One element == one colour, so element solution
        Reduced integration (so there are no other possibilities)"""

        colors = []
        fig, axes = plt.subplots()

        #Nodes coordinates storing
        for i in self.eles:

            #Displacement results storing
            dof1 = (self.eles[i][4] * 2) - 2
            dof2 = (self.eles[i][5] * 2) - 2
            dof3 = (self.eles[i][6] * 2) - 2
            dof4 = (self.eles[i][7] * 2) - 2
            dofs = [dof1, dof1 + 1, dof2, dof2 + 1, dof3, dof3 + 1, dof4, dof4 + 1]

            #Results choosing and preparing
            if results == "x":
                colors.append(0.25 * (self.res[dofs[0]] + self.res[dofs[2]] + \
                                      self.res[dofs[4]] + self.res[dofs[6]]))
                title = "Displacement in X direction"
            elif results == "y":
                colors.append(0.25 * (self.res[dofs[1]] + self.res[dofs[3]] + \
                                      self.res[dofs[5]] + self.res[dofs[7]]))
                title = "Displacement in Y direction"
            elif results in ["mag", "res"]:
                colors.append(0.25 * (math.sqrt((self.res[dofs[0]] ** 2) +
                                                (self.res[dofs[1]] ** 2)) +
                                      math.sqrt((self.res[dofs[2]] ** 2) +
                                                (self.res[dofs[3]] ** 2)) +
                                      math.sqrt((self.res[dofs[4]] ** 2) +
                                                (self.res[dofs[5]] ** 2)) +
                                      math.sqrt((self.res[dofs[6]] ** 2) +
                                                (self.res[dofs[7]] ** 2))))
                if results == "mag":
                    title = "Displacement magnitude"
                elif results == "res":
                    title = "Residual displacement magnitude"
            plt.title(title)

        #Matplotlib functions
        dis_cmap = discrete_cmap(self.ncol, self.init_cmap)[0]
        p_col = PatchCollection(self.patch_list, cmap=dis_cmap, alpha=ALPHA)
        p_col.set_array(numpy.array(colors))
        axes.add_collection(p_col)

        #Plotting min/max
        minmax_data = minmax(colors, self.eles)
        x_pos_max = minmax_data[0]
        y_pos_max = minmax_data[1]
        max_string = minmax_data[2]
        x_pos_min = minmax_data[3]
        y_pos_min = minmax_data[4]
        min_string = minmax_data[5]

        logo_legend = plt.scatter(1e6, 1e6, marker="None", label="GRoT> ver. " + VERS)

        #Markers border width change
        plt.rcParams["patch.linewidth"] = 0.5
        if float(min_string) < 0 <= float(max_string):
            max_legend = plt.scatter(x_pos_max, y_pos_max, marker="^", c="white",
                                     edgecolors="black", s=52, label="max:  " + str(max_string))
        else:
            max_legend = plt.scatter(x_pos_max, y_pos_max, marker="^", c="white",
                                     edgecolors="black", s=52, label="max: " + str(max_string))
        min_legend = plt.scatter(x_pos_min, y_pos_min, marker="v", c="white",
                                 edgecolors="black", s=52, label="min: " + str(min_string))
        plt.rcParams["patch.linewidth"] = PATCH_LINE

        cbar_lim = [min(colors), max(colors)]
        plt.colorbar(p_col, ticks=numpy.linspace(cbar_lim[0], cbar_lim[1], 1 + self.ncol))
        p_col.set_clim(cbar_lim)

        plt.xlim(self.min_x - 1, self.max_x + 1)
        plt.ylim(self.min_y - 1, self.max_y + 1)

        axes.axes.xaxis.set_ticks([])
        axes.axes.yaxis.set_ticks([])

        legend_down = plt.legend(handles=[logo_legend], loc=4, scatterpoints=1)
        frame = legend_down.get_frame()
        frame.set_edgecolor("white")
        plt.gca().add_artist(legend_down)
        legend = axes.legend(handles=[max_legend, min_legend], loc=1, scatterpoints=1)
        legend.get_texts()[0].set_color(discrete_cmap(self.ncol, self.init_cmap)[3])
        legend.get_texts()[1].set_color(discrete_cmap(self.ncol, self.init_cmap)[1])

        frame = legend.get_frame()
        frame.set_edgecolor("white")
        if not os.path.exists("results" + os.sep + proj_name):
            os.makedirs("results" + os.sep + proj_name)
        plt.savefig("results" + os.sep + proj_name + os.sep + "disp_" + results + ".png", DPI=300)
        plt.close()
        fig, axes = None, None
        return title

    def save_sresults(self, results, proj_name):
        """Matplotlib script for results viewing
        One element == one colour, so element solution"""

        dev_factor = 2
        colors = []
        fig, axes = plt.subplots()

        counter = -1

        #Nodes coordinates storing
        for i in range(self.elen):
            counter += 1
            #Results choosing and preparing
            to_plot = stress.results(self.res, results, i)
            colors.append(to_plot[0])
        plt.title(to_plot[1])
        title = to_plot[1]
        #Matplotlib functions
        dis_cmap = discrete_cmap(self.ncol, self.init_cmap)[0]

        #Hardcoded colors of color bar extensions
        dis_cmap.set_over(discrete_cmap(self.ncol, self.init_cmap)[2])
        dis_cmap.set_under(discrete_cmap(self.ncol, self.init_cmap)[1])

        p_col = PatchCollection(self.patch_list, cmap=dis_cmap, alpha=ALPHA)
        p_col.set_array(numpy.array(colors))
        axes.add_collection(p_col)

        #Plotting min/max
        minmax_data = minmax(colors, self.eles)

        x_pos_max = minmax_data[0]
        y_pos_max = minmax_data[1]
        max_string = minmax_data[2]
        x_pos_min = minmax_data[3]
        y_pos_min = minmax_data[4]
        min_string = minmax_data[5]

        logo_legend = plt.scatter(1e6, 1e6, marker="None", label="GRoT> ver. " + VERS)

        plt.rcParams["patch.linewidth"] = 0.5
        if float(min_string) < 0 <= float(max_string):
            max_legend = plt.scatter(x_pos_max, y_pos_max, marker="^", c="white",
                                     edgecolors="black", s=52, label="max:  " + str(max_string))
        else:
            max_legend = plt.scatter(x_pos_max, y_pos_max, marker="^", c="white",
                                     edgecolors="black", s=52, label="max: " + str(max_string))
        min_legend = plt.scatter(x_pos_min, y_pos_min, marker="v", c="white",
                                 edgecolors="black", s=52, label="min: " + str(min_string))
        plt.rcParams["patch.linewidth"] = PATCH_LINE

        #Color bar limits set to (mean + (dev_factor) * standard deviation)
        cbar_lim = [numpy.mean(colors) -  (dev_factor * numpy.std(colors)),
                    numpy.mean(colors) + (dev_factor * numpy.std(colors))]

        #Zero has to be in the middle!
        if results == "sign_huber":
            cbar_lim = [0 - (dev_factor * numpy.std(colors)),
                        0 + (dev_factor * numpy.std(colors))]

        if (numpy.mean(colors) + (dev_factor * numpy.std(colors))) >= float(max_string) and \
            (numpy.mean(colors) - (dev_factor * numpy.std(colors))) > float(min_string):

            cbar_lim[1] = 1.0005 * float(max_string)
            plt.colorbar(p_col, ticks=numpy.linspace(cbar_lim[0], cbar_lim[1], 1 + self.ncol),
                         extend='min')

        elif (numpy.mean(colors) - (dev_factor * numpy.std(colors))) < float(min_string) and \
            (numpy.mean(colors) + (dev_factor * numpy.std(colors))) <= float(max_string):

            cbar_lim[0] = 0.9995 * float(min_string)
            plt.colorbar(p_col, ticks=numpy.linspace(cbar_lim[0], cbar_lim[1], 1 + self.ncol),
                         extend='max')

        else:
            plt.colorbar(p_col, ticks=numpy.linspace(cbar_lim[0], cbar_lim[1], 1 + self.ncol),
                         extend='both')

        if (results in ["huber", "eff_strain"]) and (numpy.mean(colors) - \
                                                    (dev_factor * numpy.std(colors))) < 0:
            cbar_lim[0] = 0

        p_col.set_clim(cbar_lim)

        plt.xlim(self.min_x - 1, self.max_x + 1)
        plt.ylim(self.min_y - 1, self.max_y + 1)

        axes.axes.xaxis.set_ticks([])
        axes.axes.yaxis.set_ticks([])

        legend_down = plt.legend(handles=[logo_legend], loc=4, scatterpoints=1)
        frame = legend_down.get_frame()
        frame.set_edgecolor("white")
        plt.gca().add_artist(legend_down)
        legend = axes.legend(handles=[max_legend, min_legend], loc=1, scatterpoints=1)
        legend.get_texts()[0].set_color(discrete_cmap(self.ncol, self.init_cmap)[3])
        legend.get_texts()[1].set_color(discrete_cmap(self.ncol, self.init_cmap)[1])

        frame = legend.get_frame()
        frame.set_edgecolor("white")

        if not os.path.exists("results" + os.sep + proj_name):
            os.makedirs("results" + os.sep + proj_name)
        plt.savefig("results" + os.sep + proj_name + os.sep + results + ".png", DPI=300)
        plt.close()
        fig, axes = None, None
        return title
