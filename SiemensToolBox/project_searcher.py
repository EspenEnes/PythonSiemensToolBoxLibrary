import zipfile
import os
from .readProjectHeader import readProjectHeader
from .readProjectEncoding import readProjectEncoding
from .Step7V5.project import ProjectV5


class Step7Finder:
    @classmethod
    def readProjectHeader(cls, file):
        return readProjectHeader(file)


    @classmethod
    def readProjectEncoding(cls, file):
        return readProjectEncoding(file)


    @classmethod
    def appendToDict(cls,projectfile, name, StorageLocation, Codec):
        if name:
            record = ProjectV5(projectfile, name)
        else:
            record = ProjectV5(projectfile)

        record.projectPath = StorageLocation
        if Codec:
            record.projectEncoding = Codec
        return record

    @classmethod
    def search(cls, path=r"C:\Users\enese\Documents\Jobb-Mappa\Askeladden ( R5547)\aaaaa"):

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".s7p"):
                    with open(os.path.join(root, file), "rb") as f:
                        projectName = None#cls.readProjectHeader(f)
                        projectpath = os.path.join(root)
                        projectfile = os.path.join(root, file)


                        try:
                            with open(os.path.join(root, "Global", "Language")) as f:
                                projectEncoding = cls.readProjectEncoding(f)
                        except FileNotFoundError:
                            projectEncoding = None

                        yield cls.appendToDict(projectfile, projectName, projectpath, projectEncoding)
                        dirs[:] = []
                        break


                elif file.endswith(".zip"):
                    try:
                        with zipfile.ZipFile(os.path.join(root, file), "r") as myzip:
                            for zfile in myzip.infolist():
                                if zfile.filename.endswith(".s7p"):
                                    zipRoot = os.path.split(zfile.filename)[0]

                                    with myzip.open(zfile) as myfile:
                                        projectName = cls.readProjectHeader(myfile)
                                        projectfile= os.path.join(root, file)
                                        projectpath = None

                                    try:
                                        languageFile = os.path.join(zipRoot, r"Global\Language")
                                        with myzip.open(languageFile) as myfile:
                                            projectEncoding = cls.readProjectEncoding(myfile)
                                    except KeyError:
                                        projectEncoding = None

                                    yield cls.appendToDict(projectfile, projectName,projectpath, projectEncoding)

                    except (zipfile.error, PermissionError):
                        continue
