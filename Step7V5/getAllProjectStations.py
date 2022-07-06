from dbfread import DBF
from SimaticDataTypes import StationType, StationConfigurationFolder, PLCType, CpFolder

"""from projectFiles import Step7ProjectV5"""


def getAllProjectStations(projectFolder):


    dbf = DBF(f"{projectFolder}\\hOmSave7\\s7hstatx\\HOBJECT1.DBF",raw=True)
    stations = dict()

    for row in dbf.records:
        if StationType.has_value(int(row["OBJTYP"])):
            station = StationConfigurationFolder(int(row["OBJTYP"]))

            station.Name = str(row["NAME"].decode("ISO-8859-1").replace("\0", "").strip())
            station.ID = int(row["ID"])
            station.UnitID = int(row["UNITID"])
            stations[station.ID] = station
    return stations
