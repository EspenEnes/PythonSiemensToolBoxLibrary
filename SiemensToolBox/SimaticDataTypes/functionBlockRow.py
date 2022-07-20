from dataclasses import dataclass, field

@dataclass
class S7FunctionBlockRow:
    networkName: str = field(init=True, default="")
    comment: str = field(init=True, default="")