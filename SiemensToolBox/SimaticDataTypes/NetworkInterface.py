from dataclasses import dataclass, field
from .s7Types import interface


@dataclass
class  EthernetInterface:
    Type: interface = field(init=True, default=interface.IP, repr=True)
    Name: str = field(init=True, default=None, repr=True)
    Address: str = field(init=True, default=None, repr=True)
    _id: int = field(init=True, default=None, repr=False)

    UseIso: bool = field(init=True, default=False, repr=False)
    PhysicalAddress: str = field(init=True, default="", repr=False)
    UseIp: bool = field(init=True, default=None, repr=False)
    SubnetMask: str = field(init=True, default="", repr=False)
    UseRouter: bool = field(init=True, default=False, repr=False)
    IPAddressRouter: str = field(init=True, default="", repr=False)


@dataclass
class MpiProfibusInterface:
    Type: interface = field(init=True, default=interface.MPI, repr=True)
    Name: str = field(init=True, default=None, repr=True)
    Address: int = field(init=True, default=None, repr=True)
    _id: int = field(init=True, default=None, repr=False)

