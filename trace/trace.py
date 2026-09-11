import sys
import os

from db import ApplicationContext
from printers import ConsolePrinter

args = sys.argv
callingDir = args[0].rstrip("trace.py")
args = args[1:]

printer = ''
if args[0] == '-f' or args[0] == '--file':
    args = args[1:]
    pass
else:
    printer = ConsolePrinter()
ctx = ApplicationContext(os.path.abspath(callingDir + 'db.csv'), printer)

cmd = args[0]
if cmd == 'rel':
    option = ""
    units = []
    if args[1].startswith('-'):
        option = args[1]
        units = args[2:]
    else:
        units = args[1:]
    for unit in units:
        prefix = ""
        out = []
        if option == "":
            prefix = "all relations"
            out = ctx.relations(unit, "all")
        elif option == "-p":
            prefix = "relations where parent"
            out = ctx.relations(unit, "parent")
        elif option == "-c":
            prefix = "relations where child"
            out = ctx.relations(unit, "child")
        printer.result(prefix, unit, out, ['UNIT', 'TYPE', 'VERSION', 'RELATION', 'UNIT', 'TYPE', 'VERSION', 'LINE'])

elif cmd == 'add':
    if len(args) == 8:
        from_unit = args[1]
        from_type = args[2]
        from_version = args[3] # может быть можно сходить в репозиторий за свежей версией
        relation = args[4]
        to_unit = args[5]
        to_type = args[6]
        to_version = args[7]
        out = ctx.add(from_unit, from_type, from_version, relation, to_unit, to_type, to_version)
        if out != "":
            printer.error(out, args[1:8])
    if len(args) == 4:
        unit = args[1]
        type = args[2]
        version = args[3]
        out = ctx.add("", "", "", "", unit, type, version)
        if out != "":
            printer.error(out, [unit, type, version])

elif cmd == 'update':
    unit = args[1]
    out, ok = ctx.updateVersion(unit)
    if ok:
        printer.result("successfully updated", unit, out, ['LINE', 'ACTION', 'FROM', 'TO'])
    else:
        printer.error(out, unit)

elif cmd == 'ls':
    option = ""
    files = []
    if args[1].startswith('-'):
        option = args[1]
        files = args[2:]
    else:
        files = args[1:]
    for file in files:
        prefix = ""
        out = []
        if option == "":
            prefix = "list all"
            out = ctx.listUnitsInFile(os.getcwd()+"/"+file)
        elif option == '-t':
            prefix = "list traced"
            out = ctx.listUnitsInFile(os.getcwd()+"/"+file, True)
        elif option == '-n':
            prefix = "list not traced"
            out = ctx.listUnitsInFile(os.getcwd()+"/"+file, False)
        else:
            prefix = "option not found"
            printer.error(prefix, option)
            break
        printer.result(prefix, "["+str(out[1])+"] in " + file, out[0], ['UNIT'])

elif cmd == 'der':
    if args[1] == '--all':
        pass
    if args[1] == '--type':
        type = args[2]
        result = ctx.derivativesOfType(type)
        for item in result:
            print(item)
            print("\n---\n")
    else:
        file = args[1]
        result = ctx.derivativesInFile(file)
        type = result[2]
        printer.result("derivatives in file", file, [[item, type] for item in result[0]], ['UNIT', 'TYPE'])
        if result[1] != []:
            printer.error("not traced units", file, [[item, type] for item in result[1]], ['UNIT', 'TYPE'])

elif cmd == 'smell':
    was_smell = False
    if args[1] == '--all':
        repo_dir = ctx.path.replace("trace/db.csv", '')
        prefixes = ctx.typer.__typeSystem__.keys()
        for prefix in prefixes:
            target_dir = os.path.join(repo_dir, prefix)
            for filename in os.listdir(target_dir):
                if filename.endswith(".md"):
                    file = os.path.join(target_dir, filename)
                    smells = ctx.smellInFile(file)
                    if len(smells) > 0:
                        printer.error("smells in", file, smells, ['LINE', 'UNIT', 'KIND', 'ACTUAL', 'FROM_DB'])
                        was_smell = True
                    else:
                        printer.result("no smells in", file)
    elif args[1] == '--type':
        type = args[2]
    else:
        file = args[1]
        smells = ctx.smellInFile(file)
        if len(smells) > 0:
            printer.error("smells in", file, smells, ['LINE', 'UNIT', 'KIND', 'ACTUAL', 'FROM_DB'])
            was_smell = True
        else:
            printer.result("no smells in", file)
    if was_smell:
        exit(1)

else:
    print('unknown')