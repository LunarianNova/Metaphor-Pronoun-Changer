import regex as re

def get_regex(word) -> str:
    """
    Generate regex to match a word, and ignore punctuation
    """
    return f"(?<=^|[^a-zA-Z'_]){word}(?=$|[^a-zA-Z'_])"

class Message:
    __slots__ = ['__original', '__id', '__lines', '__text', '__speaker', '__built']

    def __init__(self, message : str) -> None:
        self.__original : str  = message
        self.__id       : str  = None
        self.__lines    : list = []
        self.__text     : str  = None
        self.__speaker  : str  = None
        self.__built    : str  = message
        self.__parse_text()

    def __parse_text(self) -> None:
        """
        Parses the message into all of the attributes
        """
        message = self.__original
        for line in message.split("\n"):
            if line.startswith("#SPEAKER_ID"):
                self.__speaker = line
            elif line.startswith("@"):
                self.__id = line if self.__id is None else self.__id
            self.__lines.append(line)
        text : str = message.split("{")[1]
        text = '\n'.join(text.split("\n")[1:-1])
        self.__text = text

    def __replace_word(self, word: str, replacement: str, index: int) -> None:
        """
        The actual replace function :)
        """
        reg = get_regex(word)
        # <HERO_NAME> is a variable and must stay capital
        if replacement != "<HERO_NAME>":
            word_case : list = []
            new_word : str = ""

            # Attempt to locate word to replace
            try:
                start_index : int = [m.start() for m in re.finditer(reg, self.__text.lower())][index]
            except IndexError:
                print("Ocurrence " + str(index) + " of " + word + "not found!")
                return

            # Get the case of each character in the word
            for char in self.__text[start_index:start_index + len(word)]:
                word_case.append(char.isupper())
            for j, char in enumerate(replacement):
                if j < len(word_case) - 1:
                    new_word += char.upper() if word_case[j] else char
                # If replacement word is longer, assume the case is the same as the last character
                else:
                    new_word += char.upper() if word_case[-1] else char

            # Update the text to have the new word
            self.__text = self.__text[:start_index] + new_word + self.__text[start_index + len(word):]

    def replace_word(self, word: str, replacement: str, index: int = -1) -> None:
        """
        Replaces an occurrence of a word in the message
        use index = -1 to replace all occurrences
        """
        if index == -1:
            reg = get_regex(word)
            count = len([m.start() for m in re.finditer(reg, self.__text.lower())])
            for i in range(count):
                self.__replace_word(word, replacement, i)
        else:
            self.__replace_word(word, replacement, index)

    def get_lines(self) -> list:
        """
        Returns a list of all lines in a message
        """
        return self.__lines

    def get_original(self) -> str:
        """
        Returns the original message content
        """
        return self.__original
    
    def get_id(self) -> str:
        """
        Returns the message ID
        """
        return self.__id

    def get_text(self) -> str:
        """
        Returns the text content (That a player would see)
        """
        return self.__text
    
    def get_speaker(self) -> str:
        """
        Returns a string of who is saying the message
        """
        return self.__speaker
    
    def get_built(self) -> str:
        """
        Returns a full message, ready to be added to a file
        """
        return self.__built

class MessageFile:
    __slots__ = ['__lines', '__messages', '__path']

    def __init__(self, filepath : str) -> None:
        self.__lines    : list               = None
        self.__messages : dict[str, Message] = {}
        self.__path     : str                = filepath
        self.__add_messages()

    def __add_messages(self) -> None:
        with open(self.__path) as file:
            lines : list = file.read().split("\n")
            self.__lines = lines
            lines = [x for x in lines if x != ""]
        if "//--------------------------" in lines:
            # Remove any leading lines
            lines = lines[lines.index("//--------------------------"):]
            # Split file into the messages
            messages : list = "\n".join(lines).split("//--------------------------")[1:]

            # Create message objects
            for raw_message in messages:
                obj : Message = Message("//--------------------------" + raw_message)
                self.__messages[obj.get_id()] = obj
        
        else:
            print(self.__path + " cannot be converted into messages!")

    def __compile_file(self) -> str:
        """
        Returns a raw text file with all messages
        """
        content : str = ""
        if self.__lines[0] != "//--------------------------":
            for i in range(self.__lines.index("//--------------------------")):
                content += self.__lines[i] + "\n"
        for message in self.__messages.values():
            content += message.get_built()
        return content

    def __compile_modified_file(self) -> str:
        """
        Returns a raw text file with only messages that were changed
        """
        content : str = ""
        for message in self.__messages.values():
            if message.get_original() != message.get_text():
                content += message.get_built()
        return content
    
    def overwrite_file(self) -> None:
        """
        Overwrites every message back into the original file
        (DANGEROUS, it is recommended to use save_file)
        """
        compiled = self.__compile_file()
        with open(self.__path, "w") as f:
            f.write(compiled)

    def overwrite_modified_file(self) -> None:
        """
        Overwrites the original file with only modified messages
        (DANGEROUS, it is recommended to use save_modified_file)
        """
        compiled = self.__compile_modified_file()
        with open(self.__path, "w") as f:
            f.write(compiled)

    def save_file(self, path: str) -> None:
        """
        Saves every message into a file at path
        """
        compiled = self.__compile_file()
        with open(path, "w") as f:
            f.write(compiled)

    def save_modified_file(self, path: str) -> None:
        """
        Saves only modified files into a file at path
        """
        compiled = self.__compile_modified_file()
        with open(path, "w") as f:
            f.write(compiled)

    def get_path(self) -> str:
        """
        Returns a string representation of the path of the message file
        """
        return self.__path

    def get_messages(self) -> dict[str, Message]:
        """
        Returns a dict of messages, with the message ID as a key, and the message object as a value
        """
        return self.__messages

if __name__ == "__main__":
    with open("output\\message\\battle\\event\\BE_0601.msg") as f:
        messages = MessageFile("output\\message\\battle\\event\\BE_0601.msg")
        assert messages.compile_file() == f.read()