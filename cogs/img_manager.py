import discord
from discord import app_commands
from discord.ext import commands
from core.lkk_log import loggerhandler
from core.lkkcog import lkkCog
from core.randomimg import ranimg
from core.relationword import relationword
from typing import Optional

imgfile="image.json"
ranfile="image_random.json"
wordfile='image_relationword.json'
fileextension=['.jpg','.gif']

        
class imgmanager(lkkCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        logname="img_manager"
        self.logger=loggerhandler("lkkdc."+logname,logname,level='INFO',consoleattach=False)
        self.randomdata=ranimg(self.logger,ranfile,imgfile)
        self.relationword=relationword(self.logger,wordfile)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"extension {__name__}載入完成。")

    async def returnimage(self,func,message:discord.Message,content:Optional[str]=None):
            if content:
                reply=func(content)
            else:
                reply=func(message.content)
                content=message.content
            if reply:
                await message.reply(reply)
                self.logger.info(f"向#{message.channel.name} 回傳了隨機觸發名為 {content} 的隨機圖片。")
                return True
            else:
                return False
    
    @commands.command()
    async def updateimg(self,ctx:commands.Context,imgname:str,url:str):
        self.logger.info(f"{ctx.author.name}使用了updateimg指令。")
        if self.is_admin(ctx):
            try:
                if imgname.endswith('.jpg'):
                    self.randomdata.imgjson.addimg('\\'+imgname,url)
                    await ctx.reply("新增成功!")
                    self.logger.debug(f"新增了一個圖檔，觸發名:\\{imgname}，URL:{url}")
                elif imgname.endswith('.gif'):
                    self.randomdata.imgjson.addimg('\\'+imgname,url)
                    await ctx.reply("新增成功!")
                    self.logger.debug(f"新增了一個圖檔，觸發名:\\{imgname}，URL:{url}")
                else:
                    await ctx.reply(f"資料錯誤! 請確認觸發名稱是否為{fileextension}結尾!")
                    self.logger.debug(f"新增圖檔時檢測到觸發名不正確。觸發名:{imgname}，URL:{url}")
            except:
                self.logger.error("",exc_info=True)

    @commands.command()
    async def updaterandom(self,ctx:commands.Context,imgname:str,randomname:str):
        self.logger.info(f"{ctx.author.name}使用了updaterandom指令。")
        if self.is_admin(ctx):
            try:
                if self.randomdata.updaterandomimg('\\'+imgname,randomname):
                    await ctx.reply("新增成功!")
                else:
                    await ctx.reply("新增失敗! 請詢問湯麵本人發生什麼事了。")
                    self.logger.info(f"{ctx.author.name}嘗試新增random資料庫但失敗。")
            except:
                self.logger.error("",exc_info=True)
    
    @commands.command()
    async def updateword(self,ctx:commands.Context,mainword:str,*words:str):
        self.logger.info(f"{ctx.author.name}使用了updateword指令。")
        if self.is_admin(ctx):
            try:
                reply=self.randomdata.getranimg(mainword)
                if words:
                    if reply:
                        for i in words:
                            self.relationword.addrelationword(mainword,i)
                        await ctx.reply(f"新增成功!")
                    else:
                        await ctx.reply(f"{mainword}不存在於隨機圖片庫中。")
                        self.logger.info(f"{ctx.author.name}嘗試新增 {mainword} 的關聯字，但 {mainword} 不存在於隨機圖片庫中。")
                else:
                    await ctx.reply("請輸入至少1個關聯字!")
                    self.logger.info(f"{ctx.author.name}嘗試新增關聯字但未給定關聯字。")
            except:
                self.logger.error("",exc_info=True)
    
    @commands.command()
    @commands.is_owner()
    async def refreshr(self,ctx:commands.Context):
        self.randomdata.refresh()
        await ctx.reply("random刷新完成。")


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        flag=True
        for i in fileextension:
            if message.content.endswith(i):
                flag=False
                if not await self.returnimage(self.randomdata.getranimg , message):
                    word=self.relationword.getrelationword(message.content)
                    if not await self.returnimage(self.randomdata.getranimg , message,word):
                        await self.returnimage(self.randomdata.imgjson.getimg , message)

        if flag:
            if not await self.returnimage(self.randomdata.getranimg , message):
                word=self.relationword.getrelationword(message.content)
                await self.returnimage(self.randomdata.getranimg,message,word)


    @app_commands.command(name="image_list",description="列出所有可用觸發名稱(圖檔)")
    @app_commands.describe(ext="圖檔副檔名(Ex: .jpg )，若不選擇預設為輸出全部")
    @app_commands.choices(
        ext=[app_commands.Choice(name=i,value=i) for i in fileextension]
    )
    async def listimg(self,interaction: discord.Interaction, ext: Optional[str] = "all"):
        listimg=self.randomdata.imgjson.listimg(ext)
        if(listimg):
            listimg+='\n請注意，要叫出這裡的圖片關鍵字前需加反斜線(\\\)，\n若列出的關鍵字本身有自帶反斜線或開頭為az的就不用了。'
            await interaction.response.send_message(content=listimg,ephemeral=True)
            self.logger.info(f"向{interaction.user.name}回傳了圖片庫。副檔名:{ext}")
        else:
            await interaction.response.send_message(content=f"圖庫中不存在任何副檔名為{ext}的圖。",ephemeral=True)
            self.logger.debug(f"{interaction.user.name}試圖檢視副檔名為{ext}的所有圖片，但圖片庫未有任何符合條件的圖片。")

    @app_commands.command(name="random_list",description="列出所有可用的隨機觸發名稱。若有指定隨機觸發名，則改為回傳該隨機觸發名可以觸發的圖片觸發名。")
    @app_commands.describe(ext="圖檔副檔名(Ex: .jpg )，若不選擇預設為輸出全部",random_name="指定的隨機觸發名")
    @app_commands.choices(
        ext=[app_commands.Choice(name=i,value=i) for i in fileextension]
    )
    async def listrandom(self,interaction: discord.Interaction, ext: Optional[str]=None , random_name:Optional[str]=None):
        listimg=self.randomdata.listrandom(ext,random_name)
        if not ext:
            ext='無'
        if random_name:
            if(listimg):
                await interaction.response.send_message(content=listimg,ephemeral=True)
                self.logger.info(f"向{interaction.user.name}回傳了關於 {random_name} 副檔名:{ext}的隨機圖片庫。")
            else:
                await interaction.response.send_message(content=f"隨機觸發名{random_name}{ext}不存在於隨機圖片庫中。",ephemeral=True)
                self.logger.info(f"{interaction.user.name}試圖檢視隨機觸發名 {random_name} 副檔名:{ext}，但隨機圖片庫未有該隨機觸發名。")

        else:
            if(listimg):
                await interaction.response.send_message(content=listimg,ephemeral=True)
                self.logger.info(f"向{interaction.user.name}回傳了隨機圖片庫。副檔名:{ext}")
            else:
                await interaction.response.send_message(content=f"隨機圖庫中不存在任何副檔名為{ext}的圖。",ephemeral=True)
                self.logger.info(f"{interaction.user.name}試圖檢視副檔名為{ext}的所有隨機圖片，但隨機圖片庫未有任何符合條件的圖片。")

    @app_commands.command(name="word_list",description="列出所有的關聯字，若有給參數會改變指令回傳的東西。")
    @app_commands.describe(random_name="隨機觸發名。若有填此項則僅列出該隨機觸發名關聯的所有關聯字。",word="關聯字。若有填此項則僅列出該關聯字可觸發的所有隨機觸發名。")
    async def listrelationword(self,interaction:discord.Interaction,random_name:Optional[str]=None,word:Optional[str]=None):
        try:
            if random_name or word:
                result=self.relationword.get_randomnameandword(random_name,word)
                if result:
                    await interaction.response.send_message(content=result,ephemeral=True)
                    self.logger.info(f"向{interaction.user.name}回傳了部分關聯字。random_name= {random_name} 、word= {word} 。")
                else:
                    if random_name:
                        result=f'隨機觸發名 {random_name} 不存在於關聯字庫中。'
                    elif word:
                        result=f'關聯字 {word} 不存在於關聯字庫中。'
                    await interaction.response.send_message(content=result,ephemeral=True)
                    self.logger.info(f"向{interaction.user.name}檢索關聯字但失敗。random_name= {random_name} 、word= {word} 。")
            else:
                result=self.relationword.listrelationword()
                await interaction.response.send_message(content=result,ephemeral=True)
                self.logger.info(f"向{interaction.user.name}回傳了所有關聯字。")
        except:
            self.logger.error("",exc_info=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(imgmanager(bot))
