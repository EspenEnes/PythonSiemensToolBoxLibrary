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

        # Try and load Baustein and SubBlock from DBF
        try:
            bausteinDBF = DBF(f"{self.folder}\\BAUSTEIN.DBF", encoding=self._encoding, load=True)
            subblkDBF = DBF(f"{self.folder}\\SUBBLK.DBF", encoding=self._encoding, load=True)
        except DBFNotFound:
            return blocks

        validTypes = [BlockType.SFB.value, BlockType.SFC.value, BlockType.SDB.value,
                      BlockType.DB.value,
                      BlockType.VAT.value, BlockType.FB.value, BlockType.FC.value,
                      BlockType.OB.value,
                      BlockType.UDT.value]

        # Find all Buildingblocks that are of valid types
        blocks = {int(row["ID"]): BlockInfo(row, self) for row in bausteinDBF.records if
                  int(row["TYP"]) in validTypes}

        # Group together SubBlocks with equal "OBJECT ID
        subBlocks = {}
        for row in subblkDBF.records:
            if row["OBJECTID"] not in subBlocks:
                subBlocks[row["OBJECTID"]] = []
            subBlocks[row["OBJECTID"]].append(row)

        # Merge SubBlocks with BuildingBlocks
        for key, value in subBlocks.items():
            try:
                block = blocks[key]
                block.subBlocks = value
                retval[block.BlockName] = block
            except KeyError:
                pass

        self._blockList = retval
        self._blocklist_loaded = True
        return self._blockList
