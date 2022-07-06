import codecs

def readProjectEncoding(file):
    results = []
    languageFile = file.readlines()
    for line in languageFile:
        try:
            result = codecs.lookup(line)
            results.append(result)
        except LookupError:
            continue
    return results

