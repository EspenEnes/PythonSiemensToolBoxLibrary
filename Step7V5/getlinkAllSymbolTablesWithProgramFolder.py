from dbfread import DBF
from SimaticDataTypes import SymbolTable
import os

def linkSymbolTableWithProgrammFolder(projectFolder, s7ProgrammFolders ):
    dbf1 = DBF(f"{projectFolder}\\YDBs\\YLNKLIST.DBF", raw=True)
    dbf2 = DBF(f"{projectFolder}\\YDBs\\SYMLISTS.DBF", raw=True)

    id2 = 0
    for folder in s7ProgrammFolders.values():
        for row in dbf1.records:
            if int(row["TOI"]) == folder._ID:
                id2 = int(row["SOI"])
                break

        if id2 > 0:
            for row in dbf2.records:
                if not int(row["_ID"]) == id2:
                    continue

                if os.path.isfile(f"{projectFolder}\\YDBs\\{str(id2)}\\SYMLIST.DBF"):
                    table = SymbolTable()
                    table.Name = (row["_UNAME"])
                    table.folder = f"{projectFolder}\\YDBs\\{str(id2)}"
                    folder.symbolTable = table
                    break