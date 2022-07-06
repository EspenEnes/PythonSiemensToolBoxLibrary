


def linkMpiDPWithCpuCp(cpuFolders, DPFolders, networkInterfaces):
    for network in networkInterfaces:
        DP = next((x for x in DPFolders.values() if x.networkId and network in x.networkId), None)
        if DP:
            cpu = next((x for x in cpuFolders.values() if x.unitID == DP.unitID), None)
            if cpu:
                cpu.NetworkInterfaces.append(networkInterfaces[network])