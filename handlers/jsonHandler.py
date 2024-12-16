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

def readAndWrite(filePath: str, modus: str):
   choice: str = ""
   while choice != "exit":
       pass

def read(filePath: str, modus):
    file = open(filePath, modus)
    content = file.read()
    formattedContent: str = adjustFormat(content)
    dataArr: [] = createDataArray(formattedContent)
    printArrWithLineNumbers(dataArr)


def adjustFormat(content: str):
    # removes special chars if incoming json has bad format
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


class csvHandler:
    def __init__(self):
        pass
