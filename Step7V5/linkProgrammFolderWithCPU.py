from dbfread import DBF


def linkProgrammFolderWithCPU(projectFolder, cpuFolders, s7ProgramFolders):
    dbf = DBF(fr"{projectFolder}\hOmSave7\s7hk31ax\HRELATI1.DBF")

    for row in dbf.records:
        if int(row["RELID"]) == 16:
            cpuID = int(row["SOBJID"])
            folderID = int(row["TOBJID"])

            if cpuID in cpuFolders and folderID in s7ProgramFolders:
                cpu = cpuFolders[cpuID]
                folder = s7ProgramFolders[folderID]
                folder._parent = cpu
                cpu.subItems.append(folder)
