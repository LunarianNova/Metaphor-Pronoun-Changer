import sys
from GetMessages import metaphorMessages

# gendered = ["boy", "mr", "im"]
# check king's rock "more qualified they are to be king"
# Double check king (after changes)
# gendered = ['actor', "actors'", "boy'd", "boy's", 'boyfriend', 'boyhood', 'boyish', 'boyo', 'boys', 'businessman', 'con-men', 'conman', 'craftsman', 'craftsmen', 'dad', "dad's", 'father', "father's", 'fatherly', 'fiance', 'fisherman', 'fishermen', 'fishermencolor', 'footmen', 'gent', 'gentleman', "gentleman's", 'gentlemen', 'god', "god's", 'gods', "gods'", 'guardsman', 'guardsmancolor', 'guardsmen', 'guy', "guy's", 'guycolor', 'guys', 'he', "he'd", "he'drrrrghhh", "he'll", "he's", "he'scolor", "hei've", 'heir', 'heirs', 'henchman', 'him', "him's", 'himan', 'himcolor', "himdidn't", 'himhe', "himhe's", 'himself', 'himselfthe', 'his', 'host', 'hosts', "hosts'", 'husband', "husband's", 'husbands', 'igodi', "ihe'di", "ihe'lli", "ihe'si", 'ihei', 'ihimi', 'ihis', 'ihisi', "iprince'si", 'iprincei', 'iprincelyi', 'king', "king'll", "king's", 'king-defying', 'king-ish', 'king-picking', 'king-slaying', 'king-to-be', 'kinga', 'kingcolor', 'kingif', 'kingless', 'kingliness', 'kingly', 'kinglycolor', 'kings', "kings'", 'kingscolor', 'kingslayer', 'kingslaying', 'lad', "lad's", 'laddie', 'laddies', 'lads', 'lord', "lord's", 'lordling', 'lordlings', 'lordly', 'lords', 'lordship', "m'boy", "m'lad", "m'lord", 'madlad', 'madlads', 'madman', "madman's", 'man', "man's", 'manhunter', "manwe'll", 'masculine', 'mate', 'matecolor', 'matefor', 'mates', 'men', "men's", 'mistah', 'mister', "mister'll", 'misters', 'nobleman', "nobleman's", "nolipsynche's", "ofhe's", "onehe's", 'p-papa', 'p-prince', 'papa', "papa's", 'paralysedhe', 'prince', "prince's", 'prince-impersonating', 'prince-infused', 'princecolor', 'princeeven', 'princeliness', 'princelinessi', 'princely', 'princey', 'pro-prince', "recentlyhe's", 'runnerhe', "saviourhe's", 'sir', 'sircolor', 'sire', 'sired', 'sirs', 'son', "son's", 'sons', 'wizard', 'wizardcolor']

def find_all(word, found = None):
    if found is None:
        found = []
    try:
        with open("paths.txt") as f:
            lines = f.read().split("\n")
            if len(found) > 0:
                print(lines.index(found[-1][1]))
                print(len(lines))
                lines = lines[lines.index(found[-1][1]):]
            for file in lines:
                stripped, messages = get_messages(file)
                if len(found) > 0:
                    if file == found[-1][1]:
                        messages = messages[int(found[-1][0])+1:]
                for i, message in enumerate(messages):
                    count = len(found)
                    for line in message.text:
                        for word in line.split():
                            word = word.strip().lower()
                            new_word = ""
                            if "_" in word:
                                word = ""
                            for char in word:
                                if char in "abcdefghijklmnopqrstuvwxyz-'":
                                    new_word += char
                            word = new_word
                            if word in gendered:
                                # print(f"\n\n\n\n{str(i)} {word}\n{file}\n\n")
                                # print("\n".join(messages[i-4].text)+"\n")
                                # print("\n".join(messages[i-3].text)+"\n")
                                # print("\n".join(messages[i-2].text)+"\n")
                                # print("\n".join(messages[i-1].text)+"\n")
                                # print("\n".join(message.text) + "\n")
                                # inp = input("Is this what you are looking for?")
                                # if inp == "":
                                #     pass
                                # elif inp == "q":
                                #     return found
                                # else:
                                found.append([str(i), file, word])
                                count = len(found)
        print(count)
        return found
    except KeyboardInterrupt:
        return found

def cherry_pick(found):
    try:
        newfound = []
        for x, occurance in enumerate(found[258:]):
            i = occurance[0]
            file = occurance[1]
            word = occurance[2]
            if word == "god" or word == "gods" or word == "mate" or word == "god's" or word == "gods'" or word == "mates":
                print("Skipped " + word)
                continue
            stripped, messages = get_messages(file)
            try:
                print("\n\n", word, x, "\n")
                print(messages[int(i)-3].title + " - " + "\n".join(messages[int(i)-3].text) + "\n" if messages[int(i)-3].title else "\n".join(messages[int(i)-3].text) + "\n")
                print(messages[int(i)-2].title + " - " + "\n".join(messages[int(i)-2].text) + "\n" if messages[int(i)-2].title else "\n".join(messages[int(i)-2].text) + "\n")
                print(messages[int(i)-1].title + " - " + "\n".join(messages[int(i)-1].text) + "\n" if messages[int(i)-1].title else "\n".join(messages[int(i)-1].text) + "\n")
                print(messages[int(i)].title + " - " + "\n".join(messages[int(i)].text) if messages[int(i)].title else "\n".join(messages[int(i)].text))
            except:
                try:
                    print("\n\n", word, x, "\n")
                    print(messages[int(i)-1].title + " - " + "\n".join(messages[int(i)-1].text) + "\n" if messages[int(i)-1].title else "\n".join(messages[int(i)-1].text) + "\n")
                    print(messages[int(i)].title + " - " + "\n".join(messages[int(i)].text) if messages[int(i)].title else "\n".join(messages[int(i)].text))
                except:
                    print("\n\n", word, x, "\n")
                    print(messages[int(i)].title + " - " + "\n".join(messages[int(i)].text) if messages[int(i)].title else "\n".join(messages[int(i)].text))
            inp = input("\nIs this for the Prince?")
            if inp == "":
                pass
            elif inp == "q":
                return newfound
            else:
                newfound.append([i, file, word])
        return newfound
    except KeyboardInterrupt:
        return newfound
    except Exception as e:
        print(e)
        return newfound

if __name__ == "__main__":
    ...
    # found = []
    # try:
    #     with open(f"picked {sys.argv[1]}.txt") as f:
    #         lines = f.read().split("\n")
    #         for line in lines[:-1]:
    #             i = line.split(",")[0]
    #             file = line.split(",")[1]
    #             word = line.split(",")[2]
    #             found.append([i, file, word])
    #         found = cherry_pick(found)
    #     with open(f"picked {sys.argv[1]}2.txt", "a") as f:
    #         for o in found:
    #             f.write(o[0] + "," + o[1] + "," + o[2] + "\n")
    # except Exception as e:
    #     print(e)
    #     found = find_all(sys.argv[1])
    #     with open(f"picked {sys.argv[1]}.txt", "w") as f:
    #         for o in found:
    #             f.write(o[0] + "," + o[1] + "," + o[2] + "\n")