from collections import Counter
from main import get_messages, write_messages
import re


found = {'prince': 696, 'king': 559, 'his': 527, 'he': 272, 'him': 188, 'lad': 155, 'boy': 152, "he's": 138, "prince's": 98, 'mister': 98, 'man': 64, "king's": 41, 'himself': 32, 'son': 22, "boy's": 18, 'kingly': 18, "he'd": 14, 'sir': 14, "he'll": 14, 'guy': 13, 'mistah': 11, 'heir': 10, 'kingcolor': 9, 'princecolor': 9, 'kings': 8, 'lord': 7, 'laddie': 7, 'mr': 7, "son's": 6, 'king-to-be': 4, 'sire': 4, 'ihimi': 3, "m'lord": 3, 'p-prince': 3, "king'll": 3, 'men': 3, 'boyo': 3, 'prince-infused': 3, 'ihei': 2, 'princey': 2, 'boys': 2, "lad's": 2, "ihe'si": 2, "man's": 2, 'princely': 2, 'guardsman': 1, "ofhe's": 1, 'gentlemen': 1, "lord's": 1, "ihe'di": 1, "boy'd": 1, 'runnerhe': 1, 'ihis': 1, 'princelinessi': 1, "hei've": 1, 'kinglycolor': 1, "iprince'si": 1, 'princeeven': 1, "m'boy": 1, 'boyfriend': 1, 'king-ish': 1, 'misters': 1, "mister'll": 1, 'sirs': 1, 'kingscolor': 1, 'pro-prince': 1, 'king-picking': 1, 'princeliness': 1, 'kingliness': 1, 'gentleman': 1, 'king26': 1, 'iprincei': 1, "himdidn't": 1, 'prince-impersonating': 1, 'his1': 1, 'iprincelyi': 1}


found_list = ['boy', "boy'd", "boy's", 'boyfriend', 'boyo', 'boys', 'gentleman', 'gentlemen', 'guardsman', 'guy', 'he', 
"he'd", "he'll", "he's", 'heir', 'him', 'himself', 'his', 'king', "king'll", "king's", 'king-ish', 'king-picking', 
'king-to-be', 'kingliness', 'kingly', 'kings', 'lad', "lad's", 'laddie', 'lord', "lord's", "m'boy", "m'lord", 'man', 
"man's", 'men', 'mistah', 'mister', "mister'll", 'misters', 'mr', 'p-prince', 'prince', "prince's", 
'prince-impersonating', 'prince-infused', 'princeliness', 'princely', 'princey', 'pro-prince', 'sir', 'sire', 'sirs', 
'son', "son's"] 

female_dict = {"boy": "girl", "boy'd": "girl'd", "boy's": "girl's", "boyfriend": "girlfriend", "boyo": "girly", 
               "gentleman": "lady", "guy": "girl", "he": "she", "he'd": "she'd", "he'll": "she'll", "he's": "she's",
               "heir": "heiress", "him": "her", "himself": "herself", "his": "her", "lad": "lass", "lad's": "lass's",
               "laddie": "lassie", "lord": "lady", "lord's": "lady's", "m'boy": "m'girl", "m'lord": "m'lady", 
               "man": "woman", "man's": "woman's", "mistah": "missus", "mister": "miss", "mister'll": "miss'll", 
               "mr": "ms", "p-prince": "p-princess", "prince": "princess", "prince's": "princess's", 
               "prince-impersonating": "princess-impersonating", "prince-infused": "princess-infused", 
               "princeliness": "princessliness", "princely": "princessly", "princey": "princessy", 
               "pro-prince": "pro-princess", "sir": "lady", "sire": "lady", "son": "daughter", "son's": "daughter's"}


# Manually set these :)
leftover = ["boys", "gentlemen", "king", "king'll", "king's", "king-ish", "king-picking", "king-to-be", "kingliness", 
            "kingly", "kings", "men", "misters", "sirs"]

with open("picked genderedww2.txt") as f:
    lines = f.read().split("\n")

