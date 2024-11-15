import re

class Message:
    def __init__(self, message):
        self.original = message
        self.speaker_id = None
        self.id = None
        self.text = None
        self.built = None
        self.parse_text(message)

    def parse_text(self, message):
        for line in message.split("\n"):
            if line.startswith("#SPEAKER_ID"):
                self.speaker_id = line
            elif line.startswith("@"):
                self.id = line if self.id is None else self.id
        self.text = [line for line in message.split("{")[1].split("\n")[1:-1]]

    def rebuild(self):
        self.built = "//--------------------------\n"
        self.built += self.speaker_id +"\n" if self.speaker_id else ""
        self.built += self.id + "\n" if self.id else ""
        self.built += "{\n"
        for line in self.text:
            self.built += line + "\n"
        self.built += "}"

        tokens = self.built.split("\n")
        if tokens[-1] == "}" and tokens[-2] == "}":
            tokens = tokens[:-1]
            self.built = "\n".join(tokens)

def get_messages(filename) -> dict[str, Message]:
    """
    Takes a filename as an input
    The file should be a file from Metaphor, that contains messages
    It then returns a list of those messages, as objects
    """
    message_objects = {}
    try:
        with open(filename) as file:
            lines = file.read().split("\n")
            lines = [x for x in lines if x != ""]
    except FileNotFoundError:
        lines = []

    try:
        lines = lines[lines.index("//--------------------------"):]
        # Split file into the messages
        messages = "\n".join(lines).split("//--------------------------")[1:]

        # Create message objects
        for raw_message in messages:
            obj = Message("//--------------------------" + raw_message)
            obj.rebuild()
            message_objects[obj.id] = obj

    except ValueError:
        pass    

    return message_objects

def print_message(messages, id) -> None:
    """
    Helper to print message info
    """
    index = messages.index(id)
    for i in range(index-2, index+1):
        message = list(messages.keys())[i]
        title = message.title
        text = "\n".join(message.text)
        if title:
            print(title + " - " + text)
        else:
            print(text)   