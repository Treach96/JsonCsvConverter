from tkinter import Tk
from tkinter.filedialog import askopenfilename

from handlers import fileHandler


# retrieve filePath and parse it to the fileHandler
def getFileFrom():
    Tk().withdraw()
    filePath = askopenfilename(filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")])
    return filePath


def parseFileToProcess(filePath):
    fileHandler.openFile(filePath)


def main():
    filePath = getFileFrom()
    parseFileToProcess(filePath)


if __name__ == "__main__":
    main()
