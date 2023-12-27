import json,random
import logging
random.seed()
class quotes():
    def __init__(self,logger:logging.Logger,filename:str):
        self.__logger=logger
        self.__filename=filename
        self.__importjson()
    
    def __importjson(self):
        self.__logger.info(f"{__name__}開始初始化json圖庫。")
        self.__json={str():list()}
        try:
            j=json.load(open(self.__filename,'r',encoding='utf-8'))
        except FileNotFoundError:
            self.__logger.warning(f"初始化json失敗! 無法找到json檔案{self.__filename} !")
            return
        except:
            self.__logger.error(f"發生未處理的例外。",exc_info=True)
            return
        self.__json=j

    
    def __exportjson(self):
        json.dump(self.__json,open(self.__filename,'w',encoding='utf-8'),ensure_ascii=False)
        self.__logger.info(f"{__name__}輸出json圖庫。")

    def refresh(self):
        self.__importjson()
        self.__logger.info(f'{__name__}刷新完成。')

    def addquotes(self,index:str,data:str):
        if index in self.__json.keys():
            if data in self.__json[index]:
                return False
            self.__json[index].append(data)
        else:
            self.__json[index]=[data]
        self.__exportjson()
        return True


    def getquotes(self,index:str,select:int=None) -> str|None:
        try:
            if select!=None:
                return self.__json[index][select]
            result=random.choice(self.__json[index])
            return result
        except KeyError:
            return None
        except IndexError:
            return None
        except:
            self.__logger.error('',exc_info=True)
    
    def listquotes(self,index:str) -> str|None:
        result=''
        try:
            for j in self.__json[index]:
                result+=j+'\n----\n'
        except KeyError:
            return None
        result=index+':\n--######--\n'+result
        result+='--######--\n'
        return result
    
    def listindex(self):
        return list(self.__json.keys())