from handlers import fileHandler
from handlers.saveHelper import saveHelper


class jsonHandler:
    def __init__(self):
        pass


saver = saveHelper()


def useFile(filePath: str, modus: str):
    modusHandler(filePath, modus)


def modusHandler(filePath: str, modus: str):
    match modus:
        case "r":
            print("Read Mode activated")
            # fertig
            read(filePath, modus)
        case "r+":
            print("File can be modified")
            readAndWrite(filePath, modus)
        case "w+":
            # fertig
            print("File will be cleared and overwritten")
            choice: str = input(f"Are you sure about this operation?\n"
                                f"File content will be deleted for good!\n"
                                f"yes or no?\n> ")
            match choice:
                case "yes":
                    writeAndRead(filePath, modus)
                case "no":
                    fileHandler.openFile(filePath)


def readAndWrite(filePath: str, modus: str):
    valid = False
    while not valid:
        choice: str = askUserForChoice()
        file = open(filePath, modus)
        content: str = file.read()
        formattedContent: str = adjustFormat(content)
        dataArr: [] = createDataArray(formattedContent)
        match choice:
            case "change":
                print("change selected")
                printArrWithLineNumbers(dataArr)
                number = askForLineNumber(dataArr)
                lineFromArr: str = dataArr[number]
                lineDict: dict = convertLineToDict(lineFromArr)
                dataArr[number] = updateLineAndInsert(lineDict)
                printArrWithLineNumbers(dataArr)
                saveDict: {} = convertJArrToDict(dataArr)
                saver.askForFormatAndSave(saveDict, filePath)
                # saveArrayToFile(dataArr, filePath)
                file.close()
            case "append":
                print("append selected")
                file = open(filePath, 'a')
                lineDict = convertLineToDict(dataArr[0])
                listOfKeys = lineDict.keys()
                print("\nAvailable keys are: [", ', '.join(listOfKeys), "]\n")
                contentToAdd: str = input(
                    f"For json Format use \"{{\"key\":\"value\"}}\""
                    f"\nEnter content of next line\n> ")
                file.write(f", {contentToAdd}")
                file.close()


def read(filePath: str, modus):
    file = open(filePath, modus)
    content = file.read()
    formattedContent: str = adjustFormat(content)
    dataArr: [] = createDataArray(formattedContent)
    printArrWithLineNumbers(dataArr)


def adjustFormat(content: str):
    return content.replace("\n", "").replace("[", "").replace("]", "").replace(
        " ", "").replace("\\", "")


def createDataArray(content: str):
    dataArr: [] = content.split('},')
    dataLen: int = len(dataArr) - 1
    dataArrComplete: [] = []
    for index, item in enumerate(dataArr):
        if index < dataLen:
            dataArrComplete.append(item + '}')
        else:
            dataArrComplete.append(item)
    return dataArrComplete


def printArrWithLineNumbers(arr: []):
    print("Content of array gets printed:")
    for index, item in enumerate(arr):
        print(f"{index}. {item}")


def askUserForChoice():
    userInput = input(
        "\nWhat do you want to do with the file? Select number to choose:\n"
        "1. change value of key\n"
        "2. append new entry\n"
        "3. exit\n"
        "> ")
    match userInput:
        case "1" | "change":
            return "change"
        case "2" | "append":
            return "append"
        case "3" | "exit":
            exit()
        case _:
            print("Invalid choice")
            return askUserForChoice()


def askForLineNumber(dataArr: []):
    inputUser = input("Which line do you want to change?\nInsert number"
                      "> ")
    arrLength = len(dataArr)
    valid = False
    while not valid:
        if not inputUser.strip():
            print("Input cannot be empty")
        elif inputUser == "exit":
            exit()
        else:
            try:
                number = int(inputUser)
                if 0 <= number < arrLength:
                    print(f"\n Selected line is: {number}")
                    valid = True
                    continue
                else:
                    print("\n Selected number was not valid\n")
            except ValueError:
                print("Please enter a valid number.")
        inputUser = input("Which line do you want to change?\n"
                          "Insert number\n"
                          "> ")
    return number


def convertLineToDict(line: str):
    newDict: {} = {}
    tempStr: str = line.strip('{}')
    tempArr: [str] = tempStr.split(',')

    for item in tempArr:
        key, value = item.split(':')
        key = key.strip('"')
        if isCastableToInt(value):
            value = value.strip("'")
        else:
            value = value.strip('"')
        newDict[key]: dict = value
    return newDict


def convertJArrToDict(dataArr: []):
    dictArr: [dict] = []
    print("convert", dataArr)
    tempArr = []
    for item in dataArr:
        newDict: {} = {}
        tempStr = item.strip('{}')
        tempArr = tempStr.split(',')
        for keyPair in tempArr:
            key, value = keyPair.split(':')
            key = key.strip('"')
            key = key.strip("'")
            if isCastableToInt(value):
                value = value.strip("'")
            else:
                value = value.strip('"')
            newDict[key] = value
        dictArr.append(newDict)
        print("ditarr in prog", dictArr)
        # Problem: Keys werden nur einmal eingefügt und values ausgetauscht = 1 multipler STring
        # idee: mit .join arbeiten um ['{"key":"value"}] zu generieren!
    print("dictArrConvertJarr: ", dictArr)
    return dictArr


def isCastableToInt(value: str):
    try:
        int(value)
        return True
    except ValueError:
        return False


def updateLineAndInsert(jsonDict: dict):
    # askForKeyAndUpdate
    key = askForKey(jsonDict)
    if key == "id":
        valid = False
        while not valid:
            updatedValue = input("Please enter integer\n> ")
            if not updatedValue.strip():
                print("Input cannot be empty")
            else:
                try:
                    valid = isCastableToInt(updatedValue)
                except ValueError:
                    print("Input needs to be an integer")
        jsonDict[key] = updatedValue
    else:
        updatedValue = input("Please enter new Value\n> ")
        jsonDict[key] = updatedValue
    dataArr: [] = convertDictToJArr(jsonDict)
    updatedString = "{" + ",".join(dataArr) + "}"
    return updatedString


def askForKey(jsonDict: dict):
    listOfKeys = list(jsonDict.keys())
    print("\nAvailable keys are: [", ', '.join(listOfKeys), "]\n")
    valid = False
    while not valid:
        choice = input("From which key would you like adjust the value?\n"
                       "> ")
        if choice in jsonDict.keys():
            return choice


def convertDictToJArr(jsonDict: dict):
    dataArr: [] = []
    for key, value in jsonDict.items():
        if isCastableToInt(value):
            dataArr.append(f'"{key}":{value}')
        else:
            dataArr.append(f'"{key}":"{value}"')

    return dataArr


def writeAndRead(filePath: str, modus: str):
    file = open(filePath, modus)
    content: str = input(
        f"Enter new content. Content will overwrite current file.\n"
        f"For json Format use \"{{\"key\":\"value\"}}\"\n> ")
    file.write(f"{content}")
    file.close()
