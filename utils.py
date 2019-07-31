class List:
    def __init__(self, l):
        self.list = l

    def __getitem__(self, i):
        try:
            return self.list[i]
        except:
            return self.__class__([])

    def __len__(self):
        return len(self.list)

    def __bool__(self):
        if not self.l:
            return False
        else:
            return True

def sub(small, big):
    result = small - big
    if result < 0:
        return 0
    else:
        return result

All = lambda *args: all(args)
Any = lambda *args: any(args)
