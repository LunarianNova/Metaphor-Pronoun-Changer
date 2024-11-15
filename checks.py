from mfmessages import get_messages
from filehandler import get_lines

def check_rebuild(filename, log=False) -> bool:
    """
    Checks if a file can be rebuilt by message objects
    """
    try:
        messages = get_messages(filename)
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
    lines = get_lines(filename)

    for line in lines:
        if not check_rebuild(line, log=log):
            return False
    if log:
        print("All files can be rebuilt")
    return True
        