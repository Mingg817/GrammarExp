from Grammar import *

g = Grammar()
g.readFromFile("input")

g.tran_LL1()
