from collections import Counter
import filehandler as fh
import mfmessages as mm
import regex as re
import os
from distutils.dir_util import copy_tree

MALE_FEMALE = {"boy": "girl", "boy'd": "girl'd", "boy's": "girl's", "boyfriend": "girlfriend", "boyo": "girly", 
               "gentleman": "lady", "guy": "girl", "he": "she", "he'd": "she'd", "he'll": "she'll", "he's": "she's",
               "heir": "heiress", "him": "her", "himself": "herself", "his": "her", "lad": "lass", "lad's": "lass's",
               "laddie": "lassie", "lord": "lady", "lord's": "lady's", "m'boy": "m'girl", "m'lord": "m'lady", 
               "man": "woman", "man's": "woman's", "mistah": "missus", "mister": "miss", "mister'll": "miss'll", 
               "mr": "ms", "p-prince": "p-princess", "prince": "princess", "prince's": "princess's", 
               "prince-impersonating": "princess-impersonating", "prince-infused": "princess-infused", 
               "princeliness": "princessliness", "princely": "princessly", "princey": "princessy", 
               "pro-prince": "pro-princess", "sir": "lady", "sire": "lady", "son": "daughter", "son's": "daughter's"}

MALE_NEUTRAL = {"boy": "kid", "boy'd": "kid'd", "boy's": "kid's", "boyfriend": "partner", "boyo": "kiddo",
                "gentleman": "chap", "guy": "guy", "he": "they", "he'd": "they'd", "he'll": "they'll", "he's": "they're",
                "heir": "heir", "him": "his", "himself": "themself", "his": "theirs", "lad": "lad", "lad's": "lad's",
                "laddie": "laddie", "lord": "liege", "lord's": "liege's", "m'boy": "lad", "m'lord": "m'liege",
                "man": "person", "man's": "person's", "mistah": "mistah", "mister": "mister", "mister'll": "mister'll",
                "mr": "mr", "p-prince": "h-heir", "prince": "heir", "prince's": "heir's",
                "prince-impersonating": "heir-impersonating", "prince-infused": "heir-infused",
                "princeliness": "heirliness", "princely": "heirly", "princey": "heiry",
                "pro-prince": "pro-heir", "sir": "sir", "sire": "sire", "son": "child", "son's": "child's"}

NEUTRAL_MANUAL = ["mistah", "mister", "mister'll", "mr", "sir", "sire"]

leftover = ["boys", "gentlemen", "king", "king'll", "king's", "king-ish", "king-picking", "king-to-be", "kingliness", "kingly", "kings", "men", "misters", "sirs"]

KING_FEMALE = {"boys": "girls", "gentlemen": "ladies", "king": "queen", "king'll": "queen'll", "king's": "queen's", "king-ish": "queen-ish", "king-picking": "queen-picking", "king-to-be": "queen-to-be", 
               "kingliness": "queenliness", "kingly": "queenly", "kings": "queens", "men": "women", "misters": "misses", "sirs": "misses"}
KING_NEUTRAL = {"boys": "folk", "gentlemen": "folk", "king": "ruler", "king'll": "ruler'll", "king's": "ruler's", "king-ish": "ruler-ish", "king-picking": "ruler-picking", "king-to-be": "ruler-to-be",
               "kingliness": "sovereignliness", "kingly": "sovereignly", "kings": "rulers", "men": "folk", "misters": "folks", "sirs": "folks"}

def get_regex(word) -> str:
    """
    Generate regex to match a word, and ignore punctuation
    """
    return f"(?<=^|[^a-zA-Z'_]){word}(?=$|[^a-zA-Z'_])"

def replace_word_in_message(filename, id, word, replacement, index=0) -> None:
    messages = mm.get_messages("output\\"+filename)
    original_messages = mm.get_messages(filename)
    try:
        message_object = messages[id]
    except:
        message_object = original_messages[id]

    text = replace_word("\n".join(message_object.text), word, replacement, index=index)
    message_object.text = text.split("\n")
    message_object.rebuild()
    messages[id] = message_object

    with open("output\\"+filename, "w") as file:
        file.write("\n".join([x.built for x in messages.values()]))

def generate_mismatched(lines: list) -> list:
    """
    Generates a list of lines where the word has a different number of occurences than you plan to change
    """
    mismatched = []
    counted = Counter(lines)
    for line in lines:
        # Message index, filename, word to replace
        id = line.split(",")[0]
        file = line.split(",")[1]
        word = line.split(",")[2]

        messages = mm.get_messages(file)
        text = "\n".join(messages[id].text)

        reg = get_regex(word)
        matches = [m.start() for m in re.finditer(reg, text.lower())]

        if len(matches) != counted[line]:
            mismatched.append(line)
    return mismatched


