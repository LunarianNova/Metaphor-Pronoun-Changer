from mfmessages import get_messages
import re

def get_lines(filename) -> list[str]:
    """
    Get alls non-empty lines from a file
    """
    try:
        with open(filename) as file:
            lines = file.read().split("\n")
            lines = [x for x in lines if x != ""]
    except FileNotFoundError:
        lines = []
    return lines 

def count_all_occurrences(word, files) -> int:
    reg = f"(?<=^|[^a-zA-Z']){word}(?=$|[^a-zA-Z'])"
    count = 0

    with open(files) as f:
        lines = f.read().split("\n")

        for file in lines:
            try:
                messages = get_messages(file)
            except:
                continue

            for message in messages:
                count += len(re.findall(reg, "\n".join(message.text).lower()))

    return count

def find_all_occurrences(word, files) -> None:
    reg = f"(?<=^|[^a-zA-Z']){word}(?=$|[^a-zA-Z'])"

    with open(files) as f:
        lines = f.read().split("\n")

        for file in lines:
            try:
                messages = get_messages(file)
            except:
                continue

            for message in messages:
                if len(re.findall(reg, "\n".join(message.text).lower())) > 0:
                    print(file)
                    print(message.title) if message.title else ...
                    print("\n".join(message.text))
                    print("\n")

def generate_unique_words(files) -> list[str]:
    reg = r"[a-zA-Z|'|-]*"
    words = []

    with open(files) as f:
        lines = f.read().split("\n")
    
    for f in lines:
        messages = get_messages(f)

        for message in messages:
            text = "\n".join(message.text)
            for word in re.findall(reg, text.lower()):
                words.append(word)

    words = sorted(list(set(words)))
    return words

def write_unique_words(files) -> None:
    words = generate_unique_words(files)
    with open("text/words.txt", "w") as f:
        f.write("\n".join(words))

def generate_word_counts(files) -> dict[str, int]:
    reg = r"[a-zA-Z|'|-]*"
    words = {}

    with open(files) as f:
        lines = f.read().split("\n")
    
    for f in lines:
        messages = get_messages(f)

        for message in messages:
            text = "\n".join(message.text)
            for word in re.findall(reg, text.lower()):
                words[word] = words.get(word, 0) + 1

    return words

def write_word_counts(files) -> None:
    words = generate_word_counts(files)
    sorted_words = dict(sorted(words.items(), key=lambda x: x[1], reverse=True))
    with open("text/word_counts.txt", "w") as f:
        for word, count in sorted_words.items():
            f.write(f"{word},{count}\n")