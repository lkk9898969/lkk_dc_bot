import json
import logging
import random
random.seed()

class relationword():
    def __init__(self,logger:logging.Logger,filename:str) -> None:
        self.__logger=logger
        self.__wordfile=filename
        self.__importjson()

    def __importjson(self):
        self.__wordjson={'':['']}
        self.__logger.info(f"{__name__}類別開始初始化json圖庫。")
        try:
            wordj=json.load(open(self.__wordfile,'r',encoding='utf-8'))
            self.__wordjson=wordj
        except FileNotFoundError:
            self.__logger.warning(f"初始化json失敗! 無法找到json檔案{self.__wordfile} !")
        except:
            self.__logger.error(f"發生未處理的例外。",exc_info=True)

    def __exportjson(self):
        json.dump(self.__wordjson,open(self.__wordfile,'w',encoding='utf-8'),ensure_ascii=False)
        self.__logger.info(f"{__name__}類別開始初始化json圖庫。")

    def addrelationword(self,mainword:str,word:str):
        temp=[]
        if word in self.__wordjson:
            temp=self.__wordjson[word]
        temp.append(mainword)
        self.__wordjson[word]=temp
        self.__logger.info(f"{__name__}新增關聯字 {word} 與mainword {mainword} 關聯。")
        self.__exportjson()
    
    def getrelationword(self,word:str):
        try:
            result=self.__wordjson[word]
            result=random.choice(result)
            self.__logger.info(f"{__name__}透過關聯字 {word} 回傳了隨機觸發名 {result}。")
            return result
        except KeyError:
            return None
        except:
            self.__logger.error("",exc_info=True)

    def listrelationword(self):
        mainwordtemp={}
        result=''
        for word , mainword in self.__wordjson.items():
            for i in mainword:
                if i in mainwordtemp.keys():
                    mainwordtemp[i].append(word)
                else:
                    mainwordtemp[i]=[word]
        for mainword,words in mainwordtemp.items():
            result+=mainword+':\n'
            for i in words:
                result+=i+','
            result=result[:-1]+'\n'
        self.__logger.info(f"{__name__}回傳了關聯字列表。")
        return result
    
    def get_randomnameandword(self,random_name:str=None,word:str=None):
        result=''
        if random_name and word:
            if word in self.__wordjson.keys():
                if random_name in self.__wordjson[word]:
                    result='True'
                else:
                    result='False'
            else:
                result='False'
            self.__logger.info(f"{__name__}回傳了 {random_name} 與 {word} 的關聯關係。結果為{result}。")
        elif random_name:
            resulttemp=''
            for word , mainword in self.__wordjson.items():
                if random_name in mainword:
                    resulttemp+=f'{word}、'
            if not resulttemp:
                self.__logger.info(f"{__name__}試圖檢索隨機觸發名 {random_name} ，但該隨機觸發名並未在關聯字庫中。")
                return None
            result=f'{random_name} 可以被:\n'+resulttemp[:-1]+'\n以上關聯字觸發。'
            self.__logger.info(f"{__name__}檢索了隨機觸發名 {random_name} 以下的關聯字。")
        elif word:
            result=f'{word} 可以觸發:\n'
            try:
                for i in self.__wordjson[word]:
                    result+=f'{i}、'
                result=result[:-1]+'\n以上隨機觸發名。'
                self.__logger.info(f"{__name__}檢索了可觸發關聯字 {word} 的所有隨機觸發名。")
            except KeyError:
                self.__logger.info(f"{__name__}試圖檢索關聯字 {word} ，但該關聯字並不存在於關聯字庫中。")
                return None
        else:
            self.__logger.info(f"{__name__}中的get_randomnameandword函數被呼叫，但未給定任何參數。")
            return None
        return result
