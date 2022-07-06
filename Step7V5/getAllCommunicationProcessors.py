from dbfread import DBF
from dbfread import exceptions
from SimaticDataTypes import CpFolder



def getAllCommunicationProcessors(projectFolder, stations):
    """Get all CP Objects"""

    folders = {}
    try:
        dbf = DBF(f"{projectFolder}\\hOmSave7\\s7wb53ax\\HOBJECT1.DBF", raw=True)
    except exceptions.DBFNotFound:
        return folders

    for row in dbf.records:
        cp = CpFolder(int(row["ID"]))
        cp.unitID = int(row["UNITID"])
        cp.objTyp = int(row["OBJTYP"])
        cp.name = row["NAME"].decode("ISO-8859-1").replace("\0", "").strip()
        cp.rack = int(row["SUBSTATN"])
        cp.slot = int(row["MODULN"])
        cp.subModulNumber = int(row["SUBMODN"])
        folders[cp.ID] = cp

    """add subitem to _parent"""
    for cp in folders.values():
        if cp.subModulNumber > 0:
            parent = next((x for x in folders.values() if x.ID == cp.unitID), None)
            if parent:
                parent.subModule = cp

    """Link all CP Objects"""
    dbf = DBF(f"{projectFolder}\\hOmSave7\\s7wb53ax\\HRELATI1.DBF")
    for row in dbf.records:
        if int(row["RELID"]) == 1315827: #Add CP to Station
            STATION = next((station for station in stations.values() if station.ID == int(row["TUNITID"])), None)
            CP = next((cp for cp in folders.values() if cp.ID == int(row["SOBJID"])), None)
            if STATION and CP:
                STATION.modules.append(CP)
                CP.parent = STATION

        elif int(row["RELID"]) == 64: #Add interface Foreign key to CP
            CP = next((cp for cp in folders.values() if cp.ID == int(row["SOBJID"])), None)
            if CP:
                CP.networkId = int(row["TOBJID"])





    return folders
