from SiemensToolBox.SimaticDataTypes import PLCType
from dbfread import DBF


def linkProfinetWithCpuCp(projectFolder, cpuFolders, cpFolders, networkInterfaces):
    plcsWithEternet = [PLCType.EternetInCPU3xxF.value, PLCType.EternetInCPU3xx.value, PLCType.EternetInCPU4xx.value,
                       PLCType.EternetInCPU3xx_2.value, PLCType.EternetInCPURTX.value]

    dbf = DBF(
        fr"{projectFolder}\hOmSave7\s7hssiox\HOBJECT1.DBF", raw=True)
    """find all profinet systems"""

    for row in dbf.records:

        if int(row["OBJTYP"]) in plcsWithEternet:
            """Profinet connection to CPU"""
            if int(row["UNITID"]) in cpuFolders:
                cpu = cpuFolders[int(row["UNITID"])]
                cpu.idTobjID.append(int(row["ID"]))
        elif int(row["OBJTYP"]) in [2364971, 2367589]:
            if int(row["UNITID"]) in cpFolders:
                cp = cpFolders[int(row["UNITID"])]
                cp.idTobjId.append(int[row["ID"]])



    dbf = DBF(fr"{projectFolder}\hOmSave7\s7hssiox\HRELATI1.DBF", raw=True)

    for row in dbf.records:

        if int(row["RELID"]) == 64:
            CP = next((cp for cp in cpFolders.values() if int(row["SOBJID"]) in cp.idTobjId), None)
            CPU = next((cpu for cpu in cpuFolders.values() if int(row["SOBJID"]) in cpu.idTobjID), None)
            if CP:
                CP.tObjId = int(row["TOBJID"])  # todo: this is alo done in getAll_CP  ????
            elif CPU:
                CPU.networkId = int(row["TOBJID"])

    for networkId in networkInterfaces:
        CPU = next((cpu for cpu in cpuFolders.values() if cpu.networkId == networkId), None)
        CP = next((cp for cp in cpFolders.values() if networkId == cp.networkId), None)


        if CP:
            CP.NetworkInterfaces.append(networkInterfaces[networkId])
        if CPU:
            CPU.NetworkInterfaces.append(networkInterfaces[networkId])
