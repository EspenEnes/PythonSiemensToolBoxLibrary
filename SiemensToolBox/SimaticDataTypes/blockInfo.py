from .s7Types import BlockType
from .blockBytes import BlockBytes
from SiemensToolBox.Step7V5.getLayout import Getlayout
from .functionBlockRow import S7FunctionBlockRow
from dataclasses import dataclass, field




@dataclass
class BlockInfo():
    rowData: any = field(init=True, repr=False)
    _parent: any = field(init=True, repr=False)
    id: int = field(init=False,default=None, repr=False)
    blockType: BlockType = field(init=True, default=None, repr=True)
    blockNumber: int = field(init=True, default=None, repr=True)
    name: str = field(init=True, default=False, repr=False)
    family: str = field(init=True, default=None, repr=False)
    knowHowProtection: bool = field(init=True, default=False, repr=False)
    isInstance: bool = field(init=True, default=False, repr=False)
    _folder: str = field(init=True, default=None, repr=False)
    _blockbytes : BlockBytes = field(init=True, default=None, repr=False)
    _subBlocks : list = field(init=True, default_factory=lambda : [])

    def __post_init__(self):
        self.id = int(self.rowData["ID"])
        self._folder = self._parent.folder
        self.blockNumber = int(self.rowData["NUMMER"])
        self.blockType = BlockType(int(self.rowData["TYP"]))


    @property
    def subBlocks(self):
        return self._subBlocks

    @subBlocks.setter
    def subBlocks(self, value):
        for row in value:
            if int(row["SUBBLKTYP"]) in [BlockType.FC.value, BlockType.OB.value, BlockType.FB.value,
                                         BlockType.SFC.value]:
                self.name = row["BLOCKNAME"].strip('\x00')
                self.family = row["BLOCKFNAME"].strip('\x00')

                if int(row["SUBBLKTYP"]) != BlockType.SFC.value:
                    if int(row["PASSWORD"]) == 3:
                        self.knowHowProtection = True
        self._subBlocks = value



    @property
    def syblolName(self):
        try:
            symbol = self._parent.symbolTable.symbols[self.BlockName]["symbol"]
        except KeyError:
            symbol = ""
        finally:
            return symbol



    @property
    def BlockName(self):
        return f"{self.blockType.name}{self.blockNumber}"

    @property
    def blockBytes(self):
        if self._blockbytes:
            return self._blockbytes

        blockbytes = BlockBytes()

        try:
            blockbytes.uda = self.rowData["UDA"]
        except KeyError:
            pass


        for row in self.subBlocks:

            mc5code = None
            if row["MC5CODE"] is not None:
                mc5code = row["MC5CODE"]
                if len(mc5code) > int(row["MC5LEN"]):
                    mc5code = mc5code.zfill(int(row["MC5LEN"]))

            ssbpart = None
            if row["SSBPART"] is not None:
                ssbpart = row["SSBPART"]
                if len(ssbpart) > int(row["SSBLEN"]):
                    ssbpart = ssbpart.zfill(int(row["SSBLEN"]))

            addinfo = None
            if row["ADDINFO"] is not None:
                addinfo = row["ADDINFO"]
                if len(addinfo) > int(row["ADDLEN"]):
                    addinfo = addinfo.zfill(int(row["ADDLEN"]))

            if blockbytes.CheckSum == 0 and int(row["CHECKSUM"] != 0):
                blockbytes.CheckSum = int(row["CHECKSUM"])


            if int(row["SUBBLKTYP"]) in [
                BlockType.FC.value, BlockType.OB.value, BlockType.FB.value, BlockType.SFC.value,
                BlockType.SFB.value]:

                if int(row["PASSWORD"]) == 3:
                    blockbytes.knowHowProtection = True

                blockbytes.mc7code = mc5code
                blockbytes.username = str(row["USERNAME"]).strip("\0")
                blockbytes.version = str(int(row["VERSION"]) / 16) + "." + str(int(row["VERSION"]) % 16)
                blockbytes.nwinfo = addinfo
                blockbytes.LastCodeChange = row["TIMESTAMP1"]
                blockbytes.LastInterfaceChange = row["TIMESTAMP2"]
                # blockbytes.BlockLanguage = PLCLanguage(int(row["BLKLANG"])) #todo gjør konvertering i dataclass


            elif int(row["SUBBLKTYP"]) in [5, 3, 4, 7, 9]:
                if mc5code is not None:
                    blockbytes.blkinterface = str(mc5code)

            elif int(row["SUBBLKTYP"]) in [19, 17, 18, 22, 21]:
                blockbytes.comments = mc5code
                blockbytes.blockdescription = ssbpart
                blockbytes.jumpmarks = addinfo

            elif int(row["SUBBLKTYP"]) in [1, 6]:
                if mc5code is not None:
                    blockbytes.blkinterface = str(mc5code)
                blockbytes.addinfo = addinfo

                blockbytes.LastCodeChange = row["TIMESTAMP1"]
                blockbytes.LastInterfaceChange = row["TIMESTAMP2"]

            elif int(row["SUBBLKTYP"]) == 10:
                blockbytes.mc7code = mc5code
                blockbytes.blkinterfaceInMC5 = ssbpart
                blockbytes.LastCodeChange = row["TIMESTAMP1"]
                blockbytes.LastInterfaceChange = row["TIMESTAMP2"]

                bytearrayOfssbpart = bytearray(ssbpart, encoding="ISO-8859-1")
                if int(row["SSBLEN"]) > 2 and (bytearrayOfssbpart[0] == 0x0a or bytearrayOfssbpart[0] == 0x0b):
                    blockbytes.IsInstanceDB = True
                    if bytearrayOfssbpart[0] == 11:
                        blockbytes.IsSFB = True
                    try:
                        blockbytes.FBNumber = int(bytearrayOfssbpart[1] + (256 * int(bytearrayOfssbpart[2])))
                    except IndexError:
                        pass

            elif int(row["SUBBLKTYP"]) == 14:
                pass

            elif int(row["SUBBLKTYP"]) == 42:
                pass

            elif int(row["SUBBLKTYP"]) == 27:  # VAT
                blockbytes.LastCodeChange = row["TIMESTAMP1"]
                blockbytes.LastInterfaceChange = row["TIMESTAMP2"]
                blockbytes.mc7code = mc5code
                blockbytes.nwinfo = addinfo

            elif int(row["SUBBLKTYP"]) == 38:
                blockbytes.comments = mc5code
        self._blockbytes = blockbytes
        return blockbytes

    @property
    def layout(self):
        if not self.blockBytes.blkinterface: return Getlayout(self._parent, [])
        rows = [row.strip() for row in self.blockBytes.blkinterface.split("\n") if len(row.strip()) > 0]
        root = Getlayout(self._parent, rows)
        return root


    def get_blockNetworks(self):
        networks = list()

        if not self.blockBytes.comments:
            return None

        cmt = bytearray(self.blockBytes.comments, "ISO-8859-1")

        i = 0
        while i < len(cmt) - 8:
            cmt_len = cmt[i]
            cmt_len_row = int(cmt[i + 3]) + (int(cmt[i + 4]) * 0x100)

            if cmt[i + 5] == 0x06:
                network = S7FunctionBlockRow()
                cmt_start = int(cmt[i + 1])
                network.name = cmt[i+6:((i+6)+(cmt_start-7))].decode("ISO-8859-1")
                network.comment = cmt[i + cmt_start: (i + cmt_start) + (cmt_len_row - cmt_start-1)].decode("ISO-8859-1")
                networks.append(network)
                i += cmt_len_row
            else:
                i += cmt_len + 6
        return networks