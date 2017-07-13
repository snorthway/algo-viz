# Defines nice colors and stuff.
class PlotStyle:
    BG = '#1A463B' # dork blue
    BLUE = '#35D1AA' # loight blue
    RED = '#F73E5F' # read
    ORANGE = '#E98144' # oragne

    @staticmethod
    def apply(plot_object):
        plot_object.set_facecolor(PlotStyle.BG)
        plot_object.xaxis.set_visible(False)
        plot_object.yaxis.set_visible(False)