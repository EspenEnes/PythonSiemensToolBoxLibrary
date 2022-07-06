import re
from SimaticDataTypes.NetworkInterface import EthernetInterface, MpiProfibusInterface
from SimaticDataTypes.s7Types import interface


def getAllMPI(parent=None, projectFolder=None):
    if projectFolder:
        pass
    elif hasattr(parent, "projectFolder"):
        projectFolder = parent.projectFolder
    else:
        return None

    Interfaces = {}
    with open(projectFolder + "\\S7Netze\\S7NONFGX.tab", "rb") as f:
        completeBuffer = f.read()

    matchesMPIStructure = re.compile(b'\x01\x52\x14\x00').finditer(completeBuffer)

    for structure in matchesMPIStructure:
        struct = completeBuffer[structure.end(0): structure.end(0) + 2001]
        id = int.from_bytes(struct[:4], "little")
        MPI = MpiProfibusInterface()
        MPI._id = id

        matchesName = re.compile(b'Baugruppenname').finditer(struct)
        for matchName in matchesName:
            Name = struct[matchName.end(0) + 11: matchName.end(0) + 11 + int(struct[matchName.end(0) + 10])]
            MPI.Name = Name.decode("ISO-8859-1")


        matchesMPI = re.compile(b'\x9A\x08\x00\x00\x9A\x08\x00\x00').finditer(struct)
        for matchMPI in matchesMPI:

            MPI.Type = interface.MPI
            MPI.Address = int(struct[matchMPI.end(0) + 17])
            Interfaces[id] = MPI
    return Interfaces

def getAllDP(parent=None, projectFolder=None):
    if projectFolder:
        pass
    elif hasattr(parent, "projectFolder"):
        projectFolder = parent.projectFolder
    else:
        return None

    Interfaces = {}
    with open(projectFolder + "\\S7Netze\\S7NONFGX.tab", "rb") as f:
        completeBuffer = f.read()

    matchesDPStructure = re.compile(b'\x02\x52\x14\x00').finditer(completeBuffer)

    for structure in matchesDPStructure:
        struct = completeBuffer[structure.end(0): structure.end(0) + 2001]
        id = int.from_bytes(struct[:4], "little")

        DP = MpiProfibusInterface()
        DP._id = id

        matchesName = re.compile(b'Baugruppenname').finditer(struct)
        for matchName in matchesName:
            Name = struct[matchName.end(0) + 11: matchName.end(0) + 11 + int(struct[matchName.end(0) + 10])]
            DP.Name = Name.decode("ISO-8859-1")

        matchesDP = re.compile(b'\x36\x08\x00\x00\x36\x08\x00\x00').finditer(struct)
        for matchDP in matchesDP:

            DP.Type = interface.DP
            DP.Address = int(struct[matchDP.end(0) + 17])
            Interfaces[id] = DP
    return Interfaces



