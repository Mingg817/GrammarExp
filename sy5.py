import copy

from prettytable import PrettyTable

from Grammar import Grammar
from LexicalAnalyzer import LexicalAnalyzer

g = Grammar()
g.readFromList(["S->a|b|(B)", "A->S,A|S", "B->A"])

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

    def _print(x): " ".join(sorted(list(x)))

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
    print(LexicalAnalyzerResult)


create_VT()
print_VT()
create_OP_table()
print_OP_tabel()

analyzer(LexicalAnalyzer("1+1").result)
print('Done')
