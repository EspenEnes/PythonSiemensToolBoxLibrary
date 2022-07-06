from dataclasses import dataclass, field
from .blockOfflineFolder import BlockOfflineFolder
from .symbolTable import SymbolTable
from dbfread import DBF
import os
import re


@dataclass
class S7ProgrammFolder:
    Name: str = field(init=True, default="", repr=True)
    projectFolder: str = field(init=True, default=None, repr=False)
    _linkfileoffset: int = field(init=True, default=None, repr=False)
    _ID: int = field(init=True, default=None, repr=False)
    _blockOfflineFolder: BlockOfflineFolder = field(init=True, default=None, repr=False)
    _blockOfflineFolder_loaded: bool = field(init=True, default=False, repr=False)
    _symbolTable: SymbolTable = field(init=True, default=None, repr=False)
    _symbolTable_loaded: bool = field(init=True, default=False, repr=False)
    _encoding: str = field(init=True, default="ISO-8859-1", repr=False)

    # self.onlineBlocksFolder = None
    # self.sourceFolder = None

    @property
    def symbolTable(self):
        if self._symbolTable_loaded: return self._symbolTable
        dbf1 = DBF(f"{self.projectFolder}\\YDBs\\YLNKLIST.DBF", raw=True)
        dbf2 = DBF(f"{self.projectFolder}\\YDBs\\SYMLISTS.DBF", raw=True)

        id2 = 0
        for row in dbf1.records:
            if int(row["TOI"]) == self._ID:
                id2 = int(row["SOI"])
                break

        if id2 > 0:
            for row in dbf2.records:
                if not int(row["_ID"]) == id2:
                    continue

                if os.path.isfile(f"{self.projectFolder}\\YDBs\\{str(id2)}\\SYMLIST.DBF"):
                    table = SymbolTable()
                    table.Name = (row["_UNAME"])
                    table.folder = f"{self.projectFolder}\\YDBs\\{str(id2)}"
                    self._symbolTable = table
                    self._symbolTable_loaded = True
                    return table
        return None

    @property
    def blockOfflineFolder(self):
        if self._blockOfflineFolder_loaded: return self._blockOfflineFolder
        file = self.projectFolder + "\\" + "hrs" + "\\" + "linkhrs.lnk"
        with open(file, "rb") as f:
            completeBuffer = f.read()
        match = re.compile(b"\x01\x60\x11\x00(.{2})").search(completeBuffer[self._linkfileoffset:])

        if match:
            Step7ProjectBlockFolderID = int.from_bytes(match.group(1), "little")
            dbf = DBF(fr"{self.projectFolder}\ombstx\offline\BSTCNTOF.DBF", raw=True)
            for row in dbf.records:
                if int(row["ID"]) == Step7ProjectBlockFolderID:
                    folder = BlockOfflineFolder()
                    folder.name = row["NAME"].decode(self._encoding).strip()
                    folder.folder = fr"{self.projectFolder}\ombstx\offline\{int(row['ID']):08x}"
                    folder.ID = int(row["ID"])
                    self._blockOfflineFolder = folder
                    self._blockOfflineFolder_loaded = True
                    return folder
        return None