def getAllNetworkInterfaces(projectFolder):
    NetworkInterfaces = {}
    with open(projectFolder + "\\S7Netze\\S7NONFGX.tab", "rb") as f:
        completeBuffer = f.read()



    matchesIpStructure = re.compile(b'\x03\x52\x14\x00').finditer(completeBuffer)
    matchesMPIStructure = re.compile(b'\x01\x52\x14\x00').finditer(completeBuffer)
    matchesDPStructure = re.compile(b'\x02\x52\x14\x00').finditer(completeBuffer)

    for structure in matchesIpStructure:
        struct = completeBuffer[structure.end(0): structure.end(0) + 1705]
        id = int.from_bytes(struct[0:4], "little")
        ethernet = EthernetInterface()
        ethernet._id = id

        matchesName = re.compile(b'Baugruppenname').finditer(struct)
        for matchName in matchesName:
            Name = struct[matchName.end(0) + 29: matchName.end(0) + 29 + int(struct[matchName.end(0) + 28])]
            ethernet.Name = Name.decode("ISO-8859-1")


        matchesIP = re.compile(b'\xE0\x0F\x00\x00\xE0\x0F\x00\x00').finditer(struct)
        for matchIP in matchesIP:
            IPhex = struct[matchIP.end(0) + 21: matchIP.end(0) + 21 + int(struct[matchIP.end(0) + 20])]
            ip = f"{int(IPhex[0:2], 16)}.{int(IPhex[2:4], 16)}.{int(IPhex[4:6], 16)}.{int(IPhex[6:8], 16)}"
            ethernet.Address = ip

        matchesMask = re.compile(b'\xE5\x0F\x00\x00\xE5\x0F\x00\x00').finditer(struct)
        for matchMask in matchesMask:
            maskHex = struct[matchMask.end(0) + 21: matchMask.end(0) + 21 + int(struct[matchMask.end(0) + 20])]
            mask = f"{int(maskHex[0:2], 16)}.{int(maskHex[2:4], 16)}.{int(maskHex[4:6], 16)}.{int(maskHex[6:8], 16)}"
            ethernet.SubnetMask = mask

        matchesMAC = re.compile(b'\xA2\x0F\x00\x00\xA2\x0F\x00\x00').finditer(struct)
        for matchMAC in matchesMAC:
            MAChex = struct[matchMAC.end(0): matchMAC.end(0) + 21 + int(struct[matchMAC.end(0) + 20])]
            ethernet.PhysicalAddress = MAChex

        matchesRouter = re.compile(b'\xE3\x0F\x00\x00\xE3\x0F\x00\x00').finditer(struct)
        for matchRouter in matchesRouter:
            routerHex = struct[
                        matchRouter.end(0) + 21: matchRouter.end(0) + 21 + int(struct[matchRouter.end(0) + 20])]
            router = f"{int(routerHex[0:2], 16)}.{int(routerHex[2:4], 16)}.{int(routerHex[4:6], 16)}.{int(routerHex[6:8], 16)}"
            ethernet.IPAddressRouter = router

        matchesUseRouter = re.compile(b'\xE8\x0F\x00\x00\xE8\x0F\x00\x00').finditer(struct)
        for matchUseRouter in matchesUseRouter:
            useRouter = bool(matchUseRouter.end(0) + 20)
            ethernet.UseRouter = useRouter

        matchesUseIP = re.compile(b'\xEa\x0F\x00\x00\xEA\x0F\x00\x00').finditer(struct)
        for matcheUseIP in matchesUseIP:
            useRouter = bool(matcheUseIP.end(0) + 20)
            ethernet.UseIp = useRouter

        matchesUseMAC = re.compile(b'\xED\x0F\x00\x00\xED\x0F\x00\x00').finditer(struct)
        for matcheUseMAC in matchesUseMAC:
            useMAC = bool(matcheUseMAC.end(0) + 20)
            ethernet.UseIso = useMAC

        NetworkInterfaces[id] = ethernet

    for structure in matchesMPIStructure:
        struct = completeBuffer[structure.end(0): structure.end(0) + 2001]
        id = int.from_bytes(struct[:4], "little")
        MPI = MpiProfibusInterface()
        MPI._id = id

        matchesName = re.compile(b'Baugruppenname').finditer(struct)
        for matchName in matchesName:
            Name = struct[matchName.end(0) + 11: matchName.end(0) + 11 + int(struct[matchName.end(0) + 10])]
            MPI.Name = Name.decode("ISO-8859-1")


        matchesMPI = re.compile(b'\x9A\x08\x00\x00\x9A\x08\x00\x00').finditer(struct)
        for matchMPI in matchesMPI:

            MPI.Type = interface.MPI
            MPI.Address = int(struct[matchMPI.end(0) + 17])
            NetworkInterfaces[id] = MPI

    for structure in matchesDPStructure:
        struct = completeBuffer[structure.end(0): structure.end(0) + 2001]
        id = int.from_bytes(struct[:4], "little")

        DP = MpiProfibusInterface()
        DP._id = id

        matchesName = re.compile(b'Baugruppenname').finditer(struct)
        for matchName in matchesName:
            Name = struct[matchName.end(0) + 11: matchName.end(0) + 11 + int(struct[matchName.end(0) + 10])]
            DP.Name = Name.decode("ISO-8859-1")

        matchesDP = re.compile(b'\x36\x08\x00\x00\x36\x08\x00\x00').finditer(struct)
        for matchDP in matchesDP:
            DP.Type = interface.DP
            DP.Address = int(struct[matchDP.end(0) + 17])
            NetworkInterfaces[id] = DP


    return NetworkInterfaces



