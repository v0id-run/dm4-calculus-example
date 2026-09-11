import csv
import os
import re
from typer import Typer
from git import Repo

class ApplicationContext:
    def __init__(self, path, printer):
        self.db = {}
        self.raws = []
        with open(path) as file:
            reader = csv.reader(file)
            for line in reader:
                self.raws.append(line)
                key = line[0]
                value = self.db.get(key)
                if value is None:
                    self.db[key] = [line]
                else:
                    self.db[key].append(line)
                key = line[4]
                value = self.db.get(key)
                if value is None:
                    self.db[key] = [line]
                else:
                    self.db[key].append(line)
        self.path = path
        self.typer = Typer()
        self.repo = Repo(self.path.replace("trace/db.csv", ''))
    
    def add(self, fromUnit, fromType, fromVersion, relation, toUnit, toType, toVersion):
        data = [fromUnit, fromType, fromVersion, relation, toUnit, toType, toVersion]
        lines = self.db.get(fromUnit)
        if lines is None:
            self.db[fromUnit] = []
        else:
            for line in lines:
                if line[0] == fromUnit and line[4] == toUnit:
                    if self.db[fromUnit] == []:
                        self.db.pop(fromUnit)
                    return "connection exists"
                if line[4] == fromUnit and line[0] == toUnit:
                    if self.db[fromUnit] == []:
                        self.db.pop(fromUnit)
                    return "reverse direction connection exists"
        with open(self.path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        self.db[fromUnit].append(data)
        if self.db.get(toUnit) is None:
            self.db[toUnit] = []
        self.db[toUnit].append(data)
        return ""

    def getPathOfUnit(self, unit):
        prefixes = self.typer.__typeSystem__.keys()
        for prefix in prefixes:
            dirpath = self.path.replace("trace/db.csv", '') + prefix
            for filename in os.listdir(dirpath):
                if filename.endswith(".md"):
                    filepath = os.path.abspath(os.path.join(dirpath, filename))
                    units = self.collectUnitsFromFile(filepath)
                    if unit in units:
                        return filepath
        return ''

    def updateVersion(self, unit):
        result = []
        values = self.db.get(unit)
        if values is None:
            return ("unit does not traced", False)
        path = self.getPathOfUnit(unit)
        if path == '':
            return ("unit does not exists", False)
        version = self.gitGetVersion(path, unit)
        for i in range(len(self.raws)):
            line = self.raws[i]
            if line[0] == unit:
                result.append([i+1, "no" if line[2] == version else "changed" , line[2], version])
                line[2] = version
            if line[4] == unit:
                result.append([i+1, "no" if line[6] == version else "changed" , line[6], version])
                line[6] = version
        with open(self.path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.raws)
        return (result, True)

    def contains(self, unit):
        return not self.db.get(unit) is None

    # option = all, parent, child
    def relations(self, unit, option):
        value = self.db.get(unit)
        if value is None:
            return []
        elif option == "all":
            return value
        elif option == "parent":
            return list(filter(lambda x: x[0] == unit, value))
        elif option == "child":
            return list(filter(lambda x: x[4] == unit, value))
        else:
            return []

    def collectUnitsFromFile(self, path):
        units = []
        content = []
        with open(path, 'r') as file:
            content = file.readlines()
        for line in content:
            line = line.strip('\r\n')
            if re.fullmatch(r'^\* \*\*(\w|\.)+\*\*:.*', line):
                unit = re.search(r'^\* \*\*(\w|\.)+\*\*:', line)[0].strip(':* ')
                units.append(unit)
        return units

    def listUnitsInFile(self, path, traced = None):
        apath = os.path.abspath(path)
        fileUnits = self.collectUnitsFromFile(apath)
        tracedUnits = self.db.keys()
        result = []
        for unit in fileUnits:
            if traced:
                if unit in tracedUnits:
                    result.append(unit)
            elif not traced:
                if not unit in tracedUnits:
                    result.append(unit)
            else:
                result.append(unit)
        type = self.typer.type(apath)
        return [result, type]

    def derivativesInFile(self, path):
        temp = self.listUnitsInFile(path, True)
        type = temp[1]
        traced = temp[0]
        not_traced = self.listUnitsInFile(path, False)[0]
        result = []
        for unit in traced:
            value = self.db.get(unit)
            for line in value:
                if unit == line[4]:
                    result.append(unit)
                    break
        return [result, not_traced, type]

    def derivativesOfType(self, type):
        prefixes = self.typer.path(type)
        result = []
        for prefix in prefixes:
            dirpath = self.path.replace("trace/db.csv", '') + prefix
            for filename in os.listdir(dirpath):
                if filename.endswith(".md"):
                    filepath = os.path.abspath(os.path.join(dirpath, filename))
                    result.append(self.derivativesInFile(filepath)[:2])
        return result

    def gitGetVersion(self, path, unit):
        return self.repo.git.log("--raw", "--pretty=%h", "-L", r"/\*\ \*\*{}\*\*:/,/<end>/:".format(unit)+os.path.abspath(path))[:6]

    def gitUTVInFile(self, path):
        units = self.listUnitsInFile(path, True)[0]
        type = self.typer.type(path)
        info = {
            "units": [],
            "types": [],
            "versions": []
        }
        for unit in units:
            real_version = self.gitGetVersion(path, unit)
            info["units"].append(unit)
            info["types"].append(type)
            info["versions"].append(real_version)
        return info

    def smellInFile(self, path):
        result = []
        gitUTV = self.gitUTVInFile(path)
        i = 1
        for line in self.raws:
            if line[0] in gitUTV["units"]:
                unit = line[0]
                gitIndex = gitUTV["units"].index(unit)
                gitType = gitUTV["types"][gitIndex]
                gitVersion = gitUTV["versions"][gitIndex]
                traceType = line[1]
                traceVersion = line[2]
                if gitType != traceType:
                    result.append([i, unit, "type", gitType, traceType])
                if gitVersion != traceVersion:
                    result.append([i, unit, "version", gitVersion, traceVersion])
            if line[4] in gitUTV["units"]:
                unit = line[4]
                gitIndex = gitUTV["units"].index(unit)
                gitType = gitUTV["types"][gitIndex]
                gitVersion = gitUTV["versions"][gitIndex]
                traceType = line[5]
                traceVersion = line[6]
                if gitType != traceType:
                    result.append([i, unit, "type", gitType, traceType])
                if gitVersion != traceVersion:
                    result.append([i, unit, "version", gitVersion, traceVersion])
            i += 1
        return result