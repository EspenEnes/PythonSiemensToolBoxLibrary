import re
from collections import OrderedDict
from typing import Tuple, Any
from copy import deepcopy

from anytree import Node, RenderTree
from dataclasses import dataclass


@dataclass
class Row():
    name = None
    path = None
    _dataType = ""
    initialValue = None
    comment = None
    address = None

    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        data = value.split(":=")
        if len(data) > 1:
            self._dataType = data[0].strip()
            self.initialValue = data[1]
        else:
            self._dataType = value.strip()


class MyNode(Node):
    separator = "."


class Getlayout():

    def __init__(self, parent=None, rows=[]):
        # _parent is where we find the folders blocklist (BlockOfflineFolder)
        self._nodeTree = None
        self._parent = parent

        self.root, _ = self._structToDict(rows)

    @property
    def nodeTree(self):
        # take an nested dictionary and make a nodetree
        if not self._nodeTree:
            rootNode = MyNode("root")

            # construct nodetree
            self._nodeTree = self._dictToNodeTree(self.root, rootNode)

            # Concatinate DB addresses to node leaves
            self.getPlcAdress(self._nodeTree)
        return self._nodeTree

    @nodeTree.setter
    def nodeTree(self, value):
        # Store nodetree as variable in class
        self._nodeTree = value

    def _structToDict(self, rows) -> tuple[OrderedDict, int]:
        # Parse throe all elements of a block and make a nested dictionary with row elements
        root = OrderedDict()
        _rowix = 0

        while _rowix < len(rows):

            if _namedStruct := re.compile("^(\w+)\s:\sSTRUCT").search(rows[_rowix]):

                # Recursive call
                root[_namedStruct[1]], layoutLen = self._structToDict(rows[_rowix + 1:])
                _rowix += layoutLen + 1

            elif _struct := re.compile("^STRUCT").search(rows[_rowix]):
                _rowix += 1

            elif rows[_rowix] == "VAR_INPUT":
                root["in"], layoutLen = self._structToDict(rows[_rowix + 1:])
                _rowix += layoutLen + 1

            elif rows[_rowix] == "VAR_OUTPUT":
                root["out"], layoutLen = self._structToDict(rows[_rowix + 1:])
                _rowix += layoutLen + 1

            elif rows[_rowix] == "VAR_IN_OUT":
                root["inout"] = OrderedDict()
                data, len_data = self._structToDict(rows[_rowix + 1:])
                for key, value in data.items():
                    row = Row()
                    row.name = key
                    if type(value) == OrderedDict:
                        row.dataType = "POINTER"
                    else:
                        if value.dataType in ["BOOL", "BYTE", "WORD", "DWORD", "INT", "DINT", "REAL", "S5TIME", "TIME", "TIMER",
                                              "DATE", "TIME_OF:DAY", "CHAR", "STRING", "ANY", "DATE_AND_TIME",
                                              "BLOCK_DB"]:
                            row.dataType = value.dataType

                    root["inout"][key] = row
                _rowix += len_data + 1



            elif item := re.compile("(^\w+)\s+:\s+(.*)").search(rows[_rowix]):


                # check if type is an externalSorce like UDT, FB, SFB
                if ExternalSource := re.compile("^(UDT*|FB*|SFB*)+\s(\d+)").search(item[2]):
                    root[item[1]] = deepcopy(
                        self._parent.getBlockLayout(f"{ExternalSource[1]}{ExternalSource[2]}").layout)
                    _rowix += 1

                # check if type is an array
                elif array := re.compile("^ARRAY\s+\[(\d+)\s+..\s+(\d+)\s+]\s+OF\s(.*)").search(item[2]):
                    root[item[1]] = OrderedDict()

                    # Get correct type of array
                    if len(array[3].split("//")[0]) > 0:
                        _type = array[3].split("//")[0]
                        _rowix += 1
                    else:
                        _type = rows[_rowix + 1].replace(";", "").strip().split("\t")[0]
                        _rowix += 2

                    # check if type is an struct and needs to be parsed out
                    if _type.strip() == "STRUCT":

                        for x in range(int(array[1]), int(array[2]) + 1):
                            layout, layoutLen = self._structToDict(rows[_rowix:])  # todo: do deep copy of dict
                            root[item[1]][f"{x}"] = deepcopy(layout)
                        _rowix += layoutLen

                    # check if type is an externalSorce like UDT, FB, SFB
                    elif ExternalSource := re.compile("^(UDT*|FB*|SFB*)+\s(\d+)").search(_type):
                        layout = deepcopy(self._parent.getBlockLayout(f"{ExternalSource[1]}{ExternalSource[2]}").layout)
                        for x in range(int(array[1]), int(array[2]) + 1):
                            root[item[1]][f"{x}"] = deepcopy(layout)

                    # Add Type
                    else:
                        for x in range(int(array[1]), int(array[2]) + 1):
                            row = Row()
                            row.name = x
                            row.dataType = _type.replace(";", "").strip()
                            if len(item[2].split("//")) > 1:
                                row.comment = item[2].split("//")[1].strip()

                            root[item[1]][f"{x}"] = row



                elif multi_array := re.compile("^ARRAY\s+\[(\d+)\s+..\s+(\d+),\s+(\d+)\s+..\s+(\d+)\s+]\s+OF\s(.*)").search(item[2]):
                    root[item[1]] = OrderedDict()

                    if len(multi_array[5].split("//")[0]) > 0:
                        _type = array[5].split("//")[0]
                        _rowix += 1
                    else:
                        _type = rows[_rowix + 1].replace(";", "").strip().split("\t")[0]
                        _rowix += 2

                    for x in range(int(multi_array[1]), int(multi_array[2]) + 1):
                        for y in range(int(multi_array[3]), int(multi_array[4]) + 1):
                            row = Row()
                            row.name = f"{x}.{y}"
                            if len(multi_array[5].split("//")) > 1:
                                row.comment = multi_array[5].split("//")[1].strip()
                            row.dataType = _type.replace(";", "").strip()
                            root[item[1]][f"{x}.{y}"] = row
                # Add Type
                else:
                    row = Row()
                    row.name = item[1]
                    row.dataType = item[2].split("//")[0].strip().replace(";", "").strip()
                    row.dataType = row.dataType.split("\t")[0].strip()
                    if len(item[2].split("//")) > 1:
                        row.comment = item[2].split("//")[1].strip()
                    root[item[1]] = row
                    _rowix += 1



            # Return  Struct
            elif rows[_rowix] == "END_STRUCT;" or rows[_rowix] == "END_VAR" or rows[_rowix] == "END_STRUCT ;" or rows[
                _rowix].startswith("END_STRUCT"):
                _rowix += 1
                return root, _rowix

            elif rows[_rowix] == "VAR_TEMP":
                return root, _rowix

            # if here, we are loosing data, add rowix with 1 so we dont go in loop
            else:
                _rowix += 1

        return root, _rowix

    def _dictToNodeTree(self, dict: OrderedDict, root):

        for key, value in dict.items():
            if type(value) == OrderedDict:
                self._dictToNodeTree(value, MyNode(key, root))
            else:
                _node = MyNode(key, root)
                _node.__setattr__("row_data", value)
        return root

    def getPlcAdress(self, root: MyNode):
        adress = 0
        old = None

        Types = {"BOOL": 1, "BYTE": 8, "WORD": 16, "DWORD": 32, "INT": 16, "DINT": 32, "REAL": 32, "S5TIME": 16,
                 "TIME": 32, "TIMER": 16,
                 "DATE": 16, "TIME_OF:DAY": 32, "CHAR": 8, "STRING": 8, "ANY": 80, "DATE_AND_TIME": 64, "BLOCK_DB": 2,
                 "POINTER": 48}

        for node in root.leaves:

            # check if leaf has row_data atribute
            if not hasattr(node, "row_data"):
                continue

            node.row_data.path = ".".join([str(_.name) for _ in node.path][1:])

            # start at even byte if struct change
            if ".".join(node.row_data.path.split(".")[:-1]) != old or node.row_data.dataType not in ["BOOL", "BYTE"]:


                if len(node.row_data.path.split(".")) > 2 and node.row_data.path.split(".")[-2].isdigit() and node.row_data.path.split(".")[-1].isdigit():
                    if ".".join(node.row_data.path.split(".")[:-1]) != ".".join(old.split(".")):
                        if adress % 8 != 0:
                            adress += (8 - (adress % 8))

                else:

                    if adress % 8 != 0:
                        adress += (8 - (adress % 8))
                    if (adress // 8) % 2 != 0:
                        adress += 8
                old = ".".join(node.row_data.path.split(".")[:-1])

            # Add DB Adress to Node
            node.row_data.address = f"{adress // 8}.{adress % 8}"

            # Increement adress
            if node.row_data.dataType.startswith('STRING'):
                size = re.compile(".*\[(\d+)\s]").search(node.row_data.dataType)[1]
                adress += int((int(Types.get('STRING')) * int(size) + 16))
            else:
                adress += int(Types.get(node.row_data.dataType))

    @property
    def layout(self):
        return self.root

    @property
    def dbLayout(self):
        output = []
        for node in self.nodeTree.leaves:
            if hasattr(node, "row_data"):
                output.append((node.row_data.address, node.row_data.path, node.row_data.dataType))

        return output
