from Grammar import *
from LL1Analyzer import *
from LexicalAnalyzer import *

g = Grammar()
g.readFromFile("input")
g.tran_LL1()
l = LL1Analyzer(g)
with open("Lexical") as f:
    for s in f.readlines():
        l.analyzer(LexicalAnalyzer(s).result)


