class LexicalAnalyzer:

    def __init__(self, s: str):

        self.__txt = []
        self.__now_state = None
        self.__now_point = 0
        self.__record = []
        self.result = []

        self.__txt.extend(list(s))
        self.__txt.extend(" ")
        self.__reset()
        while (self.__now_point < len(self.__txt)):
            self.__now_state(self.__txt[self.__now_point])

    def __is_blank(self, t):
        if t in ["\n", " ", "\t"]:
            return True
        return False

    def __in_1_9(self, t):
        if str.isdigit(t):
            if (int(t) in range(1, 10)):
                return True
        return False

    def __in_0_9(self, t):
        if str.isdigit(t):
            if (int(t) in range(0, 10)):
                return True
        return False

    def __is_0(self, t):
        if str.isdigit(t):
            if int(t) == 0:
                return True

    def __in_0_f(self, t):
        if str.isdigit(t):
            if int(t) in range(0, 10):
                return True
        elif str.isalpha(t):
            if t in [chr(i) for i in range(ord('a'), ord('f') + 1)]:
                return True
        return False

    def __is_keyword(self, s):
        if s in ["if", "then", "else", "while", "do"]:
            return True
        else:
            return False

    def __set_next(self, t, state):
        self.__now_point += 1
        self.__record.append(t)
        self.__now_state = state

    def __reset(self):
        self.__record.clear()
        self.__now_state = self.__case_X

    def __case_X(self, t):
        if (self.__is_blank(t)):
            self.__now_point += 1
            self.__now_state = self.__case_X
        elif (str.isalpha(t)):
            self.__set_next(t, self.__case_A)
        elif (self.__in_1_9(t)):
            self.__set_next(t, self.__case_B)
        elif (self.__is_0(t)):
            self.__set_next(t, self.__case_D)
        elif (t in ['+', '-', '*', '/', '>', '<', '=', '(', ')', ';']):
            # print(f"<{t},->")
            self.result.append((t, '-'))
            self.__now_point += 1
            self.__reset()
        else:
            raise Exception(f"Unknown Character '{t}'")

    def __case_A(self, t):
        if (str.isalpha(t) or str.isdigit(t)):
            self.__set_next(t, self.__case_A)
        else:
            s = ''.join(self.__record)
            if (self.__is_keyword(s)):
                # print(f"<{s},->")
                self.result.append((s, '-'))
            else:
                # print(f"<0,{''.join(self.__record)}>")
                self.result.append(('0', ''.join(self.__record)))
            self.__reset()

    def __case_B(self, t):
        if (self.__in_0_9(t)):
            self.__set_next(t, self.__case_B)
        else:
            # print(f"<1,{''.join(self.__record)}>")
            self.result.append(('1', ''.join(self.__record)))
            self.__reset()

    def __case_C(self, t):
        pass

    def __case_D(self, t):
        if (self.__in_1_9(t)):
            self.__set_next(t, self.__case_E)
        elif (t == 'x'):
            self.__set_next(t, self.__case_F)
        else:
            # print(f"<1,{''.join(self.__record)}>")
            self.result.append(('1', ''.join(self.__record)))
            self.__reset()

    def __case_E(self, t):
        if (self.__in_0_9(t)):
            self.__set_next(t, self.__case_E)
        else:
            # print(f"<2,{''.join(self.__record)}>")
            self.result.append(('2', ''.join(self.__record)))
            self.__reset()

    def __case_F(self, t):
        if self.__in_0_f(t):
            self.__set_next(t, self.__case_G)
        else:
            raise Exception(f"behind 0x.. must be 0~f! Rather than '{t}'")

    def __case_G(self, t):
        if self.__in_0_f(t):
            self.__set_next(t, self.__case_G)
        else:
            # print(f"<3,{''.join(self.__record)[2:]}>")
            self.result.append(('3', ''.join(self.__record)[2:]))
            self.__reset()

# print(LexicalAnalyzer("((ab3+de4)**5)+1").result)
