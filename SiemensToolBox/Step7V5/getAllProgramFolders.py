from dbfread import DBF
from SiemensToolBox.SimaticDataTypes.s7ProgramFolder import S7ProgrammFolder


def getAllProgramFolders(projectFolder, encoding="ISO-8859-1"):
    dbf = DBF(fr"{projectFolder}\hrs\S7RESOFF.DBF", raw=True)

    folders = {}
    for row in dbf.records:
        folder = S7ProgrammFolder()
        folder.projectFolder = projectFolder
        folder.Name = row["NAME"].decode(encoding).strip()
        folder._linkfileoffset = int(row["RSRVD4_L"])
        folder._ID = int(row["ID"])
        folders[folder._ID] = folder
    return folders
