class Typer:
    def __init__(self):
        self.__typeSystem__ = {
            "Спецификация требований/Общее описание":"SYSREQ",
            "Спецификация требований/Конкретные требования":"SOFTREQ",
            "Спецификация требований/Конкретные требования/Компоненты системы":"SOFTREQ"
        }

    def type(self, path):
        for item in self.__typeSystem__.items():
            if item[0] in path:
                return item[1]
    
    def path(self, type):
        paths = []
        for item in self.__typeSystem__.items():
            if item[1] == type:
                paths.append(item[0])
        return paths