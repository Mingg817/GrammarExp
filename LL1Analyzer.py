import copy

from prettytable import PrettyTable

from Grammar import Grammar


class LL1Analyzer:
    def __init__(self, grammar: Grammar):
        self.Vn = copy.deepcopy(grammar.Vn)
        self.Vt = copy.deepcopy(grammar.Vt)
        self.S = copy.deepcopy(grammar.S)
        self.P = copy.deepcopy(grammar.P)
        self.FIRST = {i: set() for i in self.Vn}
        self.FOLLOW = {i: set() for i in self.Vn}
        self.TABLE = {n: {t: "error" for t in self.Vt.union('#')} for n in self.Vn}

        self.__create_LL1_FL()
        self.__create_LL1_table()
        print("- FIRST和FOLLOW集：")
        self.print_LL1_FL()
        print("- LL1分析表：")
        self.print_LL1_table()

    def __FIRST_rule(self, vn: str, p: str):
        if (p == '@'):
            self.FIRST[vn].add('@')
        if not str.isupper(p[0]):
            self.FIRST[vn].add(p[0])
        if str.isupper(p[0]):
            self.FIRST[vn] = self.FIRST.get(vn).union(self.FIRST.get(p[0]))
            if '@' in self.P.get(p[0]):
                try:
                    self.__FIRST_rule(vn, p[1:])
                except IndexError:
                    pass

    def __get_First(self, key: str) -> set:
        if (not str.isupper(key)):
            return {key}
        else:
            ret = self.FIRST.get(key).copy()
            ret.discard('@')
            return ret

    def __FOLLOW_rule(self, vn: str, p: str):
        if (vn == self.S):
            self.FOLLOW[vn].add('#')
        if (p != '@'):
            ind = 0
            try:
                while (True):
                    if (str.isupper(p[ind])):
                        self.FOLLOW[p[ind]] = self.FOLLOW.get(p[ind]).union(self.__get_First(p[ind + 1]))
                    ind += 1
            except IndexError:
                pass
        if (str.isupper(p[-1])):
            self.FOLLOW[p[-1]] = self.FOLLOW.get(p[-1]).union(self.FOLLOW.get(vn))
            if ('@' in self.FIRST[p[-1]]):
                try:
                    self.__FOLLOW_rule(vn, p[:-1])
                except IndexError:
                    pass

    def __find_p_first_Vt(self, p: str):
        if (p == '@'):
            return {p}
        if not str.isupper(p[0]):
            return {p[0]}
        if str.isupper(p[0]):
            return self.__get_First(p[0])

    def __create_LL1_FL(self):
        while (True):
            last_FIRST = copy.deepcopy(self.FIRST)
            for i in self.Vn:
                for p in self.P[i]:
                    self.__FIRST_rule(i, p)
            if (last_FIRST == self.FIRST):
                break

        while (True):
            last_FOLLOW = copy.deepcopy(self.FOLLOW)
            for i in self.Vn:
                for p in self.P[i]:
                    self.__FOLLOW_rule(i, p)
            if (last_FOLLOW == self.FOLLOW):
                break

    def print_LL1_FL(self):
        pt = PrettyTable()
        pt.field_names = ['非终结符', "FIRST集", "FOLLOW集"]
        for n in sorted(self.Vn):
            def _print(x): " ".join(sorted(list(x)))

            pt.add_row([n, _print(self.FIRST.get(n)), _print(self.FOLLOW.get(n))])
        print(pt)

    def __create_LL1_table(self):
        for k, v in copy.deepcopy(self.P).items():
            if '@' in v:
                v.discard('@')
                Vts = self.FOLLOW.get(k)
                for t in Vts:
                    self.TABLE[k][t] = "@"

            for p in v:
                Vts = self.__find_p_first_Vt(p)
                for t in Vts:
                    self.TABLE[k][t] = p

    def print_LL1_table(self):
        pt = PrettyTable()
        vt = [t for t in self.Vt] + ['#']
        vt.sort()
        pt.field_names = ['非终结符'] + vt
        for n in sorted(self.Vn):
            pt.add_row([n] + [self.TABLE[n][t] for t in vt])
        print(pt)

    def analyzer(self, LexicalAnalyzerResult: list):
        print(f"- 正在分析:", end=" ")
        inputStack = ['i' if str.isdigit(item[0]) else item[0]
                      for item in LexicalAnalyzerResult] + ['#']
        print(inputStack)
        analysisStack = ['#', self.S]

        def done(x, y):
            return x[0] == y[-1] == '#'

        try:
            while (not done(inputStack, analysisStack)):
                if (analysisStack[-1] == inputStack[0]):
                    analysisStack.pop()
                    inputStack.pop(0)
                    continue
                p = self.TABLE[analysisStack[-1]][inputStack[0]]
                if (p == 'error'):
                    raise KeyError
                analysisStack.pop()
                if (p == '@'):
                    continue
                analysisStack.extend(p[::-1])
        except KeyError:
            print("错误!")
        else:
            print("正确!")
