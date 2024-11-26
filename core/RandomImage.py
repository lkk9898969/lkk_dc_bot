import json
import logging
import random

from core.image import image

random.seed()
FILE_EXTENSION = ['.jpg', '.gif']
CONTENT = "content"
ALLMATCH = "allMatch"
RELATEDWORD = "related"


class RandomNameJson():

    def __init__(self, logger: logging.Logger, ranfile: str):
        self.__logger = logger
        self.__ranjson: dict[str, dict[str, dict[str, bool | list[str]]]] = {}
        self.__notallMatchCache: dict[str, list[str]] = {}
        self.__ranfile = ranfile
        self.__importjson(self.__ranfile)

    def __importjson(self, ranfile: str):
        self.__logger.info(f"{__name__}類別開始初始化隨機圖庫。")
        try:
            self.__ranjson = json.load(open(ranfile, 'r', encoding='utf-8'))
        except FileNotFoundError:
            self.__logger.warning(f"初始化json失敗! 無法找到json檔案{ranfile} !")
            return
        except:
            self.__logger.error(f"發生未處理的例外。", exc_info=True)
            return
        self.__notallMatchCache = {
            randomName: v[RELATEDWORD]
            for extContent in self.__ranjson.values()
            for randomName, v in extContent.items() if v[ALLMATCH] is False
        }
        # self.__logger.debug(f"notallMatchCache: {self.__notallMatchCache}")

    def __exportjson(self, _file: str):
        json.dump(self.__ranjson,
                  open(_file, 'w', encoding='utf-8'),
                  ensure_ascii=False,
                  indent=4)
        self.__logger.info(f"{__name__}類別輸出json圖庫。")

    def refresh(self):
        self.__importjson(self.__ranfile)

    def saveJson(self):
        self.__exportjson(self.__ranfile)

    def checkRandomNamewithExtinJson(self, randomName: str, fileExt: str):
        return randomName in self.__ranjson[fileExt]

    def checkRandomNameinJson(self, randomName: str):
        for i in FILE_EXTENSION:
            if self.checkRandomNamewithExtinJson(randomName, i):
                return True
        return False

    def addRandomNametoJson(self,
                            randomName: str,
                            imageName: str,
                            fileExt: str,
                            allMatch: bool = None):
        '''
        將圖片名稱加入json圖庫中
        請注意:
         1. 請確保imageName已存在於圖片庫中
         2. randomName及imageName不應該包含副檔名(fileExt)
        '''
        if fileExt not in self.__ranjson:
            self.__ranjson[fileExt] = {}
        if randomName not in self.__ranjson[fileExt]:
            self.__ranjson[fileExt][randomName] = {}
            self.__ranjson[fileExt][randomName][ALLMATCH] = True
            self.__ranjson[fileExt][randomName][CONTENT] = []
            self.__ranjson[fileExt][randomName][RELATEDWORD] = []

        self.__ranjson[fileExt][randomName][CONTENT].append(imageName)
        if allMatch is not None:
            self.__ranjson[fileExt][randomName][ALLMATCH] = allMatch

        self.__logger.info(
            f"{__name__}類別新增{randomName}至{fileExt}的json圖庫；匹配規則為{allMatch}。")

    def addRelatedWordtoJson(self, randomName: str, relatedWord: list[str]):
        '''
        將相關字串加入json圖庫中
        '''
        for i in FILE_EXTENSION:
            if randomName in self.__ranjson[i]:
                self.__ranjson[i][randomName][RELATEDWORD] += relatedWord
                self.__logger.info(
                    f"{__name__}類別新增{randomName}的相關字串至{randomName}的json圖庫。")
                return True
        self.__logger.warning(f"{__name__}類別無法找到隨機觸發名{randomName}")
        return False

    def changeMatch(self,
                    randomName: str,
                    allMatch: bool):
        '''
        變更圖片名稱的匹配規則
        '''
        for i in FILE_EXTENSION:
            if randomName in self.__ranjson[i]:
                self.__ranjson[i][randomName][ALLMATCH] = allMatch
        self.__logger.info(f"{__name__}類別變更{randomName}的匹配規則為{allMatch}。")


    def getRandomImageName(self,
                           randomName: str,
                           fileExt: str = None) -> str | None:
        '''
        取得隨機圖片
        '''
        if fileExt is None:
            result = [
                content for fileExt in FILE_EXTENSION
                if randomName in self.__ranjson[fileExt]
                for content in self.__ranjson[fileExt][randomName][CONTENT]
            ]
            if result:
                return random.choice(result)
            return None
        else:
            if randomName in self.__ranjson[fileExt]:
                return random.choice(
                    self.__ranjson[fileExt][randomName][CONTENT])
            return None
    
    def getAllRandomName(self, fileExt: str) -> list[str]:
        '''
        取得所有隨機名稱
        '''
        return [randomName for randomName in self.__ranjson[fileExt].keys()]

    def getAllRandomNameStr(self, fileExt: str) -> str:
        '''
        取得所有隨機名稱
        '''
        return '、'.join(self.getAllRandomName(fileExt))

    def getImageList(self, randomName: str, fileExt: str) -> list[str]:
        '''
        取得隨機名稱的圖片列表
        '''
        if randomName in self.__ranjson[fileExt]:
            return self.__ranjson[fileExt][randomName][CONTENT]
        return []

    def getRelatedWordList(self,
                           randomName: str) -> list[str]:
        '''
        取得隨機名稱的相關字串列表
        '''
        for i in FILE_EXTENSION:
            if randomName in self.__ranjson[i]:
                return self.__ranjson[i][randomName][RELATEDWORD]
        return []

    def getMatch(self, randomName: str) -> bool | None:
        for i in FILE_EXTENSION:
            if randomName in self.__ranjson[i]:
                return self.__ranjson[i][randomName][ALLMATCH]
        return None

    def matchString(self, string: str) -> list[str]:
        '''
        從字串中取得隨機觸發名並回傳
        '''
        result = []
        for randomName, relatedWordList in self.__notallMatchCache.items():
            if (randomName in string):
                result.append(randomName)
            elif any(True for word in relatedWordList if word in string):
                result.append(randomName)
        return result


