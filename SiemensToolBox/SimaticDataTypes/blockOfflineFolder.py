from dataclasses import dataclass, field

from dbfread import DBF, DBFNotFound
from .s7Types import BlockType
from .symbolTable import SymbolTable
from .blockInfo import BlockInfo
from .blockBytes import BlockBytes


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
            bausteinDBF = DBF(f"{self.folder}\\BAUSTEIN.DBF", raw=True)
            subblkDBF = DBF(f"{self.folder}\\SUBBLK.DBF", raw=True)
        except DBFNotFound:
            return blocks

        for row in bausteinDBF.records:
            if int(row["TYP"]) in [BlockType.SFB.value, BlockType.SFC.value, BlockType.SDB.value,
                                   BlockType.DB.value,
                                   BlockType.VAT.value, BlockType.FB.value, BlockType.FC.value,
                                   BlockType.OB.value,
                                   BlockType.UDT.value]:
                tmp = BlockInfo(int(row["ID"]))
                tmp._folder = self.folder
                tmp._parent = self
                tmp.blockNumber = int(row["NUMMER"])
                tmp.blockType = BlockType(int(row["TYP"]))
                blocks[int(row["ID"])] = tmp

        typ = [BlockType.FC.value, BlockType.OB.value, BlockType.FB.value, BlockType.SFC.value]

        for row in subblkDBF.records:
            try:
                block = blocks[int(row["OBJECTID"])]
                if int(row["SUBBLKTYP"]) in typ:
                    block.name = row["BLOCKNAME"].decode(self._encoding).strip('\x00')
                    block.family = row["BLOCKFNAME"].decode(self._encoding).strip('\x00')

                    if int(row["SUBBLKTYP"]) != BlockType.SFC.value:
                        if int(row["PASSWORD"]) == 3:
                            block.knowHowProtection = True
            except KeyError:
                continue

            retval[block.BlockName] = block

        self._blockList = retval
        self._blocklist_loaded = True
        return retval

