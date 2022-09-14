from dataclasses import dataclass, field

from dbfread import DBF, DBFNotFound
from .s7Types import BlockType
from .symbolTable import SymbolTable
from .blockInfo import BlockInfo



@dataclass
class BlockOfflineFolder:
    name: str = field(init=True, default="", repr=True)
    folder: str = field(init=True, default="", repr=False)
    _ID: int = field(init=True, default=None, repr=False)
    parent = None
    symbolTable: SymbolTable = field(init=True, default=None, repr=False)
    _blockList: dict[BlockInfo] = field(init=True, default_factory=lambda: {}, repr=False)
    _blocklist_loaded: bool = field(init=True, default=False, repr=False)
    _retrevedblockbytes: dict = field(init=True, default_factory=lambda: {}, repr=False)
    _retrevedblockLayout: dict = field(init=True, default_factory=lambda: {}, repr=False)
    _encoding: str = field(init=True, default="ISO-8859-1", repr=False)

    def getBlockBytes(self, input):
        if type(input) == BlockInfo:
            blkinfo = input
        elif type(input) == str:
            try:
                blkinfo = self._blockList[input]
            except KeyError:
                return None

        if str(blkinfo.id) in self._retrevedblockbytes:
            return self._retrevedblockbytes[str(blkinfo.id)]

        retval = blkinfo.blockBytes
        self._retrevedblockbytes[str(blkinfo.id)] = retval
        return retval

    def getBlockLayout(self, input):
        if not self._blocklist_loaded:
            _ = self.blockList

        if type(input) == type(BlockInfo):
            blkinfo = input
        elif type(input) == str:
            try:
                blkinfo = self._blockList[input]
            except KeyError:
                return None

        if str(blkinfo.id) in self._retrevedblockLayout:
            return self._retrevedblockLayout[str(blkinfo.id)]

        self._retrevedblockLayout[str(blkinfo.id)] = blkinfo.layout
        return blkinfo.layout

    @property
    def blockList(self):
        if self._blocklist_loaded: return self._blockList
        blocks = {}
        retval = {}

        try:
            self.bausteinDBF = DBF(f"{self.folder}\\BAUSTEIN.DBF", encoding=self._encoding, load=True).records
            self.subblkDBF = DBF(f"{self.folder}\\SUBBLK.DBF", encoding=self._encoding, load=True).records
        except DBFNotFound:
            return blocks

        validTypes = [BlockType.SFB.value, BlockType.SFC.value, BlockType.SDB.value,
                      BlockType.DB.value,
                      BlockType.VAT.value, BlockType.FB.value, BlockType.FC.value,
                      BlockType.OB.value,
                      BlockType.UDT.value]

        blocks = {int(row["ID"]): BlockInfo(row, self) for row in self.bausteinDBF if
                  int(row["TYP"]) in validTypes}

        output = {}
        self.subblkDBF: list[dict]
        for row in self.subblkDBF:
            if row["OBJECTID"] not in output:
                output[row["OBJECTID"]] = []
            output[row["OBJECTID"]].append(row)

        for key, value in output.items():
            try:
                block = blocks[key]
                block.subBlocks = value
                retval[block.BlockName] = block
            except KeyError:
                pass

        self._blockList = retval
        self._blocklist_loaded = True
        return self._blockList
