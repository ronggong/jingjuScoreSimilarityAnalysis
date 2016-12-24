# -*- coding: utf-8 -*-

from Bio.Phylo.TreeConstruction import _DistanceMatrix
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio.Phylo import draw_graphviz,draw
import pylab
import matplotlib.pyplot as plt

def buildTree(names,matrix):
    m = _DistanceMatrix(names,matrix)
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(m)
    return tree

def drawTree(tree):
    fig = plt.gcf()
    fig.set_size_inches(8*2, 6*2)

    # draw(tree)
    draw_graphviz(tree,node_size=0,font_size=10)
    plt.savefig("myplot.png", dpi = 300)