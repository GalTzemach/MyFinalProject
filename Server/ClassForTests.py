
class ClassForTests(object):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.getStr() as myStr:
            print(myStr)

    def getTrue(self):
        return True

    def getFalse(self):
        return False

    def getStr(self):
        return "str"


