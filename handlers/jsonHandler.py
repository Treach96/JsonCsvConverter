from handlers import fileHandler


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
                    writeAndRead(filePath, modus)
                case "no":
                    fileHandler.openFile(filePath)


def readAndWrite(filePath: str, modus: str):
    valid = False
    while not valid:
        choice: str = askUserForChoice()
        match choice:
            case "change":
                print("change selected")
                file = open(filePath, modus)
                content: str = file.read()
                formattedContent: str = adjustFormat(content)
                dataArr: [] = createDataArray(formattedContent)
                printArrWithLineNumbers(dataArr)
                number = askForLineNumber(dataArr)
                lineFromArr: str = dataArr[number]
                lineDict: dict = convertLineToDict(lineFromArr)
                dataArr[number] = updateLineAndInsert(lineDict)
                printArrWithLineNumbers(dataArr)
                saveDataToFile(dataArr, filePath)
                file.close()
            case "append":
                print("append selected")
                file = open(filePath, 'a')
                contentToAdd: str = input(
                    f"For json Format use \"{{\"key\":\"value\"}}\"\n> ")
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
        key = key.strip("'")
        if isCastableToInt(value):
            value = value.strip("'")
        else:
            value = value.strip('"')
        newDict[key]: dict = value

    return newDict


def isCastableToInt(value: str):
    try:
        int(value)
        return True
    except ValueError:
        return False


def updateLineAndInsert(jsonDict: dict):
    # askForKeyAndUpdate
    key = askForKey(jsonDict)
    updatedValue = input("Please enter new Value\n> ")
    jsonDict[key] = updatedValue
    # convertBackToString
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


def saveDataToFile(dataArr: [], filePath: str):
    print("saving process starting")
    file = open(filePath, 'w')
    dataLen = len(dataArr) - 1

    for index, item in enumerate(dataArr):
        print(f"saved line {index}")
        if index < dataLen:
            file.write(f"{item},")
        else:
            file.write(f"{item}")


def writeAndRead(filePath: str, modus: str):
    file = open(filePath, modus)
    content: str = input(
        f"Enter new content. Content will overwrite current file.\n"
        f"For json Format use \"{{\"key\":\"value\"}}\"\n> ")
    file.write(f"{content}")
    file.close()


class csvHandler:
    def __init__(self):
        pass


"""
def json_to_csv(json_string):
    # Remove special characters and split the string into individual records
    json_string = json_string.replace('\n', '').replace('[', '').replace(']', '').replace(' ', '').replace('\\', '')
    records = json_string.split('},')
    records = [record + '}' if not record.endswith('}') else record for record in records]

    # Extract headers
    headers = set()
    for record in records:
        items = record.replace('{', '').replace('}', '').split(',')
        for item in items:
            key, _ = item.split(':')
            headers.add(key)
    headers = list(headers)

    # Create CSV string
    csv_string = ','.join(headers) + '\n'
    for record in records:
        items = record.replace('{', '').replace('}', '').split(',')
        row = {key: '' for key in headers}
        for item in items:
            key, value = item.split(':')
            row[key] = value
        csv_string += ','.join(row[key] for key in headers) + '\n'

    return csv_string

# Example usage
json_string = '''
[
    {"name": "John", "age": 30, "city": "New York"},
    {"name": "Anna", "age": 22, "city": "London"},
    {"name": "Mike", "age": 32, "city": "Chicago"}
]
'''
csv_string = json_to_csv(json_string)
print(csv_string)
"""
