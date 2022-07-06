import re


def linkOfflineblockFolderWithProgrammFolder(projectFolder, blocksOfflineFolders, s7ProgramFolders):
    file = projectFolder + "\\" + "hrs" + "\\" + "linkhrs.lnk"
    with open(file, "rb") as f:
        completeBuffer = f.read()

    for S7ProgrammFolder in s7ProgramFolders.values():
        position = S7ProgrammFolder._linkfileoffset

        match = re.compile(b"\x01\x60\x11\x00(.{2})").search(completeBuffer[position:])
        if match:
            Step7ProjectBlockFolderID = int.from_bytes(match.group(1), "little")

            try:
                folder = blocksOfflineFolders[Step7ProjectBlockFolderID]
                S7ProgrammFolder.blockOfflineFolder = folder
                folder._parent = S7ProgrammFolder
                break
            except KeyError:
                pass
