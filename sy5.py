import copy

from prettytable import PrettyTable

from Grammar import Grammar

g = Grammar()
g.readFromList(["S->a|b|(B)", "A->S,A|S", "B->A"])

S = copy.deepcopy(g.S)
P = copy.deepcopy(g.P)
Vn = copy.deepcopy(g.Vn)
Vt = copy.deepcopy(g.Vt)

FIRSTVT = {i: set() for i in Vn}
LASTVT = {i: set() for i in Vn}


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
    _print = lambda x: " ".join(sorted(list(x)))
    for n in sorted(Vn):
        pt.add_row([n, _print(FIRSTVT.get(n)), _print(LASTVT.get(n))])
    print(pt)


create_VT()
print_VT()
print('Done')
