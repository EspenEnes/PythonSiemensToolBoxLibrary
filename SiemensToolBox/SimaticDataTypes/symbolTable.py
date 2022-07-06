from dataclasses import dataclass, field
from dbfread import DBF


@dataclass
class SymbolTable():
    folder: str = field(init=True, default="", repr=False)
    Name: str = field(init=True, default="", repr=True)
    _symbols: dict = field(init=True, default_factory=lambda: {}, repr=False)
    _loaded: bool = field(init=True, default=False, repr=False)

    @property
    def symbols(self):
        if self._loaded:
            return self._symbols

        dbf = DBF(f"{self.folder}\\SYMLIST.DBF", raw=True)
        sym = {}
        for row in dbf.records:
            operand = "".join(x.strip() for x in row["_OPHIST"].decode("ISO-8859-1").split())
            sym[operand] = {}

            sym[operand]["symbol"] = row["_SKZ"].decode("ISO-8859-1").strip()
            sym[operand]["operand"] = row["_OPHIST"].decode("ISO-8859-1").strip()
            sym[operand]["operandIEC"] = row["_OPIEC"].decode("ISO-8859-1").strip()
            sym[operand]["dataType"] = row["_DATATYP"].decode("ISO-8859-1").strip()
            sym[operand]["comment"] = row["_COMMENT"].decode("ISO-8859-1").strip()
        self._symbols = sym
        self._loaded = True
        return sym
