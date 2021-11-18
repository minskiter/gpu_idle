class DictObj():
    def __init__(self,d) -> None:
        self.__dict__.update(d)

    def __getitem__(self,key):
        return self.__dict__[key]