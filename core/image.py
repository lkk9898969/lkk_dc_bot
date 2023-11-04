import json
import logging

class image():
    def __init__(self,logger:logging.Logger,file:str,fileextension:list):
        self.__logger=logger
        self.__filename=file
        self.__file_extension=fileextension
        self.__importjson(file)
    
    def __importjson(self,_file:str):
        self.__logger.info(f"{__name__}開始初始化json圖庫。")
        self.__json={}
        try:
            j=json.load(open(_file,'r',encoding='utf-8'))
        except FileNotFoundError:
            self.__logger.warning(f"初始化json失敗! 無法找到json檔案{_file} !")
            return
        except:
            self.__logger.error(f"發生未處理的例外。",exc_info=True)
            return
        for i in self.__file_extension:
            try:
                self.__json[i]=j[i]
            except KeyError:
                self.__logger.warning(f"初始化:圖片庫中未有任何副檔名為{i}的圖片。")
                continue
    
    def __exportjson(self,_file:str):
        json.dump(self.__json,open(_file,'w',encoding='utf-8'),ensure_ascii=False)
        self.__logger.info(f"{__name__}輸出json圖庫。")
    
    def __getimg(self,_file_extension:str,_name:str):
        if _file_extension in self.__file_extension:
            try:
                result = self.__json[_file_extension][_name]
                self.__logger.info(f"{__name__}回傳了一個圖片。圖片名.副檔名:{_name}{_file_extension}")
                return result
            except KeyError:
                return None
    
    def __addimg(self,_file_extension:str,_name:str,_url:str):
        self.__json[_file_extension][_name]=_url
        self.__logger.info(f"{__name__}新增了一個圖片。圖片名.副檔名:{_name}{_file_extension}")
        self.__exportjson(self.__filename)

    def getimg(self,name:str):
        for i in self.__file_extension:
            if name.endswith(i):
                return self.__getimg(i,name[:-4])
    
    def listimg(self,name:str):
        if name=="all":
            imglist=""
            for fileext,value in self.__json.items():
                imglist=imglist+f"\n{fileext}:\n"
                for filename in value.keys():
                    imglist=imglist+f"{filename} , "
                imglist=imglist.rstrip(', ')
            imglist=imglist.lstrip()
            self.__logger.info(f"{__name__}回傳了圖片庫。")
        elif name in self.__file_extension:
            imglist=f"{name}:\n"
            for filename in self.__json[name].keys():
                imglist=imglist+f"{filename} , "
            imglist=imglist.rstrip(', ').lstrip()
            self.__logger.info(f"{__name__}回傳了副檔名為{name}圖片庫。")
        else:
            imglist=None
        return imglist

    def addimg(self,name:str,url:str):
        if(url.startswith("http")):
            for i in self.__file_extension:
                if name.endswith(i):
                    self.__addimg(i,name.rstrip(i),url)
                    break
        else:
            self.__logger.warning(f"{__name__}在新增圖檔時檢測到URL非http開頭。")
            self.__logger.warning(f"觸發名:{name}，URL:{url}")
    
    def refresh(self):
        self.__importjson(self.__filename)
        self.__logger.info(f"{__name__}刷新完成。")