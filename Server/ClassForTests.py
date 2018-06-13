import datetime

class ClassForTests(object):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        d = datetime.datetime.fromtimestamp(1528909668)
        print(d)


