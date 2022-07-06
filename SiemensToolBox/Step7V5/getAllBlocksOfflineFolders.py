from dbfread import DBF
from SiemensToolBox.SimaticDataTypes import BlockOfflineFolder


def getAllBlocksOfflineFolders(projectFolder, encoding="ISO-8859-1"):
    dbf = DBF(fr"{projectFolder}\ombstx\offline\BSTCNTOF.DBF", raw=True)

    folders = dict()
    for row in dbf.records:
        folder = BlockOfflineFolder()
        folder.name = row["NAME"].decode(encoding).strip()
        folder.folder = fr"{projectFolder}\ombstx\offline\{int(row['ID']):08x}"
        folder.ID = int(row["ID"])
        folders[int(row["ID"])] = folder
    return folders
