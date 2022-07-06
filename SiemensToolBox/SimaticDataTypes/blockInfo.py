from dataclasses import dataclass, field
from .s7Types import BlockType
from .blockBytes import BlockBytes
from dbfread import DBF
from SiemensToolBox.Step7V5.getLayout import Getlayout


@dataclass
class BlockInfo():
    id: int = field(init=True, repr=False)
    blockType: BlockType = field(init=True, default=None, repr=True)
    blockNumber: int = field(init=True, default=None, repr=True)
    name: str = field(init=True, default=False, repr=False)
    family: str = field(init=True, default=None, repr=False)
    knowHowProtection: bool = field(init=True, default=False, repr=False)
    isInstance: bool = field(init=True, default=False, repr=False)
    _folder: str = field(init=True, default=None, repr=False)


    @property
    def BlockName(self):
        return f"{self.blockType.name}{self.blockNumber}"

    @property
    def blockBytes(self):
        if not hasattr(self, "bausteinDBF"):
            self.bausteinDBF = DBF(f"{self._folder}\\BAUSTEIN.DBF", encoding="ISO-8859-1")
        if not hasattr(self, "subblkDBF"):
            self.subblkDBF = DBF(f"{self._folder}\\SUBBLK.DBF", encoding="ISO-8859-1")

        blockbytes = BlockBytes()

        for row in self.bausteinDBF.records:
            if not int(row["ID"]) == self.id:
                continue
            if row["UDA"]:
                blockbytes.uda = row["UDA"]

        for row in self.subblkDBF.records:
            if not int(row["OBJECTID"]) == self.id:
                continue

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

            if blockbytes.CheckSum == 0:
                if int(row["CHECKSUM"] != 0):
                    blockbytes.CheckSum = int(row["CHECKSUM"])

            if row["SUBBLKTYP"] in [
                BlockType.SDB.value, BlockType.OB.value, BlockType.FB.value, BlockType.SFC.value,
                BlockType.SFB.value]:

                if int(row["PASSWORD"]) == 3:
                    blockbytes.knowHowProtection = True

                blockbytes.mc7code = mc5code
                blockbytes.username = str(row["USERNAME"]).strip("\0")
                blockbytes.version = str(int(row["VERSION"]) / 16) + "." + str(int(row["VERSION"]) % 16)
                blockbytes.nwinfo = addinfo
                blockbytes.LastCodeChange = row["TIMESTAMP1"]
                blockbytes.LastInterfaceChange = row["TIMESTAMP2"]
                # blockbytes.BlockLanguage = PLCLanguage(int(row["BLKLANG"]))


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
        return blockbytes

    @property
    def layout(self):
        if not self.blockBytes.blkinterface: return None
        rows = [row.strip() for row in self.blockBytes.blkinterface.split("\n") if len(row.strip()) > 0]
        root = Getlayout(self, rows)
        return root
