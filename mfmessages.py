class Message:
    __slots__ = ['__original', '__id', '__lines', '__text', '__speaker']

    def __init__(self, message : str) -> None:
        self.__original : str  = message
        self.__id       : str  = None
        self.__lines    : list = []
        self.__text     : str  = None
        self.__speaker  : str  = None
        self.__parse_text()

    def __parse_text(self) -> None:
        message = self.__original
        for line in message.split("\n"):
            if line.startswith("#SPEAKER_ID"):
                self.__speaker = line
            elif line.startswith("@"):
                self.__id = line if self.__id is None else self.__id
            self.__lines.append(line)
        content : str = message.split("{")[1]
        content = '\n'.join(content.split("\n")[1:-1])
        self.__text = content

    def get_lines(self) -> list:
        return self.__lines

    def get_original(self) -> str:
        return self.__original
    
    def get_id(self) -> str:
        return self.__id

    def get_text(self) -> str:
        return self.__text
    
    def get_speaker(self) -> str:
        return self.__speaker

class MessageFile:
    __slots__ = ['__messages', '__path']

    def __init__(self, filepath : str) -> None:
        self.__messages : dict[str, Message] = {}
        self.__path     : str                = filepath
        self.__add_messages()

    def __add_messages(self) -> None:
        with open(self.__path) as file:
            lines : list = file.read().split("\n")
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

    def get_path(self) -> str:
        return self.__path

    def get_messages(self) -> dict[str, Message]:
        return self.__messages

if __name__ == "__main__":
    messages = MessageFile("output\\message\\battle\\event\\BE_0601.msg")