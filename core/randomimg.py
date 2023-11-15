import json
import logging
from core.image import image
import random
random.seed()
fileextension=['.jpg','.gif']


class ranimg():
    def __init__(self,logger:logging.Logger,ranfile:str,imgfile:str):
        self.__logger=logger
        self.__ranfile=ranfile
        self.imgjson=image(logger,imgfile,fileextension)
        self.__importjson(ranfile)
    
    def __importjson(self,ranfile:str):
        self.__logger.info(f"{__name__}類別開始初始化json圖庫。")
        self.__ranjson={}
        try:
            ranj=json.load(open(ranfile,'r',encoding='utf-8'))
        except FileNotFoundError:
            self.__logger.warning(f"初始化json失敗! 無法找到json檔案{ranfile} !")
            return
        except:
            self.__logger.error(f"發生未處理的例外。",exc_info=True)
            return
        try:
            self.__ranjson=ranj
        except :
            self.__logger.error("",exc_info=True)
    
    def __exportjson(self,_file:str):
        json.dump(self.__ranjson,open(_file,'w',encoding='utf-8'),ensure_ascii=False)
        self.__logger.info(f"{__name__}類別輸出json圖庫。")

    def updaterandomimg(self,imgname:str,randomname:str):
        try:
            self.imgjson.refresh()
            for i in fileextension:
                if imgname.endswith(i):
                    fileext=i
                    self.__logger.info(f"{__name__}嘗試新增{imgname}歸屬於{randomname}下。")
                    break
            try:
                if(fileext):
                    pass
            except:
                self.__logger.info(f"{imgname}的副檔名不符合隨機資料庫中的副檔名或沒有副檔名。")
                return False
            if (self.imgjson.getimg(imgname)):
                if fileext in self.__ranjson:
                    if randomname in self.__ranjson[fileext]:
                        array=self.__ranjson[fileext][randomname]
                        array.append(imgname)
                        self.__logger.info(f"已成功將{imgname}歸類於{randomname}下。")
                    else:
                        self.__logger.info(f"正在新增{randomname}索引資料，因random資料庫未有該索引。")
                        array=[imgname]
                        self.__ranjson[fileext][randomname]=array
                else:
                    self.__logger.info(f"正在新增{fileext}副檔名及其資料，因random資料庫未有該副檔名。")
                    array=[imgname]
                    self.__ranjson[fileext]={}
                    self.__ranjson[fileext][randomname]=array
                self.__exportjson(self.__ranfile)
                return True
            else:
                self.__logger.info(f"新增失敗，{imgname}並不存在於圖片庫中。")
                return False

        except:
            self.__logger.error("",exc_info=True)

    def listrandom(self,ext=None,randomname:str|None=None):
        result=""
        if not ext:
            if randomname:
                for i,j in self.__ranjson.items():
                    if self.getranimg(randomname+i):
                        result+=i+':\n'
                        # self.__logger.info(str(j))
                        for k in j[randomname]:
                            result+=k+'、'
                        result=result[:-1]+'\n'
            else:
                for i in self.__ranjson.keys():
                    result+=i+':\n  '
                    for j in self.__ranjson[i].keys():
                        result+=j+'、'  
                    result=result[:-1]+'\n'
                self.__logger.info(f"{__name__}類別回傳隨機圖庫。")
        else:
            result+=ext+':\n  '
            if randomname:
                if self.getranimg(randomname+ext):
                    for i in self.__ranjson[ext][randomname]:
                        result+=k+','
                    result=result[:-1]+'\n'
                else:
                    return None
            else:
                try:
                    for i in self.__ranjson[ext].keys():
                        result+=j+'、'  
                    result=result[:-1]+'\n'
                    self.__logger.info(f"{__name__}類別回傳副檔名為{ext}的隨機圖庫。")
                except KeyError:
                    return None
        return result
    
    def getranimg(self,ranname:str):
        result=[]
        for i in self.__ranjson.keys():
            if ranname in self.__ranjson[i].keys():
                for j in self.__ranjson[i][ranname]:
                    result.append(j)
        if result:
            result=random.choice(result)
            self.__logger.info(f"{__name__}回傳了隨機圖片，圖片名:{result}。")
            return self.imgjson.getimg(result)
        else:
            for i in self.__ranjson.keys():
                if ranname.endswith(i):
                    if ranname[:-4] in self.__ranjson[i].keys():
                            result=self.__ranjson[i][ranname[:-4]]
                            break
        if result:
            result=random.choice(result)
            self.__logger.info(f"{__name__}回傳了隨機圖片，圖片名:{result}。")
            return self.imgjson.getimg(result)
        else:
            return None
        
    def refresh(self):
        self.imgjson.refresh()
        self.__importjson(self.__ranfile)
        self.__logger.info(f"{__name__}刷新完成。")
    