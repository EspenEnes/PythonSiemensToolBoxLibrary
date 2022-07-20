from dataclasses import dataclass, field
from . import StationType
from .s7ProgramFolder import S7ProgrammFolder


@dataclass
class StationConfigurationFolder:
    objTyp: int = field(init=True, repr=False)
    Name: str = field(init=True, default="", repr=True)
    UnitID: int = field(init=True, default=None,  repr=False)
    modules: list = field(init=True, default_factory=lambda: [], repr=False)


    def __post_init__(self):
        self.stationType = StationType(self.objTyp)

    def getAllNetworkInterfaces(self):
        tmpInterfaces = list()
        for module in self.modules:
            tmpInterfaces.append(module.NetworkInterfaces)
        return [val for sublist in tmpInterfaces for val in sublist]

    @property
    def blockOfflineFolders(self):
        tmpFolders = list()
        for module in self.modules:
            if hasattr(module, "subItems"):
                for item in module.subItems:
                    if type(item) == S7ProgrammFolder:
                        tmpFolders.append(item.blockOfflineFolder)
        return tmpFolders




    # def __repr__(self):
    #     return self.Name





    # @stationType.setter
    # def stationType(self, value):
    #     if value == StationType.Simatic300.value:
    #         self._stationType = PLCType.Simatic300
    #     elif value == StationType.Simatic400.value:
    #         self._stationType = PLCType.Simatic400
    #     elif value == StationType.Simatic400H.value:
    #         self._stationType = PLCType.Simatic400H
    #     elif value == StationType.SIAMTICPC.value:
    #         self._stationType = PLCType.SimaticRTX
