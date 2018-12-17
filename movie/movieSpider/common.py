class Common:
    def judgeListAndJoinStr(self):  # 判断list是否是一个还是多个，一个则直接返回，多个则返回字符串以“|”分割
        if len(self) >= 2:
            return " | ".join(list(map(lambda x: Common.clearBeforeAndAfterBlank(x), self)))
        elif len(self) >= 1:
            return Common.clearBeforeAndAfterBlank(self[0])
        else:
            return ''

    def clearBeforeAndAfterBlank(self):  # 清除前后空格和换行
        if len(self) <= 0:
            return self
        else:
            return self.replace("/n", "").strip()

    def respace(self,targetStr, newStr):  # 替换list中的字符串
        if len(self) <= 0:
            return self
        else:
            return list(map(lambda x : x.replace(targetStr, newStr), self))
