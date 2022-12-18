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

    def readFromList(self,l:list):
        for i in l:
            ls = i.strip("\n").strip(";").split("->")
            a = ls[0]
            if self.S is None:
                self.S = a
            b = ls[1].split("|")
            # 加入非终结符
            self.Vn.add(a)
            # 加入终结符
            for j in b:
                for item in j:
                    if not str.isupper(item):
                        self.Vt.add(item)
            # 加入产生式
            for j in b:
                for k in j:
                    if k.islower():
                        self.Vt.add(k)
                self.P[a] = self.P.get(a, set())
                self.P[a].add(j)
        print(self)
        print()

    def readFromFile(self, filename: str):
        try:
            with open(filename) as f:
                self.readFromList(f.readlines())
        except IOError:
            print("读取文件失败！")

    def __getNewVn(self) -> str:
        """
        用于产生一个新的非终结符
        :return: 返回新的非终结符
        """
        for i in range(ord("A"), ord("Z")):
            if chr(i) not in self.Vn:
                return chr(i)

    def __remove_left_recursion(self):
        """
        用于消除左递归
        :return:
        """
        VnList = list(self.Vn)
        print("非终结符顺序是:", "->".join(VnList))
        ranges = range(len(VnList))
        """
        递归每一个非终结符对应的语句
        """
        for i in ranges:  # i是序号
            N = VnList[i]  # N就是这个序号对应的非终结符
            """
            我们需要把N对应的文法右部开始的非终结符Vn消除
            消除方法：
                如果Vn==N，不把自己带入自己
                如果Vn==以前遍历过的N (N in [VnList[j]] for j in range(0,i))，把对应的语句带入
                其他情况不带入
            """
            # 加入
            if (i == 0):  # 如果Vn==N，不把自己带入自己
                pass
            else:
                # _p是获取以前遍历过的N
                _p = {VnList[j]: self.P[VnList[j]] for j in range(0, i)}
                # p是获取当前N对应语句
                p = self.P[N]
                # while中反复把文法右部开始的非终结符消除
                while (True):
                    new_p = set()
                    for item in p:
                        # 检测左边是否存在非终结符
                        if str.isupper(item[0]) and item[0] != N and (item[0] in _p.keys()):
                            for j in _p[item[0]]:
                                new_p.add(j + item[1:])
                            # 注意！带入过一次不能再次带入，要删掉
                            _p.pop(item[0])
                        else:
                            new_p.add(item)
                    if (new_p == p):  # 如果循环一遍没有变化，则退出
                        self.P[N] = new_p
                        break
                    else:  # 如果循环一遍有变化，再来一轮循环
                        p = new_p
            """
            将左递归去除
            """
            alpha = set()
            beta = set()
            for item in self.P[N]:
                if (item[0] == N):
                    alpha.add(item[1:])
                else:
                    beta.add(item)
            if (alpha == set()):  # 说明这个非终结符对应的文法没有左递归
                continue
            # 构造新非终结符
            newVn = self.__getNewVn()
            self.Vn.add(newVn)
            self.P[newVn] = set([f"{i}{newVn}" for i in alpha])
            self.P[newVn].add("@")
            self.P[N] = set([f"{i}{newVn}" for i in beta])

    def __remove_left_gene(self):
        """
        提取左因子
        :return:
        """
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
        print("转化为LL1文法完成！")
        print(self)
