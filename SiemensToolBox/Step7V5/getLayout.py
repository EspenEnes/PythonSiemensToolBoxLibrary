import re
from collections import OrderedDict


class Getlayout():
    def __init__(self, parent, rows):
        self._rowix = 0
        self._parent = parent
        self.layout = self.getStruct(rows)

    def getStruct(self, rows, name=""):
        def parseOutComment(row):
            _tmpComment = re.compile(".*\/\/(.*$)").search(row)
            if not _tmpComment:
                return row
            return row[:_tmpComment.start(1) - 2]

        def parseOutTypeValue(_type):
            _tmpType = re.compile(".*:=(.*)").search(_type)
            if not _tmpType:
                return _type
            return _type[:_tmpType.start(1) - 2]

        root = OrderedDict()
        while self._rowix < len(rows):
            # _row = Row(rows[self._rowix])

            row = rows[self._rowix].strip()
            if row == "VAR_TEMP": return root
            _comment = re.compile("^.*//(.*$)").search(row)

            row = parseOutComment(row)
            _namedStruct = re.compile("^(\w+)\s:\sSTRUCT").search(row)
            EndStruct = re.compile("^(\w+)$").search(row)

            if _namedStruct:
                struct = GetStruct(rows[self._rowix + 1:])
                if struct:
                    layout = Getlayout(self._parent, struct).layout
                    root[f"{_namedStruct.group(1)}"] = OrderedDict()
                    for key, value in layout.items():
                        root[f"{_namedStruct.group(1)}"][key] = value
                    self._rowix += len(struct) + 2
                    continue

            elif EndStruct:
                struct = GetStruct(rows[self._rowix + 1:])
                if struct:
                    layout = Getlayout(self._parent, struct).layout
                    for key, value in layout.items():
                        root[key] = value
                    self._rowix += len(struct) + 2
                    continue

            item = re.compile("(^\w+)\s+:\s+(.*)").search(row)
            if item:
                name = item.group(1)
                _type = item.group(2)

                FB = re.compile("^FB\s(\d+);").search(_type)
                UDT = re.compile("^UDT\s(\d+);").search(_type)
                SFB = re.compile("^SFB\s(\d+)").search(_type)
                array = re.compile("^ARRAY\s+\[(\d+)\s+..\s+(\d+)\s+]\s+(OF.*)").search(_type)

                if FB:
                    layout = self._parent.getBlockLayout(f"FB{FB.group(1)}").layout
                    root[name] = layout
                elif UDT:
                    layout = self._parent.getBlockLayout(f"UDT{UDT.group(1)}").layout
                    root[name] = layout

                elif SFB:
                    layout = self._parent.getBlockLayout(f"SFB{SFB.group(1)}").layout
                    root[name] = layout
                elif array:
                    start = array.group(1)
                    stop = array.group(2)

                    if len(array.group(3).replace("OF", "").strip()) > 0:
                        _type = parseOutTypeValue(array.group(3).replace("OF", "").strip()).replace(";", "").strip()
                    else:
                        _type = parseOutTypeValue(rows[self._rowix + 1]).replace(";", "").strip()

                    if _type.strip() == "STRUCT":
                        struct = GetStruct(rows[self._rowix + 1:])
                        layout = Getlayout(self._parent, struct).layout
                        for item in range(int(start), int(stop) + 1):
                            root[f"{name}{[item]}"] = OrderedDict()
                            for key, value in layout.items():
                                root[f"{name}{[item]}"][key] = value
                        self._rowix += len(struct) + 2
                        continue

                    else:
                        FB = re.compile("^FB\s(\d+)").search(_type)
                        UDT = re.compile("^UDT\s(\d+)").search(_type)
                        SFB = re.compile("^SFB\s(\d+)").search(_type)

                        if FB:
                            layout = self._parent.getBlockLayout(f"FB{UDT.group(1)}").layout
                            for item in range(int(start), int(stop) + 1):
                                root[f"{name}[{item}]"] = layout
                        elif UDT:
                            layout = self._parent.getBlockLayout(f"UDT{UDT.group(1)}").layout
                            for item in range(int(start), int(stop) + 1):
                                root[f"{name}[{item}]"] = layout
                        elif SFB:
                            layout = self._parent.getBlockLayout(f"SFB{UDT.group(1)}").layout
                            for item in range(int(start), int(stop) + 1):
                                root[f"{name}[{item}]"] = layout
                        else:

                            for item in range(int(start), int(stop) + 1):
                                root[f"{name}{[item]}"] = parseOutTypeValue(_type).replace(";", "").strip()

                else:
                    root[name] = parseOutTypeValue(_type).replace(";", "").strip()
            self._rowix += 1
        return root

    def listLayout(self, df=None, parent=None):
        ls = []
        if df == None:
            df = self.layout
        for key, value in df.items():
            if type(value) == OrderedDict:
                if parent:
                    key = f"{parent}.{key}"
                res = self.listLayout(value, key)
                for x in res:
                    ls.append(x)
            else:
                if parent:
                    ls.append(f"{parent}.{key} : {value}")
                else:
                    ls.append(f"{key} : {value}")
        return ls

    @property
    def dbLayout(self):
        rows = self.listLayout()

        def checkType(type: str, types: dict) -> int:

            if type.startswith('STRING'):
                size = re.compile(".*\[(\d+)\s]").search(type).group(1)
                return int((int(types.get('STRING')) * int(size) + 16))

            else:
                try:
                    return int(types.get(type))
                except ValueError:
                    print(f"concatDBAdress {type}")
                    return 0

        outData = list()
        adress = 0
        dirty = True
        oldname = None

        Types = {"BOOL": 1, "BYTE": 8, "WORD": 16, "DWORD": 32, "INT": 16, "DINT": 32, "REAL": 32, "S5TIME": 16,
                 "TIME": 32,
                 "DATE": 16, "TIME_OF:DAY": 32, "CHAR": 8, "STRING": 8, "ANY": 80, "DATE_AND_TIME": 64}

        ixRows = 0
        while ixRows < len(rows):
            row = rows[ixRows]

            item = re.compile("(^.*)\s:\s(.*)(?:\s;)*").search(row)

            pitem = re.compile("(^.*)\s:\s(.*)(?:\s;)*").search(rows[ixRows - 1])

            if item:
                name = item.group(1)
                #is there a struct change??
                if oldname:
                    dirty = ".".join(name.split(".")[:-1]) != ".".join(oldname.split(".")[:-1])
                #we have a typechange into a array
                if (item.group(2) != pitem.group(2)) and item.group(1).endswith("]") :
                    dirty = True
                if item.group(1).endswith("]") and not pitem.group(1).endswith("]"):
                    dirty = True

                elif not dirty:
                    if item.group(2) == "BYTE":
                        if adress % 8 != 0:
                            adress += (8 - (adress % 8))


                _type = item.group(2)

                if _type in Types.keys() or _type.startswith("STRING"):
                    if _type not in ["BOOL", "BYTE"] or dirty:
                        if adress % 8 != 0:
                            adress += (8 - (adress % 8))
                        if (adress // 8) % 2 != 0:
                            adress += 8


                oldname = name
                outData.append([f"{adress // 8}.{adress % 8}", name, _type])
                adress += checkType(_type, Types)
                ixRows += 1
        return outData


def GetStruct(rows):
    output = []
    for row in rows:
        _tmpComment = re.compile(".*\/\/(.*$)").search(row)
        if _tmpComment:
            row = row[:_tmpComment.start(1) - 2]

        if row == "END_STRUCT;" or row == "END_VAR" or row == "END_STRUCT ;" or row.startswith("END_STRUCT"):
            return output
        output.append(row)
    return output
