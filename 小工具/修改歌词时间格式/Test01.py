from os import listdir
for file in listdir():
    if file[-3:].upper() == "LRC" or file[-3:].upper() == "TXT":
        file_path = file
        line_list = []
        with open(file_path,mode="r",encoding="utf-8") as r:
            for line in r:
                line_list.append(line[0:9] + line[10:])
        with open(file_path,mode="w",encoding="utf-8") as w:
            for line in line_list:
                w.write(line+"\n")
            