from dataclasses import dataclass, field
from SiemensToolBox.Step7V5 import *
from SiemensToolBox.getProjectFolder import getProjectfolder
from SiemensToolBox.project import Project
from SiemensToolBox.SimaticDataTypes import ProjectType



@dataclass
class ProjectV5(Project):
    """Project class for Step7V5 projects"""
    _projectloaded: bool = field(init=True, default=False, repr=False)

    ProjectType = ProjectType.Step7

    def getProjectFolder(self):
        """Will unpack a zipped project to a local temp folder and return the new path and project file, this is needed to be able to parse DBF files when parsing Step7 project"""
        if hasattr(self, "projectZipFile"):
            self.projectPath, self.projectFile, self._ziphelper = getProjectfolder(self.projectZipFile)

    def loadProject(self):
        self._projectloaded = True

        """Get The project folder, unpack if ZipFile"""
        self.getProjectFolder()

        """Get Hardware part of project"""
        self.stations = getAllProjectStations(self.projectPath)
        self._DpFolders = getAllDPfolders(self.projectPath)
        self._cpuFolder = getAllCpuFolders(self.projectPath, self.stations)
        self._cpFolder = getAllCommunicationProcessors(self.projectPath, self.stations)
        self._networkInterfaces = getAllNetworkInterfaces(self.projectPath)
        linkProfinetWithCpuCp(self.projectPath, self._cpuFolder, self._cpFolder, self._networkInterfaces)
        linkMpiDPWithCpuCp(self._cpuFolder, self._DpFolders, self._networkInterfaces)
        """Union of CP with interface and CP with station"""
        for cp in [x for x in self._cpFolder.values() if x.subModule]:
            [cp.NetworkInterfaces.append(x) for x in cp.subModule.NetworkInterfaces]
            del cp.subModule

        """Get Software part of project"""
        self._s7ProgrammFolders = getAllProgramFolders(self.projectPath)
        linkProgrammFolderWithCPU(self.projectPath, self._cpuFolder, self._s7ProgrammFolders)

        #self._blocksOfflineFolders = getAllBlocksOfflineFolders(self.projectPath)
        #linkOfflineblockFolderWithProgrammFolder(self.projectPath,self._blocksOfflineFolders, self._s7ProgrammFolders)
        #linkSymbolTableWithProgrammFolder(self.projectPath, self._s7ProgrammFolders)