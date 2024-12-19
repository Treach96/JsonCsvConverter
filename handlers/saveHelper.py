
class saveHelper:
    def __init__(self):
        pass

    """
    This class handles all the saving operations.
    This includes the Array <-> Dict transformation.
    """

    def askForFormatAndSave(self, saveDict: [dict], filePath):
        print("askForFormatDicT: ", saveDict)
        choice: str = input("In which format do you wan to save?\n json or csv\n> ")
        match choice:
            case "csv":
                csvArr: [str] = self.convertDictToCsvArray(saveDict)
                self.transformToCsvAndSave(csvArr, filePath)
            case "json":
                self.saveArrayToFile(saveDict, filePath)
                # {"id":390,"first_name":"Rahel","last_name":"McLae","gender":"Female","street_name":"OldShore"}
                pass

    def saveArrayToFile(self, dataArr, filePath):
        print("saving process starting")
        if filePath.endswith('.csv'):
            filePath = filePath.replace('.csv', '_fromCsv.json')
        file = open(filePath, 'w')
        dataLen = len(dataArr) - 1

        for index, item in enumerate(dataArr):
            if index < dataLen:
                file.write(f"{item},")
            else:
                file.write(f"{item}")
        print("save completed.")

    def convertDictToCsvArray(self, csvDict: [dict]):
        dataArr: [] = []
        print(csvDict[0])
        # todo: aray doch nicht als dict konvertiert orden?

        headers = ','.join(csvDict[0].keys())
        dataArr.append(headers)
        for itemDict in csvDict:
            row = ','.join(itemDict.values())
            dataArr.append(row)
        return dataArr


    def transformToCsvAndSave(self, dataArr: [str], filePath: str):
        print("saving process starting")
        if filePath.endswith('.json'):
            filePath.replace('.json', '_fromJson.csv')
        file = open(filePath, 'w')
        headers: str = dataArr[0]
        file.write(headers + "\n")

        for index, item in enumerate(dataArr[1:]):
            file.write(item + "\n")
        file.close()
        print("saving proces completed")
