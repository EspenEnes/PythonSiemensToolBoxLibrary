import tempfile
import zipfile

def getProjectfolder(file: str) -> tuple:
    if file.lower().endswith(".s7p"):
        return "\\".join(file.split("\\")[:-1]), file,  None
    elif file.lower().endswith(".zip"):
        zip = zipfile.ZipFile(file)

        for zfile in zip.filelist:
            if zfile.filename.endswith(".s7p"):
                dir = tempfile.TemporaryDirectory()
                zip.extractall(dir.name)
                root = "/".join(zfile.filename.split("/")[:-1])
                file = zfile.filename

                projectfolder = f"{dir.name}/{root}".replace("/", "\\")
                projectFile = f"{dir.name}/{file}".replace("/", "\\")

                return projectfolder, projectFile, dir