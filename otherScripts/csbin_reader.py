# from pathlib import Path
# print(*Path("C:\Users\Lab Engineer.DESKTOP-HN2JAP3\Documents\i_simpa_scripts\otherScripts").iterdir(), sep="\n")

with open("C:\\Users\\Lab Engineer.DESKTOP-HN2JAP3\\Documents\\i_simpa_scripts\\otherScripts\\Sound level.csbin", mode="rb") as file_in:
    lines = []
    for line in file_in:
        lines.append(line)

del(file_in)

for line in lines:
    x=line.decode('cp1252')
    print(x)
    print(x.encode('utf-8'))

# s = u'Zåìôèðà'
# print(s.encode('latin1').decode('cp1251'))