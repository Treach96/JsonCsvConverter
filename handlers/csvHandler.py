from handlers import fileHandler
from typing import List


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
            print("File will be cleared and overwritten")
            choice: str = input(f"Are you sure about this operation?\n"
                                f"File content will be deleted for good!\n"
                                f"yes or no?\n> ")
            match choice:
                case "yes":
                    pass

                    # writeAndRead(filePath, modus)
                case "no":
                    fileHandler.openFile(filePath)


def read(filePath: str, modus):
    file = open(filePath, modus)
    content = file.read()
    dataArr: [] = createDataArray(content)
    printArrWithLineNumbers(dataArr)


def createDataArray(content: str):
    dataArray: [] = content.splitlines()
    return dataArray


def printArrWithLineNumbers(dataArray: []):
    print("Content of array gets printed:")
    for index, item in enumerate(dataArray):
        if index == 0:
            print(f"{item}")
        else:
            print(f"{index}. {item}")


def readAndWrite(filePath: str, modus: str):
    valid = False
    while not valid:
        choice: str = askUserForChoice()
        match choice:
            case "change":
                print("change selected")
                file = open(filePath, modus)
                content: str = file.read()
                dataArr: [] = createDataArray(content)
                printArrWithLineNumbers(dataArr)
                number = askForLineNumber(dataArr)
                lineFromArr: str = dataArr[number]
                lineDict: dict = convertLineToDict(lineFromArr, dataArr)
                dataArr[number] = updateLineAndInsert(lineDict)
                printArrWithLineNumbers(dataArr)
                saveDict: [dict] = csvArrayToDict(dataArr)
                test1: [] = convertDictToCsvArray(saveDict)
                transformToCsvAndSave(dataArr, filePath)
                file.close()
            case "append":
                print("append selected")
                file = open(filePath, modus)
                content = file.read()
                dataArr: [] = createDataArray(content)
                contentToAdd: str = input(
                    f"Header of Csv:\n {dataArr[0]}\nEnter your content:\n> ")

                file.write(f"\n{contentToAdd.replace(" ", "")}")
                file.close()
            case "exit":
                fileHandler.openFile(filePath)


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
            return "exit"


def askForLineNumber(dataArr: []):
    inputUser = input("Which line do you want to change?\nInsert number"
                      "> ")
    arrLength = len(dataArr)
    valid = False

    while not valid:
        if not inputUser.strip():
            print("Input cannot be empty")
        else:
            try:
                number = int(inputUser)
                if 1 <= number < arrLength:
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


def convertLineToDict(lineToAdjust, dataArr: []):
    csvDict = {}
    keys: str = dataArr[0]
    keys: List[str] = keys.split(",")
    items = lineToAdjust.split(',')
    for index, item in enumerate(items):
        value = item
        key = keys[index]
        csvDict[key] = value
    return csvDict


def updateLineAndInsert(csvDict: dict):
    # askForKeyAndUpdate
    key = askForKey(csvDict)
    updatedValue = input("Please enter new Value\n> ")
    csvDict[key] = updatedValue
    # convertBackToString
    dataArr: [] = convertValuesToArr(csvDict)

    updatedString = ",".join(dataArr)
    return updatedString


def askForKey(csvDict: dict):
    listOfKeys = list(csvDict.keys())
    print("\nAvailable keys are: [", ', '.join(listOfKeys), "]\n")
    valid = False
    while not valid:
        choice = input("From which key would you like adjust the value?\n"
                       "> ")
        if choice in csvDict.keys():
            return choice


def convertValuesToArr(csvDict: dict):
    # Add data rows
    dataArr: [] = []
    for item in csvDict.values():
        dataArr.append(f'{item}')

    return dataArr


def isCastableToInt(value: str):
    try:
        int(value)
        return True
    except ValueError:
        return False


def transformToCsvAndSave(dataArr: [str], filePath: str):
    print("saving process starting")
    file = open(filePath, 'w')
    headers: str = dataArr[0]
    file.write(headers + "\n")

    for index, item in enumerate(dataArr[1:]):
        file.write(item + "\n")
    file.close()
    print("saving proces completed")


def csvArrayToDict(dataArr: []):
    headers: [] = dataArr[0].split(',')

    dictArray: [] = []
    for row in dataArr[1:]:
        values: [] = row.split(',')
        rowDict: [] = {headers[i]: values[i] for i in range(len(headers))}
        dictArray.append(rowDict)
    return dictArray

def convertDictToCsvArray(csvDict: [dict]):
    dataArr: [] = []
    # 1x keys filtern und als header setzen
    # todo: convert dict to csv array
    for item in csvDict[0].keys():
        dataArr.append(f'{item}')
        # convertValuesToArray returns values of single dictonary
    for itemDict in csvDict:
       pass
    print("converted:\n", dataArr)
    return dataArr


class csvHandler:
    def __init__(self):
        pass
