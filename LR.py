from prettytable import PrettyTable

import LexicalAnalyzer

P = [('E', 'E+T'),
     ('E', 'T'),
     ('T', 'T*F'),
     ('T', 'F'),
     ('F', '(E)'),
     ('F', 'i')]

TABLE = {
    0: {'i': 's5', '(': 's4', 'E': 1, 'T': 2, 'F': 3},
    1: {'+': 's6', '#': 'acc'},
    2: {'+': 'r2', '*': 's7', ')': 'r2', '#': 'r2'},
    3: {'+': 'r4', '*': 'r4', ')': 'r4', '#': 'r4'},
    4: {'i': 's5', '(': 's4', 'E': 8, 'T': 2, 'F': 3},
    5: {'+': 'r6', '*': 'r6', ')': 'r6', '#': 'r6'},
    6: {'i': 's5', '(': 's4', 'T': 9, 'F': 3},
    7: {'i': 's5', '(': 's4', 'F': 10},
    8: {'+': 's6', ')': 's11'},
    9: {'+': 'r1', '*': 's7', ')': 'r1', '#': 'r1'},
    10: {'+': 'r3', '*': 'r3', ')': 'r3', '#': 'r3'},
    11: {'+': 'r5', '*': 'r5', ')': 'r5', '#': 'r5'}
}

L = LexicalAnalyzer.LexicalAnalyzer("1*2+3").result


def analyst(LexicalAnalyzerResult):
    inputStack = ['i' if str.isdigit(item[0]) else item[0]
                  for item in LexicalAnalyzerResult] + ['#']
    print(inputStack)
    status = [0]
    analystStack = ['#']
    pt = PrettyTable()
    pt.field_names = ['Status', 'AnalystStack', "InputStack"]
    try:
        while (1):
            result = TABLE[status[-1]][inputStack[0]]
            if (result == 'acc'):
                break
            if (result[0] == 's'):
                status.append(int(result[1:]))
                analystStack.append(inputStack.pop(0))
            if (result[0] == 'r'):
                p = P[int(result[-1]) - 1]
                analystStack = analystStack[0:-(len(p[-1]))]
                status = status[0:-(len(p[-1]))]
                analystStack.append(p[0])
                status.append(TABLE[status[-1]][p[0]])
            pt.add_row([status.copy(), analystStack.copy(), inputStack.copy()])
    except:
        print("错误!")
        # print(pt)
    else:
        print("正确!")
        # print(pt)

with open("Lexical") as f:
    for s in f.readlines():
        analyst(LexicalAnalyzer.LexicalAnalyzer(s).result)

# analyst(LexicalAnalyzer.LexicalAnalyzer('1*2+3').result)

