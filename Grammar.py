class Grammar:
    def __int__(self):
        pass

    Vn = set()
    Vt = set()
    S = None
    P = {}

    def __repr__(self):
        ls = [f"""{i[0]}->{"|".join(i[1])};""" for i in self.P.items()]
        ls.sort(key=lambda x: -1 if x[0] == self.S else 0)
        return "\n".join(ls)

    def readFromFile(self, filename: str):
        with open(filename) as f:
            for i in f.readlines():
                ls = i.strip("\n").strip(";").split("->")
                a = ls[0]
                if self.S is None:
                    self.S = a
                    start = 0
                b = ls[1].split("|")
                # 加入非终结符
                for j in a:
                    self.Vn.add(j)
                # 加入终结符
                # 加入产生式
                for j in b:
                    for k in j:
                        if k.islower():
                            self.Vt.add(k)
                    self.P[a] = self.P.get(a, set())
                    self.P[a].add(j)
            print(self)
            print()

    def __getNewVn(self):
        for i in range(ord("A"), ord("Z")):
            if chr(i) not in self.Vn:
                return chr(i)

    # p是产生式
    def __remove_left_recursion(self):
        backup = self.P.copy()
        VnList = list(self.Vn)
        print(VnList)
        ranges = range(len(VnList))
        for i in ranges:
            N = VnList[i]
            # 加入
            if (i == 0):
                continue
            else:
                _p = {VnList[j]: self.P[VnList[j]] for j in range(0, i)}
                p = self.P[N]
                while (True):
                    new_p = set()
                    for item in p:
                        # 检测左边是否存在非终结符
                        if str.isupper(item[0]) and item[0] != N and (item[0] in _p.keys()):
                            for i in _p[item[0]]:
                                new_p.add(i + item[1:])
                            # 注意！带入过一次不能再次带入，要删掉
                            _p.pop(item[0])
                        else:
                            new_p.add(item)
                    if (new_p == p):
                        self.P[N]=new_p
                        break
                    else:
                        p = new_p
            # 分类
            alpha = set()
            beta = set()
            for item in self.P[N]:
                if (item[0] == N):
                    alpha.add(item[1:])
                else:
                    beta.add(item)
            if (alpha == set()):
                continue
            # 构造新非终结符
            newVn = self.__getNewVn()
            self.Vn.add(newVn)
            self.P[newVn] = set([f"{i}{newVn}" for i in alpha])
            self.P[newVn].add("@")
            self.P[N] = set([f"{i}{newVn}" for i in beta])

    def __remove_left_gene(self):
        while (True):
            old_vn_set = self.Vn.copy()
            for N in self.Vn.copy():
                # 找出有左递归的那个非终结符
                while (True):
                    p = self.P[N]
                    found = None
                    head_ch = set()
                    for item in p:
                        if item[0] in head_ch:
                            found = item[0]
                            break
                        else:
                            head_ch.add(item[0])
                    if found is None:
                        break
                    beta = set()
                    gama = set()
                    for item in p:
                        if (item[0] == found):
                            if (item[1:] == ''):
                                beta.add("@")
                            else:
                                beta.add(item[1:])
                        else:
                            gama.add(item)
                    new_Vn = self.__getNewVn()
                    gama.add(f"{found}{new_Vn}")
                    self.P[N] = gama
                    self.Vn.add(new_Vn)
                    self.P[new_Vn] = beta
            if (old_vn_set == self.Vn):
                break

    def tran_LL1(self):
        self.__remove_left_recursion()
        self.__remove_left_gene()
        print(self)
