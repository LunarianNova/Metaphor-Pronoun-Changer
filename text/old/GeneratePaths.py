import sys
import os
from mfmessages import Message

def rewrite_file(filename):
    try:
        with open(filename) as file:
            file = file.read()
            built_messages = []
            lines = file.split("\n")
            startstripped = []
            while lines[0].strip() != "//--------------------------":
                startstripped.append(lines[0])
                lines = lines[1:]
            messages = "\n".join(lines).split("//--------------------------")[1:]
            for i, message in enumerate(messages):
                oldmessage = "//--------------------------\n"+message[1:-1]
                newmessage = Message(message)
                newmessage.rebuild()
                built_messages.append(newmessage.built)
                # if oldmessage != newmessage.built:
                #     print(oldmessage)
                #     print("|||||||||||")
                #     print(newmessage.built)
                #     print("\n\n||||||||||||||||||||||||||||||\n\n")
            with open("new.txt", "w") as file:
                for line in startstripped:
                    file.write(line+"\n")
                file.write("\n".join(built_messages)+"\n")
            with open(filename) as file:
                with open("new.txt") as file2:
                    txt = file.read()
                    txt2 = file2.read()
                    if txt != txt2:
                        return False
                    return True
    except IndexError:
        return False
    except UnicodeDecodeError:
        return False

# file = sys.argv[1]
# rewrite_file(file)

count = 0
failed = 0
rootdir = sys.argv[1]
paths = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".msg"):
            if "\system" not in filepath:
                count += 1
                if not rewrite_file(filepath):
                    failed += 1
                    print(filepath)
                else:
                    paths.append(filepath)

print(count)
print(failed)
with open("paths.txt", "w") as file:
    file.write("\n".join(paths))