def write_indexed(filename) -> None:
    """
    Adds indexes to lines that match count of words to count of words that need to be changed
    """
    lines = fh.get_lines(filename)
    lookover = generate_mismatched(lines)
    new_lines = [x+",0" if x not in lookover else x for x in lines]

    with open("text/indexed.txt", "w") as f:
        f.write("\n".join(new_lines))


def check_indexed(filename) -> None:
    """
    Allows for a manually scan of lines without an index in filename
    """
    with open(filename) as f:
        lines = f.read().split("\n")
    lookover = [x for x in lines if len(x.split(",")) < 4] # Everything that doesn't have an index
    
    for line in lookover:
        if len(line) > 0:
            i = int(line.split(",")[0])
            file = line.split(",")[1]
            word = line.split(",")[2]

            messages = mm.get_messages(file)

            print("\n\n",word)
            print(file)
            mm.print_message(messages, i)
            inp = input("Index? ")

            with open(filename, "r+") as f:
                lines = f.read().split("\n")
                index = lines.index(line)
                lines[index] = f"{i},{file},{word},{inp}"
                f.seek(0)
                f.truncate()
                f.write("\n".join(lines))

def check_leftover() -> None:
    lines = fh.get_lines("text/indexed.txt")

    count = 0
    leftover_count = len([line for line in lines if (len(line.split(",")) != 5 and word in leftover)])
    for line in lines:
        word = line.split(",")[2]
        if word in leftover and len(line.split(",")) != 5:
            leftover_count += 1

    for line in lines:
        if len(line) > 0:
            split_line = line.split(",")
            i = split_line[0]
            file = split_line[1]
            word = split_line[2]
            word_index = split_line[3]

            if word in leftover and len(split_line) != 5:
                count += 1
                messages = mm.get_messages("output\\"+file)

                print("\n\n" + file)
                print(word, str(count)+"/"+str(leftover_count))
                mm.print_message(messages, int(i))
                inp = input("Replacement? ")

                if inp == "":
                    replacement = "ruler"
                elif inp == "'":
                    replacement = "queen"
                elif inp == "\\":
                    replacement = "king"
                else:
                    replacement = inp
                with open("text/indexed.txt", "r+") as f:
                    lines = f.read().split("\n")
                    index = lines.index(line)
                    lines[index] = f"{i},{file},{word},{word_index},{replacement}"
                    f.seek(0)
                    f.truncate()
                    f.write("\n".join(lines))

def replace_word(string, word, replacement, index=0) -> str:
    reg = get_regex(word)
    if replacement != "<HERO_NAME>":
        case = []
        new_word = ""
        try:
            i = [m.start() for m in re.finditer(reg, string.lower())][index]
        except:
            return string
        for char in string[i:i + len(word)]:
            case.append(char.isupper())
        for j, char in enumerate(replacement):
            try:
                new_word += char.upper() if case[j] else char
            except IndexError:
                new_word += char.upper() if case[-1] else char
        return string[:i] + new_word + string[i + len(word):]
    try:
        i = [m.start() for m in re.finditer(reg, string.lower())][index]
        print(string[:i] + replacement + string[i + len(word):])
        print(string)
        print("\n\n")
        return string[:i] + replacement + string[i + len(word):]
    except Exception as e:
        print(e)
        return string

def manually_replace(words, log) -> None:
    with open("text/indexed.txt") as f:
        lines = f.read().split("\n")

    with open(log) as f:
        processed = f.read().split("\n")
        processed = [x for x in processed if len(x) > 0]
        processed_lines = [",".join(x.split(",")[:-1]) for x in processed]
    
    message_list = []
    for line in lines:
        if len(line) > 0:
            if line.split(",")[2] in words:
                message_list.append(line)

    for messagecount, line in enumerate(message_list):
        i = line.split(",")[0]
        file = line.split(",")[1]
        word = line.split(",")[2]
        index = line.split(",")[3]

        messages = mm.get_messages("output\\"+file)
        message = messages[int(i)]
        if line in processed_lines:
            message.text = replace_word("\n".join(message.text), line.split(",")[2], processed[processed_lines.index(line)].split(",")[-1]).split("\n")
        else:
            print(word)
            print(message.title)
            print("\n".join(messages[int(i)-2].text))
            print("\n".join(messages[int(i)-1].text))
            print("\n".join(message.text))
            print(messagecount, "/", len(message_list))
            new = input("Replace with? ")
            message.text = replace_word("\n".join(message.text), word, new).split("\n")

            with open(log, "a") as f:
                f.write(f"{i},{file},{word},{index},{new}\n")
        
        message.rebuild()
        messages[int(i)] = message
        mm.write_messages("output\\"+file, messages)

