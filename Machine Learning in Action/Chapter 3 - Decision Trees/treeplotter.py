import matplotlib.pyplot as plt

decisionNode = dict(boxstyle = "sawtooth", fc = "0.8");
leafNode = dict(boxstyle = "round4", fc = "0.8");
arrow_args = dict(arrowstyle = "<-");

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeType, xy=parentPt, xycoords='axes fraction', xytext=centerPt, ha="center", textcoords='axes fraction', va="center", ha="center", bbox=nodeType, arrowprop=arrow_args);
