import copy

from prettytable import PrettyTable

from Grammar import Grammar
from LexicalAnalyzer import LexicalAnalyzer

g = Grammar()
g.readFromList(["E->T|E+T", "T->F|T*F;", "F->i|(E)"])

S = copy.deepcopy(g.S)
P = copy.deepcopy(g.P)
Vn = copy.deepcopy(g.Vn)
Vt = copy.deepcopy(g.Vt)

FIRSTVT = {i: set() for i in Vn}
LASTVT = {i: set() for i in Vn}
TABLE = {n: {t: set() for t in Vt} for n in Vt}


def FIRSTVT_rule(vn: str, p: str):
    if (p == '@'):
        raise KeyError
    if (not str.isupper(p[0])):
        FIRSTVT[vn] = FIRSTVT[vn].union(p[0])
    if (str.isupper(p[0])):
        FIRSTVT[vn] = FIRSTVT[vn].union(FIRSTVT[p[0]])
        try:
            if (not str.isupper(p[1])):
                FIRSTVT[vn] = FIRSTVT[vn].union(p[1])
        except IndexError:
            pass


def LASTVT_rule(vn: str, p: str):
    if (p == '@'):
        raise KeyError
    if (not str.isupper(p[-1])):
        LASTVT[vn] = LASTVT[vn].union(p[-1])
    if (str.isupper(p[-1])):
        LASTVT[vn] = LASTVT[vn].union(LASTVT[p[-1]])
        try:
            if (not str.isupper(p[-2])):
                LASTVT[vn] = LASTVT[vn].union(p[-2])
        except IndexError:
            pass


def create_VT():
    while (True):
        last_FIRSTVT = copy.deepcopy(FIRSTVT)
        for i in Vn:
            for p in P[i]:
                FIRSTVT_rule(i, p)
        if (last_FIRSTVT == FIRSTVT):
            break
    while (True):
        last_LASTVT = copy.deepcopy(LASTVT)
        for i in Vn:
            for p in P[i]:
                LASTVT_rule(i, p)
        if (last_LASTVT == LASTVT):
            break


def print_VT():
    pt = PrettyTable()
    pt.field_names = ['非终结符', "FIRSTVT", "LASTVT"]

    def _print(x): return " ".join(sorted(list(x)))

    for n in sorted(Vn):
        pt.add_row([n, _print(FIRSTVT.get(n)), _print(LASTVT.get(n))])
    print(pt)


def create_OP_table():
    for k, v in copy.deepcopy(P).items():
        for p in v:
            ind = 0
            while (True):
                try:
                    if (not str.isupper(p[ind])) and (str.isupper(p[ind + 1])):
                        for item in FIRSTVT[p[ind + 1]]:
                            TABLE[p[ind]][item] = '<'
                    if (str.isupper(p[ind])) and (not str.isupper(p[ind + 1])):
                        for item in LASTVT[p[ind]]:
                            TABLE[item][p[ind + 1]] = '>'
                    if (not str.isupper(p[ind])) and (not str.isupper(p[ind + 2])):
                        TABLE[p[ind]][p[ind + 2]] = '='
                except IndexError:
                    break
                else:
                    ind += 1


def print_OP_tabel():
    pt = PrettyTable()
    vt = sorted(list(Vt))
    vt.sort()
    pt.field_names = ['TABLE'] + vt
    for n in vt:
        pt.add_row([n] + ['\033[1m' + TABLE[n][t] + '\033[0m' if TABLE[n][t] != set() else " " for t in vt])
    print(pt)


def analyzer(LexicalAnalyzerResult: list):
    print(f"- 正在分析:", end=" ")
    inputStack = ['i' if str.isdigit(item[0]) else item[0]
                  for item in LexicalAnalyzerResult] + ['#']
    print(inputStack)
    analysisStack = ['#', inputStack.pop(0)]

    T_TABEL = {}
    for k, v in P.items():
        for item in v:
            for i in item:
                if (not str.isupper(i)):
                    T_TABEL[i] = (k, item)

    def done(x, y):
        if (y == ['#'] and len(x) < 3 and x[0] == '#' and str.isupper(x[1])):
            return True
        else:
            return False

    def check(analysisStack, inputStack):
        """
        :param analysisStack:
        :param inputStack:
        :return: -1 < | 0 = | 1 >
        """
        a = analysisStack.copy()
        b = inputStack[0]
        while (str.isupper(a[-1])):
            a.pop()
        a = a[-1]
        if (b == '#'):
            return 1, a
        if (a[-1] == '#'):
            return -1, a
        r = TABLE[a][b]
        if (r == '='):
            return 0, a
        elif (r == '<'):
            return -1, a
        elif (r == '>'):
            return 1, a
        else:
            raise KeyError

    try:
        while (not done(analysisStack, inputStack)):
            result, t = check(analysisStack, inputStack)
            if (result == -1 or result == 0):
                analysisStack.append(inputStack.pop(0))
            if (result == 1):
                n, p = T_TABEL[t]
                analysisStack = analysisStack[:-(len(p))]
                analysisStack.append(n)

    except KeyError:
        print("错误!")
    except IndexError:
        print("错误!")
    else:
        print("正确!")


create_VT()
print_VT()
create_OP_table()
print_OP_tabel()

analyzer(LexicalAnalyzer("(1+2)*3+(5+6*7)").result)
print('Done')
