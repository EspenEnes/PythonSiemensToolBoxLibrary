from dataclasses import dataclass, field
from .blockItem import BlockItem


@dataclass
class BlockLayout():
    rows: list = field(init=True)
    items: list = field(init=True, default_factory=lambda : ())

    def __post_init__(self):
        _rowix = 0

        while _rowix < len(self.rows):
            row = self.rows[_rowix].strip()
            if row == "VAR_TEMP": break
            item = BlockItem(self.rows[_rowix])

            if item.type_ == "STRUCT":
                STRUCT = True
                name = item.name
                while STRUCT:
                    item = BlockItem(self.rows[_rowix + 1])
                    if item.name.startswith("END_STRUCT"):
                        STRUCT = False
                        continue

                    item.name = f"{name}.{item.name}"
                    self.items.append(item)
                    print(item)
                    _rowix += 1









            _rowix += 1





