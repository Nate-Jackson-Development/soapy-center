def dumpToFile(name, content):
    with open(name+".txt") as f:
        f.write(content)