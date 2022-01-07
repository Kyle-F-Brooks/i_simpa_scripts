# from pathlib import Path
# print(*Path("C:\Users\Lab Engineer.DESKTOP-HN2JAP3\Documents\i_simpa_scripts\otherScripts").iterdir(), sep="\n")
in_type = input("Is the input a file? (y/n):\n")


# "C:\\Users\\Lab Engineer.DESKTOP-HN2JAP3\\Documents\\i_simpa_scripts\\otherScripts\\Sound level.csbin"

if in_type.lower()=="y":
    input_data = input("Input file location:\n")
    try:
        with open(input_data, mode="rb") as file_in:
            lines = []
            for line in file_in:
                lines.append(line)
        del(file_in)

        for line in lines:
            # x=line.decode('cp1252')
            print(line)
            print("\n")
            
            # try:
            #     print(line.decode('cp1252'))
            # except:
            #     pass
    except:
        print("Issue occurred")
if in_type.lower()=='n':
    input_data = input("Input file location:\n")
    try:
        s = input_data
        print(s.encode('latin1').decode('cp1251'))
    except:
        print("Invalid Input")
else:
    print("invalid answer")
