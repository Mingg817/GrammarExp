from Grammar import *
from LL1Analyzer import *
from LexicalAnalyzer import *

g = Grammar()
g.readFromFile("input")
g.tran_LL1()
l = LL1Analyzer(g)
l.analyzer(LexicalAnalyzer("10").result)
l.analyzer(LexicalAnalyzer("1+2").result)
l.analyzer(LexicalAnalyzer("(1+2)*3+(5+6*7)").result)
l.analyzer(LexicalAnalyzer("((1+2)*3+4").result)
l.analyzer(LexicalAnalyzer("1+2+3+(*4+5)").result)
l.analyzer(LexicalAnalyzer("(a+b)*(c+d)").result)
l.analyzer(LexicalAnalyzer("((ab3+de4)**5)+1").result)

