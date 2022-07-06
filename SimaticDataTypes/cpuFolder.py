from dataclasses import dataclass, field

@dataclass
class CPUFolder:
    NetworkInterfaces: list = field(init=True, default_factory=lambda: [])
    subItems: list = field(init=True, default_factory=lambda: [])
    name: str = field(init=True, default="")

    parent = None
    unitID = None
    networkType = None
    networkId = None
    cpuType = None
    rack:int = None
    slot:int = None
    ID = None

    idTobjID = list()

    def __repr__(self):
        return self.name
