# Credit goes to simon at:
# https://stackoverflow.com/users/6356258/simon

from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
from enum import Enum

class Location(Enum):
    EastOutside = 1
    WestOutside = 2
    NorthOutside = 3
    SouthOutside = 4

class Legend:
    def __init__(self, figure, plotAxes, location: Location):
        self.figure = figure
        self.plotAxes = plotAxes
        self.location = location

        # Create a separate subplot for the legend. Actual location doesn't matter - will be modified anyway.
        self.legendAxes = figure.add_subplot(1, 2, 1)
        self.legendAxes.clear() # remove old lines
        self.legendAxes.set_axis_off()

        # Add all lines from the plot to the legend subplot
        for line in plotAxes.get_lines():
            legendLine = Line2D([], [])
            legendLine.update_from(line)
            self.legendAxes.add_line(legendLine)

        if self.location == Location.EastOutside:
            self.legend = self.legendAxes.legend(loc = "center left")
        elif self.location == Location.WestOutside:
            self.legend = self.legendAxes.legend(loc = "center right")
        elif self.location == Location.NorthOutside:
            self.legend = self.legendAxes.legend(loc = "lower center")
        elif self.location == Location.SouthOutside:
            self.legend = self.legendAxes.legend(loc = "upper center")
        else:
            raise Exception("Unknown legend location.")

        self.UpdateSize()

        # Recalculate legend size if the size changes
        figure.canvas.mpl_connect('resize_event', lambda event: self.UpdateSize())

    def UpdateSize(self):
        self.figure.canvas.draw() # draw everything once in order to get correct legend size

        # Extract legend size in percentage of the figure width
        legendSize = self.legend.get_window_extent().inverse_transformed(self.figure.transFigure)
        legendWidth = legendSize.width
        legendHeight = legendSize.height

        # Update subplot such that it is only as large as the legend
        if self.location == Location.EastOutside:
            gridspec = GridSpec(1, 2, width_ratios = [1 - legendWidth, legendWidth])
            legendLocation = 1
            plotLocation = 0
        elif self.location == Location.WestOutside:
            gridspec = GridSpec(1, 2, width_ratios = [legendWidth, 1 - legendWidth])
            legendLocation = 0
            plotLocation = 1
        elif self.location == Location.NorthOutside:
            gridspec = GridSpec(2, 1, height_ratios = [legendHeight, 1 - legendHeight])
            legendLocation = 0
            plotLocation = 1
        elif self.location == Location.SouthOutside:
            gridspec = GridSpec(2, 1, height_ratios = [1 - legendHeight, legendHeight])
            legendLocation = 1
            plotLocation = 0
        else:
            raise Exception("Unknown legend location.")

        self.legendAxes.set_position(gridspec[legendLocation].get_position(self.figure))
        self.legendAxes.set_subplotspec(gridspec[legendLocation]) # to make figure.tight_layout() work if that's desired

        self.plotAxes.set_position(gridspec[plotLocation].get_position(self.figure))
        self.plotAxes.set_subplotspec(gridspec[plotLocation]) # to make figure.tight_layout() work if that's desired
