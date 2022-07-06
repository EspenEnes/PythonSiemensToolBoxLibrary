from dataclasses import dataclass, field
import codecs
from readProjectHeader import readProjectHeader
import os



@dataclass
class Project():
    """Base project class, only necessary input variable is projectFile. Other variables will autogenertate if they are missing """

    projectFile: str = field(init=True, repr=False)
    projectName: str = field(init=True, repr=True, default= None)

    projectPath: str = field(init=True, repr=False, default=None)
    projectEncoding: codecs.Codec = field(init=True, repr=False, default_factory=lambda: [codecs.lookup("ISO-8859-1")])



    def __post_init__(self):
        if (not self.projectName) and self.projectFile.lower().endswith(".s7p"):
            with open(self.projectFile, "rb") as f:
                self.projectName = readProjectHeader(f)

        if (not self.projectPath) and self.projectFile.lower().endswith(".s7p"):
            self.projectPath = os.path.split(self.projectFile)[0]

        if self.projectFile.endswith(".zip"):
            self.projectZipFile = self.projectFile
            self.projectFile = None

















