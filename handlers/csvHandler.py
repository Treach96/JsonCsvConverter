from handlers import fileHandler
from typing import List

from handlers.saveHelper import saveHelper


class csvHandler:
    def __init__(self):
        pass


saver = saveHelper()


def useFile(filePath: str, modus: str):
    modusHandler(filePath, modus)


def modusHandler(filePath: str, modus: str):
    match modus:
        case "r":
            print("Read Mode activated")
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
                    writeAndRead(filePath, modus)
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
                saver.askForFormatAndSave(saveDict, filePath)
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
                exit()


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
        case _:
            print("Choice not valid")
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
        csvDict[key] = updatedValue
    else:
        updatedValue = input("Please enter new Value\n> ")
        csvDict[key] = updatedValue

    # convertBackToString
    dataArr: [] = convertValuesToArr(csvDict)
    updatedString = ",".join(dataArr)
    return updatedString


def csvArrayToDict(csvDataArr: []):
    headers: [] = csvDataArr[0].split(',')
    dictArray: [dict] = []
    for row in csvDataArr[1:]:
        values: [] = row.split(',')
        rowDict: [] = {headers[i]: values[i] for i in range(len(headers))}
        dictArray.append(rowDict)
    return dictArray


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


def writeAndRead(filePath: str, modus: str):
    file = open(filePath, modus)
    content: str = input(
        f"Enter new content. Content will overwrite current file.\n")
    file.write(f"{content}")
    file.close()
