from tabulate import tabulate

class ConsolePrinter:
    resultColor = "\033[38;5;10m"
    errorColor = "\033[38;5;9m"
    msgColor = "\033[38;5;32m"
    paramsColor = "\033[38;5;172m"
    resetColor = "\033[0m"

    def error(self, query, params, data = None, headers = None):
        print(
            self.errorColor+ "ERROR:",
            self.msgColor + query,
            self.paramsColor + params,
            self.resetColor
        )
        if data and headers:
            print(tabulate(data, headers, tablefmt="fancy_grid"))
    def result(self, query, params, data = None, headers = None):
        print(
            self.resultColor + "QUERY:", 
            self.msgColor + query, 
            self.paramsColor + params,
            self.resetColor
        )
        if data and headers:
            print(tabulate(data, headers, tablefmt="fancy_grid"))