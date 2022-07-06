from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class BlockBytes:
    mc7code: bytes = field(init=True, default=None, repr=False)
    uda: bytes = field(init=True, default=None, repr=False)
    subblocks: bytes = field(init=True, default=None, repr=False)
    comments: bytes = field(init=True, default=None, repr=False)
    addinfo: bytes = field(init=True, default=None, repr=False)
    blkinterface: str = field(init=True, default=None, repr=False)
    blkinterfaceInMC5: bytes = field(init=True, default=None, repr=False)
    nwinfo: bytes = field(init=True, default=None, repr=False)
    blockdescription: bytes = field(init=True, default=None, repr=False)
    jumpmarks: bytes = field(init=True, default=None, repr=False)
    knowHowProtection: bool = field(init=True, default=False, repr=False)
    username: str = field(init=True, default=None, repr=False)
    version: str = field(init=True, default=None, repr=False)
    IsInstanceDB: bool = field(init=True, default=False, repr=False)
    IsSFB: bool = field(init=True, default=False, repr=False)
    FBNumber: int = field(init=True, default=None, repr=False)
    CheckSum: int = field(init=True, default=0, repr=False)
    BlockLanguage: str = field(init=True, default=None, repr=False)

    _LastCodeChange: datetime = field(init=True, default_factory=lambda : datetime(1984, 1, 1, 0, 0, 0, 0), repr=False)
    _LastInterfaceChange: datetime = field(init=True, default_factory=lambda : datetime(1984, 1, 1, 0, 0, 0, 0), repr=False)

    @property
    def LastCodeChange(self):
        return self._LastCodeChange

    @LastCodeChange.setter
    def LastCodeChange(self, value):
        self._LastCodeChange = self._getTimeStamp(value)

    @property
    def LastInterfaceChange(self):
        return self._LastInterfaceChange

    @LastInterfaceChange.setter
    def LastInterfaceChange(self, value):
        self._LastInterfaceChange = self._getTimeStamp(value)

    def _getTimeStamp(self, strTime):
        try:
            time = bytes(strTime, "ISO-8859-1")
            delta = timedelta(milliseconds=time[0] * 0x1000000 + time[1] * 0x10000 + time[2] * 0x100 + time[3])
            delta += timedelta(days=time[4] * 0x100 + time[5])

            dt = datetime(1984, 1, 1, 0, 0, 0, 0)
            dt += delta
            return dt
        except:
            dt = datetime(1984, 1, 1, 0, 0, 0, 0)
            return dt



