# from pathlib import Path
# print(*Path("C:\Users\Lab Engineer.DESKTOP-HN2JAP3\Documents\i_simpa_scripts\otherScripts").iterdir(), sep="\n")
in_type = input("Is the input a file? (y/n):\n")

codecs=['latin1', 'utf-8', 'utf-16', 'cp1251', 'cp1252', 'ascii', 'binhex']
# "C:\\Users\\Lab Engineer.DESKTOP-HN2JAP3\\OneDrive\\Documents\\Github Repos\\i_simpa_scripts\\otherScripts\\Sound_level.csbin"
try:
    if in_type.lower()=="y":
        input_data = input("Input file location:\n")
        try:
            with open(input_data, mode="rb") as file_in:
                lines = []
                for line in file_in:
                    lines.append(line)
            del(file_in)

            for codec in codecs:
                try:
                    print(lines[0].decode(codec) + " - using" + codec)
                except:
                    print(f"Decode using {codec} failed")
            # for line in lines:
                  # print(line)
    #             # print("\n")

    #             # print(int.from_bytes(line, byteorder='little'))
    #             # print("\n")
                
    #             try:
    #                 print(line.decode('utf-8'))
    #             except:
    #                 print("line read failed")
    #     except:
    #         print("Issue occurred")
    # if in_type.lower()=='n':
    #     input_data = input("Input String:\n")
    #     try:
    #         s = input_data
    #         print(s.encode('latin1').decode('cp1252'))
        except:
            print("Invalid Input")
except:
    print("invalid answer")

