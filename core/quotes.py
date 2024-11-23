import json, random
import logging

random.seed()

CONTENT = 'content'
RELATED_NAME = 'related'


class QuotesJson():

    def __init__(self,
                 logger: logging.Logger,
                 name: str,
                 quote: list[str],
                 relatedName: list[str] = None):
        self.__logger = logger
        self.__name = name
        self.__quote = quote
        self.__relatedName = relatedName
        self.__logger.info(f"{self.__name}初始化完成。")

    def __contains__(self, item: str) -> bool:
        return item == self.__name or item in self.__relatedName

    def __eq__(self, value):
        if isinstance(value, str):
            return value == self.__name
        elif isinstance(value, QuotesJson):
            return super().__eq__(value)
        else:
            return NotImplemented

    def __str__(self):
        return self.__name

    def exportDict(self):
        self.__logger.info(f"{self.__name}輸出語錄。")
        return {
            self.__name: {
                CONTENT: self.__quote,
                RELATED_NAME: self.__relatedName
            }
        }

    def addQuote(self, data: str):
        '''
        新增語錄。若新增成功則會回傳True。  
        如果語錄已存在於語錄庫中，則回傳False且不會新增。
        '''
        if self.__quote is None:
            self.__quote = []
        elif data in self.__quote:
            return False
        self.__quote.append(data)
        return True

    def addRelated(self, related: str):
        '''
        新增相關分類名稱。  
        若相關分類名稱已存在於相關分類名稱列表中，則不會新增。
        '''
        if self.__relatedName is None:
            self.__relatedName = []
        elif related in self.__relatedName:
            return
        self.__relatedName.append(related)

    def getQuote(self, select: int = None) -> str | None:
        try:
            if len(self.__quote) == 0:
                return None
            if select != None:
                return self.__quote[select]
            result = random.choice(self.__quote)
            return result
        except IndexError:
            return None
        except:
            self.__logger.error('', exc_info=True)

    def getQuoteList(self) -> list[str] | None:
        if len(self.__quote) == 0:
            return None
        return self.__quote

    def getRelatedList(self) -> list[str] | None:
        if self.__relatedName == None:
            return None
        return self.__relatedName


class Quotes():

    def __init__(self, logger: logging.Logger, filename: str):
        self.__logger = logger
        self.__filename = filename
        self.__json: list[QuotesJson] = []
        self.__importjson()

    def __importjson(self):
        self.__logger.info(f"{__name__}開始初始化語錄資料庫。")
        try:
            j = json.load(open(self.__filename, 'r', encoding='utf-8'))
        except FileNotFoundError:
            self.__logger.warning(f"初始化json失敗! 無法找到json檔案{self.__filename} !")
            return
        except:
            self.__logger.error(f"發生未處理的例外。", exc_info=True)
            return
        self.__json = [
            QuotesJson(self.__logger, k, v[CONTENT], v.get(RELATED_NAME, None))
            for k, v in j.items()
        ]

    def __exportjson(self):
        _json = {}
        for i in self.__json:
            _json.update(i.exportDict())
        json.dump(_json,
                  open(self.__filename, 'w', encoding='utf-8'),
                  ensure_ascii=False,
                  indent=4)
        self.__logger.info(f"{__name__}輸出json語錄庫。")

    def refresh(self):
        self.__importjson()
        self.__logger.info(f'{__name__}刷新完成。')

    def checkNameStrict(self, name: str) -> bool:
        '''
        檢查語錄分類名稱是否存在於語錄庫中。  
        嚴格檢查，即忽略相關分類名稱。
        '''
        return any(i == name for i in self.__json)

    def checkName(self, name: str) -> bool:
        '''
        檢查語錄分類名稱是否存在於語錄庫中。  
        寬鬆檢查。
        '''
        return any(name in i for i in self.__json)

    def addQuoteName(self, name: str):
        '''
        新增語錄分類名稱。若語錄分類名稱已存在於語錄庫中，則不會新增。
        '''
        if self.checkNameStrict(name):
            self.__logger.warning(f'{name}已存在於語錄庫中。')
            return False
        self.__json.append(QuotesJson(self.__logger, name, []))
        self.__exportjson()
        self.__logger.info(f'{name}新增至語錄庫。')
        return True

    def addQuote(self, name: str, data: str):
        '''
        新增語錄。  
        請注意，語錄分類名稱必須存在於語錄庫中，否則將不會新增語錄。
        '''
        for i in self.__json:
            if i == name:
                result = i.addQuote(data)
                self.__exportjson()
                self.__logger.info(f'{i}新增{data}語錄。')
                return result
        self.__logger.warning(f'{name}不存在於語錄庫中。')
        return False

    def addRelated(self, name: str, related: str):
        '''
        新增相關分類名稱。  
        請注意，語錄分類名稱必須存在於語錄庫中，否則將不會新增相關分類名稱。  
        若相關分類名稱已存在於相關分類名稱列表中，則不會新增。
        '''
        for i in self.__json:
            if i == name:
                i.addRelated(related)
                self.__exportjson()
                self.__logger.info(f'{i}新增{related}相關分類名稱。')
                return True
        self.__logger.warning(f'{name}不存在於語錄庫中。')
        return False

    def getQuote(self, name: str, select: int = None) -> str | None:
        '''
        取得語錄。  
        語錄分類名稱為寬鬆檢查(即亦會檢查相關分類名稱)，但必須完全符合。  
        給定select參數則會從語錄列表中選擇第select個語錄。  
        語錄分類名稱不存在於語錄庫中 或 給定的select參數超出範圍，則回傳None。
        '''
        try:
            for i in self.__json:
                if name in i:
                    self.__logger.info(f"{__name__}回傳了{i}。")
                    return i.getQuote(select)
            return None
        except:
            self.__logger.error('', exc_info=True)

    def getQuoteList(self, name: str) -> list[str] | None:
        for i in self.__json:
            if i == name:
                self.__logger.info(f"{__name__}回傳了{i}的語錄列表。")
                return i.getQuoteList()
        return None

    def listName(self):
        return [str(i) for i in self.__json]