class RandomImage():

    def __init__(self, logger: logging.Logger, ranfile: str, imgfile: str):
        self.__logger = logger
        self.imageJson = image(logger, imgfile, FILE_EXTENSION)
        self.__RandomNameJson = RandomNameJson(logger, ranfile)

    def __checkFileExt(self, imageName: str):
        '''
        檢查圖片副檔名是否符合隨機資料庫中的副檔名
        :param imageName: 圖片名稱
        :return: 符合的副檔名，沒有符合的副檔名則回傳None
        '''
        for i in FILE_EXTENSION:
            if imageName.endswith(i):
                return i
        return None

    def __splitRandomName(self, randomName: str) -> tuple[str, str]:
        '''
        將隨機名稱分割為隨機名稱+副檔名(如果有)
        '''
        if (ext := self.__checkFileExt(randomName)) is not None:
            return randomName[:-len(ext)], ext
        return randomName, None

    def checkRandomName(self, randomName: str) -> bool:
        return self.__RandomNameJson.checkRandomNameinJson(randomName)

    def updateRandomNameImage(self, imageName: str, randomName: str):
        try:
            fileExt = None
            self.imageJson.refresh()
            fileExt = self.__checkFileExt(imageName)

            if (fileExt is None):
                self.__logger.info(f"{imageName}的副檔名不符合隨機資料庫中的副檔名或沒有副檔名。")
                return False

            if (self.imageJson.getimg(imageName)):
                self.__RandomNameJson.addRandomNametoJson(
                    randomName, imageName, fileExt)
                self.__logger.info(
                    f"{__name__}嘗試新增{imageName}歸屬於{randomName}下。")
                self.__RandomNameJson.saveJson()
                return True
            else:
                self.__logger.info(f"新增失敗，{imageName}並不存在於圖片庫中。")
                return False

        except:
            self.__logger.error("", exc_info=True)
    
    def updateMatch(self, randomName: str, allMatch: bool):
        if self.checkRandomName(randomName):
            self.__RandomNameJson.changeMatch(randomName, allMatch)
            self.__RandomNameJson.saveJson()
            self.__logger.info(f"{__name__}更新{randomName}的匹配規則為{allMatch}。")
            return True
        else:
            self.__logger.info(f"{__name__}隨機觸發名{randomName}不存在於隨機圖庫中。")
            return False

    def updateRelatedWord(self, randomName: str, relatedWord: list[str]):
        try:
            self.__RandomNameJson.addRelatedWordtoJson(randomName, relatedWord)
            self.__RandomNameJson.saveJson()
            self.__logger.info(f"{__name__}新增{randomName}的相關字串。")
            return True
        except:
            self.__logger.error("", exc_info=True)
            return False

    def getRandomImage(self, messageContent: str) -> str | None:
        if randomName := self.__RandomNameJson.matchString(messageContent):
            self.__logger.info(f"{__name__}偵測到隨機觸發名{randomName[0]}。")
            return self.imageJson.getimg(
                self.__RandomNameJson.getRandomImageName(randomName[0]))

        randomName, fileExt = self.__splitRandomName(messageContent)
        imageName = self.__RandomNameJson.getRandomImageName(
            randomName, fileExt)
        if imageName is not None:
            self.__logger.info(f"{__name__}偵測到隨機觸發名{randomName}.{fileExt}。")
            return self.imageJson.getimg(imageName)
        return None

    def getRelatedWord(self, randomName: str) -> str:
        '''
        取得關聯字，以'、'分隔
        '''
        self.__logger.info(f"{__name__}取得{randomName}的關聯字庫。")
        return '、'.join(self.__RandomNameJson.getRelatedWordList(randomName))
    
    def getAllRandomName(self, fileExt: str = None, loggerEnalbe: bool = True) -> list[str]:
        if fileExt is None:
            if loggerEnalbe:
                self.__logger.info(f"{__name__}取得所有隨機名稱。")
            return [
                i for ext in FILE_EXTENSION
                for i in self.__RandomNameJson.getAllRandomName(ext)]
        else:
            if loggerEnalbe:
                self.__logger.info(f"{__name__}取得{fileExt}副檔名的隨機名稱。")
            return self.__RandomNameJson.getAllRandomName(fileExt)

    def listRandom(self, fileExt: str = None, randomName: str | None = None):
        result = ""
        if (fileExt is None) and (randomName is None):
            self.__logger.info(f"{__name__}列出所有隨機名稱。")
            for ext in FILE_EXTENSION:
                result += f"{ext}:\n" + self.__RandomNameJson.getAllRandomNameStr(
                    ext) + "\n"
            return result

        if randomName is None:
            self.__logger.info(f"{__name__}列出{fileExt}副檔名的隨機名稱。")
            return f"{fileExt}:\n" + self.__RandomNameJson.getAllRandomNameStr(
                fileExt) + "\n"

        if fileExt is None:
            self.__logger.info(f"{__name__}列出{randomName}的圖片列表。")
            result = '、'.join([
                i for ext in FILE_EXTENSION
                for i in self.__RandomNameJson.getImageList(randomName, ext)
            ])
            if result:
                result += f"\n匹配規則:{"全部符合" if self.__RandomNameJson.getMatch(randomName) else "部分符合"}\n"
            return result

        self.__logger.info(f"{__name__}列出{randomName}.{fileExt}的圖片列表。")
        result= '、'.join(self.__RandomNameJson.getImageList(
            randomName, fileExt))
        if result:
            result += f"\n匹配規則:{"全部符合" if self.__RandomNameJson.getMatch(randomName) else "部分符合"}\n"
        return result

    def refresh(self):
        self.imageJson.refresh()
        self.__RandomNameJson.refresh()
        self.__logger.info(f"{__name__}刷新完成。")
