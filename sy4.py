import copy
from prettytable import PrettyTable


Vn = {'A', 'B', 'F', 'T', 'E'}
Vt = {'+', ')', '*', 'i', '('}
S = 'E'
P = {'E': {'TA'},
     'T': {'iB', '(E)B'},
     'F': {'(E)', 'i'},
     'A': {'+TA', '@'},
     'B': {'*FB', '@'}}

FIRST = {i: set() for i in Vn}
FOLLOW = {i: set() for i in Vn}
TABLE = {n: {t: "error" for t in Vt.union('#')} for n in Vn}


def FIRST_rule(vn: str, p: str):
    if (p == '@'):
        FIRST[vn].add('@')
    if not str.isupper(p[0]):
        FIRST[vn].add(p[0])
    if str.isupper(p[0]):
        FIRST[vn] = FIRST.get(vn).union(FIRST.get(p[0]))
        if '@' in P.get(p[0]):
            try:
                FIRST_rule(vn, p[1:])
            except IndexError:
                pass


def get_First(key: str) -> set:
    if (not str.isupper(key)):
        return {key}
    else:
        ret = FIRST.get(key).copy()
        ret.discard('@')
        return ret


def FOLLOW_rule(vn: str, p: str):
    if (vn == S):
        FOLLOW[vn].add('#')
    if (p != '@'):
        ind = 0
        try:
            while (True):
                if (str.isupper(p[ind])):
                    FOLLOW[p[ind]] = FOLLOW.get(p[ind]).union(get_First(p[ind + 1]))
                ind += 1
        except IndexError:
            pass
    if (str.isupper(p[-1])):
        FOLLOW[p[-1]] = FOLLOW.get(p[-1]).union(FOLLOW.get(vn))
        if ('@' in FIRST[p[-1]]):
            try:
                FOLLOW_rule(vn, p[:-1])
            except IndexError:
                pass


def find_p_first_Vt(p: str):
    if (p == '@'):
        return {p}
    if not str.isupper(p[0]):
        return {p[0]}
    if str.isupper(p[0]):
        return get_First(p[0])


def create_LL1_FL():
    while (True):
        last_FIRST = copy.deepcopy(FIRST)
        for i in Vn:
            for p in P[i]:
                FIRST_rule(i, p)
        if (last_FIRST == FIRST):
            break

    while (True):
        last_FOLLOW = copy.deepcopy(FOLLOW)
        for i in Vn:
            for p in P[i]:
                FOLLOW_rule(i, p)
        if (last_FOLLOW == FOLLOW):
            break


def print_LL1_FL():
    pt = PrettyTable()
    pt.field_names = ['非终结符', "FIRST", "FOLLOW"]
    for n in sorted(Vn):
        pt.add_row([n, FIRST.get(n), FOLLOW.get(n)])
    print(pt)


def create_LL1_table():
    for k, v in copy.deepcopy(P).items():
        if '@' in v:
            v.discard('@')
            Vts = FOLLOW.get(k)
            for t in Vts:
                TABLE[k][t] = "@"

        for p in v:
            Vts = find_p_first_Vt(p)
            for t in Vts:
                TABLE[k][t] = p


def print_LL1_table():
    pt = PrettyTable()
    vt = [t for t in Vt] + ['#']
    vt.sort()
    pt.field_names = ['非终结符'] + vt
    for n in sorted(Vn):
        pt.add_row([n] + [TABLE[n][t] for t in vt])
    print(pt)


def LL1Analyzer(table: dict, s: str, LexicalAnalyzerList: list):
    print(f"正在分析:")
    inputStack = ['i' if str.isdigit(item[0]) else item[0]
                  for item in LexicalAnalyzerList] + ['#']
    print(inputStack)
    analysisStack = ['#', s]
    done = lambda x, y: x[-1] == y[-1] == '#'
    try:
        while (not done(inputStack, analysisStack)):
            if (analysisStack[-1] == inputStack[0]):
                analysisStack.pop()
                inputStack.pop(0)
                continue
            p = table[analysisStack[-1]][inputStack[0]]
            if (p == 'error'):
                raise KeyError
            analysisStack.pop()
            if (p == '@'):
                continue
            analysisStack.extend(p[::-1])
    except KeyError:
        print("错误")
    else:
        print("正确")


create_LL1_FL()
print_LL1_FL()
create_LL1_table()
print_LL1_table()
from LexicalAnalyzer import LexicalAnalyzer

LL1Analyzer(TABLE, S, LexicalAnalyzer("((ab3+de4)*5)+1").result)
print("Done")