counted = Counter(lines)
unique_files = []

for line in lines:
    try:
        if line.split(",")[1] not in unique_files:
            unique_files.append(line.split(",")[1])
    except:
        pass

per_file = {}
for file in unique_files:
    for line in lines:
        try:
            if line.split(",")[1] == file:
                per_file[file] = per_file.get(file, []) + [line]
        except:
            pass

success = []
dictionary = {}
for file in per_file.keys():
    stripped, messages = get_messages(file)
    for line in per_file[file]:
        i = line.split(",")[0]
        word = line.split(",")[2]

        text = "\n".join(messages[int(i)].text)
        text_lower = text.lower()

        matches = [m.start() for m in re.finditer(word, text_lower)]
        if len(matches) != counted[line]:
            pass
        else:
            try:
                new_word = female_dict[word]
                success.append(line)
                if len(matches) > 1:
                    print(matches)
                    print(text)
                    for match in matches:
                        print(text[match:match+len(word)])
                    print("\n\n")

                print(text.find(word))
                text.replace(word, new_word)
                print(text.find(word))
                for i, m in enumerate(matches):
                    m = m + (len(new_word) - len(word)) * i
                    if text[m].isupper():
                        if text[m+1].isupper():
                            text = (text[:m] + new_word.upper() + text[m+len(word):])
                        else:
                            text = (text[:m] + new_word.capitalize() + text[m+len(word):])
                    else:
                        print(m)
                        text = (text[:m] + new_word.lower() + text[m+len(word):])
                print(text, "\n\n")
                messages[int(i)].text = text.split("\n")
                messages[int(i)].rebuild()
            except KeyError:
                # if "king" in word:
                #     print("\n\n")
                #     print(word)
                #     print(messages[int(i)].title if messages[int(i)].title else "")
                #     print("\n".join(messages[int(i)-2].text))
                #     print("\n".join(messages[int(i)-1].text))
                #     print("\n".join(messages[int(i)].text))
                #     inp = input('Default to Ruler, or change to Queen? ')
                #     if inp == "q":
                #         break
                #     if inp == "":
                #         dictionary[line] = "ruler"
                #         print("ruler")
                #     elif inp == "'":
                #         dictionary[line] = "queen"
                #         print("queen")
                #     else:
                #         print("passed")
                #         pass
                pass
    #write_messages(file, stripped, messages)

# with open("ruler.txt", "a") as f:
#     for line in dictionary.keys():
#         f.write(line + "," + dictionary[line] + "\n")

# with open("picked genderedww2 copy 3.txt", "r+") as f:
#     try:
#         filelines = f.read().split("\n")
#         for line in success:
#             i = filelines.index(line)
#             filelines[i] = ""
#         f.seek(0)
#         f.write("\n".join(filelines))
#     except Exception as e:
#         print(e)

# count = 0
# for reference in counted.keys():
#     try:
#         i = reference.split(",")[0]
#         file = reference.split(",")[1]
#         word = reference.split(",")[2]
#         stripped, messages = get_messages(file)

#         text = "\n".join(messages[int(i)].text)
#         text_lower = text.lower()

#         matches = [m.start() for m in re.finditer(word, text_lower)]
#         if len(matches) != counted[reference]:
#             count += 1
#         if len(matches) == counted[reference]:
#             try:
#                 new_word = female_dict[word]
#                 print(text)
#                 print(new_word)
#                 for m in matches:
#                     m = m + (len(new_word) - len(word)) * matches.index(m)
#                     left = text[:m]
#                     right = text[m+len(word):]
#                     print(left, right)
#                     if text[m].isupper():
#                         if text[m+1].isupper():
#                             text = left + new_word.upper() + right
#                         else:
#                             text = left + new_word.capitalize() + right
#                     else:
#                         text = left + new_word.lower() + right
#                 print(reference, file, "\n", text, "\n\n")
#             except KeyError:
#                 pass


#     except IndexError:
#         print(reference, "ERROR")

# print(count)