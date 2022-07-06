

def readProjectHeader(file):
    data = file.read()
    startindex = 5
    span = int(data[startindex - 1])
    stopindex = startindex + span
    name = data[startindex: stopindex].decode("ISO-8859-1")

    startindex = stopindex + 5
    span = int(data[startindex - 1])
    stopindex = startindex + span
    description = data[startindex: stopindex].decode("ISO-8859-1")
    return name