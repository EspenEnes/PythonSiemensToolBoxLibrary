from enum import Enum, auto

class PlcItemType(Enum):
    BOOL = 1
    BYTE = 8
    WORD = 16
    DWORD = 32
    INT = 16
    DINT = 32
    REAL = 32
    S5TIME = 16
    TIME = 32
    DATE = 16
    TIME_OF_DAY = 32
    CHAR : 8
    STRING: 8
    ANY = 80
    DATE_AND_TIME = 64

class BlockType(Enum):
    AllBlocks = 0xffff
    AllEditableBlocks = 0xfffe
    SourceBlock = 2

    # Step7 Types...
    OB = 0x08  # 8
    DB = 0x0a  # 10
    SDB = 0x0b  # 11
    FC = 0x0c  # 12
    SFC = 0x0d  # 13
    FB = 0x0e  # 14
    SFB = 0x0f  # 15
    UDT = 0x00  # 0
    VAT = 0x1B  # 27

    # Step5 Types...
    S5_PB = 0xf04
    S5_FB = 0xf08
    S5_FX = 0xf05
    S5_DB = 0xf01
    S5_DX = 0xf0c
    S5_SB = 0xf02
    S5_OB = 0xf10
    S5_OK = 0xf51
    S5_PK = 0xf31
    S5_FK = 0xf41
    S5_FKX = 0xf5a
    S5_SK = 0xf21
    S5_DK = 0xf5b
    S5_DKX = 0xf5c
    S5_BB = 0xf64

    S5_FV = 0xff1
    S5_FVX = 0xff2
    S5_DV = 0xff3
    S5_DVX = 0xff4

    # TIA Portal7 Types...
    S7V11_OB = 0xe08
    S7V11_DB = 0xe0a
    S7V11_SDB = 0xe0b
    S7V11_FC = 0xe0c
    S7V11_SFC = 0xe0d
    S7V11_FB = 0xe0e
    S7V11_SFB = 0xe0f
    S7V11_UDT = 0xeff
    S7V11_VAT = 0xe1B

class StationType(Enum):
    Simatic300 = 1314969
    Simatic400 = 1314970
    Simatic400H = 1315650
    SimaticPC = 1315651

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

class ProjectType(Enum):
    Step5 = auto()
    Step7 = auto()

class interface(Enum):
    IP = auto()
    MPI = auto()
    DP = auto()

class PLCType(Enum):
    Simatic300 = 1314969
    Simatic400 = 1314970
    Simatic400H = 1315650
    Simatic400H_backup = 1315656
    SimaticRTX = 1315651
    EternetInCPU3xx = 2364796
    EternetInCPU3xx_2 = 2364572
    EternetInCPU3xxF = 2364818
    EternetInCPU4xx = 2364763
    EternetInCPURTX = 2364315
    MpiDPinCPU = 1314972
    MpiDP400 = 1315038
    MpiDP300 = 1315016

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
