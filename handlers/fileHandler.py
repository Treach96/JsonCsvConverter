from handlers import csvHandler
from handlers import jsonHandler


class fileHandler:

    def __init__(self):
        pass


READ_MODUS = "r"
READ_AND_WRITE_MODUS = "r+"
WRITE_AND_READ_MODUS = "w+"


def openFile(filePath):
    modus = askForModus()
    handlerSwitch(filePath, modus)


def askForModus():
    valid = False
    while not valid:
        try:
            userIn = int(input("What do you want to do with the file?\n"
                               "Use the number to select your choice:\n"
                               "1. read -- only shows content of file\n"
                               "2. read and write -- alter values or add new content\n"
                               "3. write and read -- clear file and add new content\n"
                               "4. exit\n"
                               "> "))
            if 4 >= userIn >= 1:
                valid = True
        except ValueError:
            print("Please select a number.")
    return modeSwitch(userIn)


def modeSwitch(userIn):
    match userIn:
        case 1:
            return READ_MODUS
        case 2:
            return READ_AND_WRITE_MODUS
        case 3:
            return WRITE_AND_READ_MODUS
        case 4:
            exit()


def checkForFileType(filepath):
    filesplit = filepath.split(".")
    return filesplit[1]


def handlerSwitch(filePath, modus):
    filetype = checkForFileType(filePath)
    match filetype:
        case "json":
            jsonHandler.useFile(filePath, modus)
        case "csv":
            csvHandler.useFile(filePath, modus)
