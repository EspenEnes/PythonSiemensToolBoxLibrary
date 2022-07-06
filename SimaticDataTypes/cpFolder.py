from dataclasses import dataclass, field


@dataclass
class CpFolder():
    ID: int = field(init=True, repr=True)
    NetworkInterfaces: list = field(init=True, default_factory=lambda: [])
    idTobjId: list = field(init=True, default_factory=lambda: [])
    name: str = field(init=True, default=None)
    parent = None

    unitID: int = None
    objTyp: int = None
    networkType: int = None
    subModulNumber: int = None
    subModule = None

    rack: int = None
    slot: int = None

    networkId = None # forgein Key ProfinetSystem

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return str(self.ID)