def replace_leftover(filename, neutral=False) -> None:
    lines = fh.get_lines(filename)
    
    for line in lines:
        if len(line.split(",")) == 5:
                id = line.split(",")[0]
                file = line.split(",")[1]
                word = line.split(",")[2]
                index = int(line.split(",")[3])
                replacement = line.split(",")[4]

                replace_word_in_message(file, id, word, replacement, index=index)

def generate_paths_file(rootdir, log=False) -> None:
    count = 0
    failed = 0
    paths = []

    for subdir, _, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(".msg"):
                count += 1
                if not check_rebuild(filepath):
                    failed += 1
                    print(filepath)
                else:
                    paths.append(filepath)

    if log:
        print("Checked",count,"files")
        print(failed,"files failed")

    with open("text/paths.txt", "w") as file:
        file.write("\n".join(paths))

def replace_helper(file, message, word, replacement, index=0) -> None:
    if os.path.isfile("output\\"+file):
        with open("output\\"+file) as f:
            lines = f.read().split("\n")
    messages = mm.get_messages(file)
    message = messages[message]
    text = "\n".join(message.text)

    reg = f"(?<=^|[^a-zA-Z']){word}(?=$|[^a-zA-Z'])"
    matches = [m.start() for m in re.finditer(reg, text)]

    start = matches[index]
    end = start + len(word)
    new_text = text[:start] + replacement + text[end:]
    message.text = new_text.split("\n")
    message.rebuild()

    mm.write_messages(file, messages)

def replace_message_format(filename) -> None:
    lines = fh.get_lines(filename)
    new_lines = []
    for line in lines:
        i = int(line.split(",")[0])
        file = line.split(",")[1]
        messages = mm.get_messages(file)
        id = list(messages.keys())[i]
        new_lines.append(f"{id}," + ",".join(line.split(",")[1:]))
    with open(filename, "w") as f:
        f.write("\n".join(new_lines))

def replace_easy(dictionary, indexed_file) -> None:
    reset_output("message", include_files=False)
    lines = fh.get_lines(indexed_file)
    
    for line in lines:
        id = line.split(",")[0]
        file = line.split(",")[1]
        word = line.split(",")[2]
        try:
            index = int(line.split(",")[3])
        except IndexError:
            print(line)
        
        if word in dictionary.keys():
            replace_word_in_message(file, id, word, dictionary[word], index=index)

def reset_output(folder, include_files=False) -> None:
    """
    Copies a folder into the output folder
    """
    copy_tree(folder, "output\\" + folder)
    if not include_files:
        skeleton_output(folder)

def skeleton_output(folder) -> None:
    """
    Deletes all the files in a folder, but preserves the folder structure
    """
    for roots, dirs, files in os.walk("output\\" + folder):
        for file in files:
            os.remove(os.path.join(roots, file))

def check_rebuild(filename, log=False) -> bool:
    """
    Checks if a file can be rebuilt by message objects
    """
    try:
        messages = mm.get_messages(filename)
    except:
        return False
    
    for message in messages.values():
        message.rebuild()
        if message.original != message.built +"\n" and message.original != message.built:
            if log:
                print(message.original)
                print(message.built)
                print(filename)
            return False
    return True


def mass_check_rebuild(filename, log=False) -> bool:
    """
    Provided with a file with filepaths on each line, checks if every file can be rebuilt
    """
    lines = fh.get_lines(filename)

    for line in lines:
        if not check_rebuild(line, log=log):
            return False
    if log:
        print("All files can be rebuilt")
    return True

def find_all_occurrences(text : str, filelist: str):
    lines = fh.get_lines(filelist)
    for line in lines:
        messages = fh.get_messages(line)
        for message in messages.values():
            content : str = '\n'.join(message.text)
            reg : str = get_regex(text)
            matches = [m.start() for m in re.finditer(reg, content.lower())]
            if len(matches) > 0:
                print(line)
                print(content)

if __name__ == "__main__":
    # check_leftover()
    # replace_easy(MALE_FEMALE, "text\\indexed.txt")
    # replace_leftover(filename="text\\indexed-king.txt", neutral=False)
    # cleanup()
    # write_indexed("text\\gendered_messages.txt")
    # manually_replace(NEUTRAL_MANUAL, log="text\\manual_neutral.log")
    # reset_output()
    # generate_paths_file("message", True)
    find_all_occurrences("sword", "text/output_paths.txt")
    # write_word_counts("text/paths.txt")
    # write_unique_words("text/paths.txt")
    # print(count_all_occurrences("princesss", "text/paths.txt"))
    # mass_check_rebuild(filename="text\\paths.txt", log=True)
    # print(get_messages("message\\AccessPointName.msg"))
    # replace_message_format("text\\backups\\indexed-king-backup.txt")
    ...