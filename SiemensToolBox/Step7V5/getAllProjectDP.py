from dbfread import DBF
from SiemensToolBox.SimaticDataTypes import PLCType, CpFolder
from dataclasses import dataclass

@dataclass
class DpHelp():
    ID: int = None
    addr: int = None
    TobjID: int = None



def getAllDPfolders(projectFolder):
    dbf = DBF(f"{projectFolder}\\hOmSave7\\s7hstatx\\HOBJECT1.DBF",raw=True)
    DpFolder = {}

#  //Get The Project Stations..
    for row in dbf.records:
        if int(row["OBJTYP"]) == PLCType.MpiDPinCPU.value:

            dp = CpFolder(int(row["ID"]))
            dp.unitID = int(row["UNITID"])
            DpFolder[dp.ID] = dp

# Get The HW Folder for the Station...
    dbf = DBF(f"{projectFolder}\\hOmSave7\\s7hstatx\\HRELATI1.DBF")
    for row in dbf.records:

        if int(row["RELID"]) == 1315820:
            if int(row["TOBJTYP"]) in [PLCType.MpiDP300.value, PLCType.MpiDP400.value]:
                try:
                    DP = DpFolder[int(row["SOBJID"])]
                    DP.idTobjId.append(int(row["TOBJID"]))
                except KeyError:
                    pass

#//Get The ProfiBus and MPI
    dpList = dict()
    dbf =  DBF(f"{projectFolder}\\hOmSave7\\s7hkdmax\\HOBJECT1.DBF", raw=True)

    for row in dbf.records:

        dp = DpHelp()
        dp.ID = int(row["ID"])
        dpList[int(row["ID"])] = dp

    dbf = DBF(f"{projectFolder}\\hOmSave7\\s7hkdmax\\HRELATI1.DBF")
    for row in dbf.records:
        if int(row["RELID"]) == 1315837: #RelToCPU
            try:
                DP = dpList[int(row["SOBJID"])]
                DP.TobjID = (int(row["TOBJID"]))
            except KeyError:
                pass

        elif int(row["RELID"]) == 64:
            try:
                DP = dpList[int(row["SOBJID"])]
                DP.addr = (int(row["TOBJID"]))
            except KeyError:
                pass
#//remove DP from DPlist to DPFolder
    for dp in dpList.values():
        try:
            DP1 =  next((x for x in DpFolder.values() if (len(x.idTobjId) > 0 and dp.TobjID in x.idTobjId)), None)
            DP2 = DpFolder[dp.TobjID]

            if DP1.networkId == None: DP1.networkId = list()
            DP1.networkId.append(dp.addr)
        except:
            pass




    return DpFolder
