"""Postprocessor module for deformed view plotting"""

import math
import os
import numpy
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import version

VERS = version.get()
PATCH_LINE = 0.0

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
    """Create an n-div discrete colormap from the specified input map"""
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(numpy.linspace(1 - (1 / ndiv), 1 / ndiv, ndiv))
    color_list[3] = [.918, .918, .918, 1.]
    #For edge colors retrieving: 0 is for max, 1 is for min, 2 is for min label
    down_up = [base(numpy.linspace(1 - (0.2 / ndiv), 0.2 / ndiv, ndiv))[0],
               base(numpy.linspace(1 - (0.2 / ndiv), 0.2 / ndiv, ndiv))[-1],
               base(numpy.linspace(1 - (0.2 / ndiv), 0.2 / ndiv, ndiv))[-1]]
    cmap_name = base.name + str(ndiv)
    return [clr.LinearSegmentedColormap.from_list(cmap_name, color_list, ndiv),
            down_up[0], down_up[1], down_up[2]]

class Prepare():
    """Prepares whole matplotlib enviroment for postprocessing"""
    def __init__(self, elements, results, scale):
        self.eles = elements
        self.res = results
        self.ncol = 7
        self.init_cmap = "coolwarm_r"
        self.scale = scale

    def save_deformed(self, results, proj_name):
        """Matplotlib script for results viewing
        One element == one colour, so element solution"""

        colors = []
        fig, axes = plt.subplots()
        deformed_points_x, deformed_points_y = [], []
        deformed_points_colors = []
        center_points_x, center_points_y = [], []

        #Nodes coordinates storing
        for i in self.eles:
            xlist = [self.eles[i][j][0] for j in range(0, 4)]
            ylist = [self.eles[i][j][1] for j in range(0, 4)]

            #Rectangle of vertex in (x, y) and given width and height
            center_points_x.append((min(xlist) + 0.5))
            center_points_y.append((-1 * min(ylist) - 0.5))

            #Displacement results storing
            dof1 = (self.eles[i][4] * 2) - 2
            dof2 = (self.eles[i][5] * 2) - 2
            dof3 = (self.eles[i][6] * 2) - 2
            dof4 = (self.eles[i][7] * 2) - 2
            dofs = [dof1, dof1 + 1, dof2, dof2 + 1, dof3, dof3 + 1, dof4, dof4 + 1]

            #Results choosing and preparing
            if results == "deformed":
                colors.append(0)
                deformed_points_colors.append(0.25 * (math.sqrt((self.res[dofs[0]] ** 2) +
                                                                (self.res[dofs[1]] ** 2)) +
                                                      math.sqrt((self.res[dofs[2]] ** 2) +
                                                                (self.res[dofs[3]] ** 2)) +
                                                      math.sqrt((self.res[dofs[4]] ** 2) +
                                                                (self.res[dofs[5]] ** 2)) +
                                                      math.sqrt((self.res[dofs[6]] ** 2) +
                                                                (self.res[dofs[7]] ** 2))))
                deformed_points_x.append(0.25 * (self.res[dofs[0]] + self.res[dofs[2]] +
                                                 self.res[dofs[4]] + self.res[dofs[6]]))
                deformed_points_y.append(0.25 * (self.res[dofs[1]] + self.res[dofs[3]] +
                                                 self.res[dofs[5]] + self.res[dofs[7]]))
                title = "Deformed shape (displacement magnitude)"
                plt.title(title)

        #Deformed shape
        if results == "deformed":
            max_deformed = max(deformed_points_x + deformed_points_y)
            for j in range(len(deformed_points_x)):
                deformed_points_x[j] = (self.scale * deformed_points_x[j] / max_deformed) + \
                                       center_points_x[j]
                deformed_points_y[j] = (self.scale * deformed_points_y[j] / max_deformed) + \
                                       center_points_y[j]
            scatter = plt.scatter(deformed_points_x, deformed_points_y, c=deformed_points_colors,
                                  cmap=discrete_cmap(self.ncol, self.init_cmap)[0])
        #Axes range
        max_y = max(deformed_points_y)
        min_y = min(deformed_points_y)
        max_x = max(deformed_points_x)
        min_x = min(deformed_points_x)
        diff_x = max(deformed_points_x) - min(deformed_points_x)
        diff_y = max(deformed_points_y) - min(deformed_points_y)
        sum_x = max(deformed_points_x) + min(deformed_points_x)
        sum_y = max(deformed_points_y) + min(deformed_points_y)

        if diff_x > diff_y:
            max_y = (sum_y / 2) + (diff_x / 2)
            min_y = (sum_y / 2) - (diff_x / 2)
        else:
            max_x = (sum_x / 2) + (diff_y / 2)
            min_x = (sum_x / 2) - (diff_y / 2)

        minmax_data = minmax(deformed_points_colors, self.eles)

        x_pos_max = minmax_data[0]
        y_pos_max = minmax_data[1]
        max_string = minmax_data[2]
        min_string = minmax_data[5]
        logo_legend = plt.scatter(1e6, 1e6, marker="None", label="GRoT> ver. " + VERS)
        plt.rcParams["patch.linewidth"] = 0.5
        if float(min_string) < 0 <= float(max_string):
            max_legend = plt.scatter(x_pos_max, y_pos_max, marker="^", c="white", s=52,
                                     label="max:  " + str(max_string))
        else:
            max_legend = plt.scatter(99999, 99999, marker="^", c="white", s=52,
                                     label="max: " + str(max_string))
        min_legend = plt.scatter(-99999, -99999, marker="v", c="white", s=52,
                                 label="min: " + str(min_string))
        plt.rcParams["patch.linewidth"] = PATCH_LINE
        cbar_lim = [min(deformed_points_colors), max(deformed_points_colors)]
        plt.colorbar(scatter, ticks=numpy.linspace(cbar_lim[0], cbar_lim[1], 1 + self.ncol))
        plt.xlim(min_x - 1, max_x + 1)
        plt.ylim(min_y - 1, max_y + 1)

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

        print("Plotted deformed view",
              "[" + results + ".png] to results" + os.sep + proj_name + os.sep)
        return title
