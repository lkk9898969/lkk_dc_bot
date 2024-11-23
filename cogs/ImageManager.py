import discord
import time
from discord import app_commands
from discord.ext import commands
from core.lkk_log import loggerhandler
from core.lkkcog import lkkCog, is_admin_check
from core.RandomImage import RandomImage
from typing import Optional, Callable

imgfile = "image.json"
ranfile = "image_random.json"
fileextension = ['.jpg', '.gif']


class ImageManager(lkkCog):

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        logname = "ImageManager"
        self.logger = loggerhandler("lkkdc." + logname,
                                    logname + time.strftime("-%Y%m%d"),
                                    cwd="log",
                                    level='INFO',
                                    logfile_level="DEBUG",
                                    attachConsole=False)
        self.RandomImageProcesser = RandomImage(self.logger, ranfile, imgfile)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"extension {__name__}載入完成。")

    async def returnimage(self,
                          func: Callable[[str], str],
                          message: discord.Message,
                          content: Optional[str] = None):
        if content:
            reply = func(content)
        else:
            reply = func(message.content)
            content = message.content
        if reply:
            await message.reply(reply)
            self.logger.info(f"向#{message.channel.name} 回傳了隨機圖片。")
            return True
        else:
            return False

    async def _UpdateImage(self,
                           imgname: str,
                           url: str,
                           *,
                           ctx: commands.Context = None,
                           interaction: discord.Interaction = None):
        if ctx is None and interaction is None:
            return
        if ctx is None:
            reply = lambda x: interaction.response.send_message(x,
                                                                ephemeral=True)
        else:
            reply = ctx.reply
        try:
            if imgname.endswith('.jpg'):
                self.RandomImageProcesser.imageJson.addimg('\\' + imgname, url)
                await reply("新增成功!")
                self.logger.debug(f"新增了一個圖檔，觸發名:\\{imgname}，URL:{url}")
            elif imgname.endswith('.gif'):
                self.RandomImageProcesser.imageJson.addimg('\\' + imgname, url)
                await reply("新增成功!")
                self.logger.debug(f"新增了一個圖檔，觸發名:\\{imgname}，URL:{url}")
            else:
                await reply(f"資料錯誤! 請確認觸發名稱是否為{fileextension}結尾!")
                self.logger.debug(f"新增圖檔時檢測到觸發名不正確。觸發名:{imgname}，URL:{url}")
        except:
            self.logger.error("", exc_info=True)

    async def _UpdateRandom(self,
                            imgname: str,
                            randomname: str,
                            *,
                            ctx: commands.Context = None,
                            interaction: discord.Interaction = None):
        if ctx is None and interaction is None:
            return
        if ctx is None:
            reply = lambda x: interaction.response.send_message(x,
                                                                ephemeral=True)
        else:
            reply = ctx.reply
        try:
            if self.RandomImageProcesser.updateRandomNameImage(
                    '\\' + imgname, randomname):
                await reply("新增成功!")
                self.logger.debug(
                    f"新增了一個random名稱，圖檔名稱:\\{imgname}，random名稱:{randomname}")
            else:
                await reply("新增失敗! 請詢問湯麵本人發生什麼事了。")
                self.logger.debug(
                    f"嘗試新增random資料庫但失敗。圖檔名稱:\\{imgname}，random名稱:{randomname}")
        except:
            self.logger.error("", exc_info=True)

    async def _UpdateWord(self,
                          mainword: str,
                          *words: str,
                          ctx: commands.Context = None,
                          interaction: discord.Interaction = None):
        if ctx is None and interaction is None:
            return
        if ctx is None:
            author = interaction.user.name
            reply = lambda x: interaction.response.send_message(x,
                                                                ephemeral=True)
        else:
            author = ctx.author.name
            reply = ctx.reply
        try:
            if words:
                if self.RandomImageProcesser.checkRandomName(mainword):
                    for i in words:
                        self.RandomImageProcesser.updateRelatedWord(
                            mainword, i)
                    await reply(f"新增成功!")
                else:
                    await reply(f"{mainword}不存在於隨機圖片庫中。")
                    self.logger.debug(
                        f"{author}嘗試新增 {mainword} 的關聯字，但 {mainword} 不存在於隨機圖片庫中。"
                    )
            else:
                await reply("請輸入至少1個關聯字!")
                self.logger.debug(f"{author}嘗試新增關聯字但未給定關聯字。")
        except:
            self.logger.error("", exc_info=True)

    #-------------------------------------------

    @commands.command(name='UpdateImage', aliases=['ir', 'IR'])
    async def UpdateImageCmd(self, ctx: commands.Context, imgname: str,
                             url: str):
        if self.is_admin(ctx):
            self.logger.info(f"{ctx.author.name}使用了UpdateImage指令。")
            await self._UpdateImage(imgname, url, ctx=ctx)

    # @app_commands.command(name='update_image', description="新增一個圖片到圖片庫中。")
    # @app_commands.describe(imgname='圖片名稱', url='圖片網址')
    # @app_commands.check(is_admin_check)
    # async def UpdateImageApp(self, interaction: discord.Interaction,
    #                          imgname: str, url: str):
    #     self.logger.info(f"{interaction.user.name}使用了UpdateImage指令。")
    #     await self._UpdateImage(imgname, url, interaction=interaction)

    #-------------------------------------------

    @commands.command(name="UpdateRandom", aliases=['ur', 'UR'])
    async def UpdateRandomCmd(self, ctx: commands.Context, imageName: str,
                              randomName: str):
        if self.is_admin(ctx):
            self.logger.info(f"{ctx.author.name}使用了UpdateRandom指令。")
            await self._UpdateRandom(imageName, randomName, ctx=ctx)

    # @app_commands.command(name='update_random', description="新增一個圖片的隨機名稱。")
    # @app_commands.describe(image_name='圖片名稱', random_name='隨機名稱')
    # @app_commands.check(is_admin_check)
    # async def UpdateRandomApp(self, interaction: discord.Interaction,
    #                           image_name: str, random_name: str):
    #     self.logger.info(f"{interaction.user.name}使用了UpdateRandom指令。")
    #     await self._UpdateRandom(image_name,
    #                              random_name,
    #                              interaction=interaction)

    #-------------------------------------------

    @commands.command(name="UpdateMatch", aliases=['um', 'UM'])
    async def UpdateMatchCmd(self, ctx: commands.Context, randomName: str,
                             match: str):
        if self.is_admin(ctx):
            self.logger.info(f"{ctx.author.name}使用了UpdateMatchm指令。")
            if "true" in match.lower():
                match = True
            elif "false" in match.lower():
                match = False
            else:
                self.logger.info(
                    f"嘗試更新隨機觸發名{randomName}的match值但失敗，因為match參數錯誤。match:{match}"
                )
                await ctx.reply("match參數錯誤:請輸入true或false")
                return
            if self.RandomImageProcesser.updateMatch(randomName, match):
                await ctx.reply("更新成功!")
                self.logger.info(f"更新了random名稱{randomName}的match值為{match}")
            else:
                await ctx.reply("更新失敗! 隨機圖庫中不存在該隨機名稱。")
                self.logger.info(
                    f"嘗試更新隨機觸發名{randomName}的match值但失敗，因為該隨機名稱不存在於隨機圖庫中。")

    #-------------------------------------------

    @commands.command(aliases=['uw', 'UW'])
    async def UpdateWordCmd(self, ctx: commands.Context, mainword: str, *words:
                            str):
        if self.is_admin(ctx):
            self.logger.info(f"{ctx.author.name}使用了UpdateWord指令。")
            await self._UpdateWord(mainword, *words, ctx=ctx)

    # @app_commands.command(name='update_word', description="新增一個關聯字到關聯字庫中。")
    # @app_commands.describe(mainword='關聯字', word='關聯字')
    # @app_commands.check(is_admin_check)
    # async def UpdateWordApp(self, interaction: discord.Interaction,
    #                         mainword: str, word: str):
    #     self.logger.info(f"{interaction.user.name}使用了UpdateWord指令。")
    #     await self._UpdateWord(mainword, word, interaction=interaction)

    #-------------------------------------------

    @commands.command()
    @commands.is_owner()
    async def refreshr(self, ctx: commands.Context):
        self.RandomImageProcesser.refresh()
        await ctx.reply("random刷新完成。")

    @app_commands.command(name="image_list", description="列出所有可用觸發名稱(圖檔)")
    @app_commands.describe(ext="圖檔副檔名(Ex: .jpg )，若不選擇預設為輸出全部")
    @app_commands.choices(
        ext=[app_commands.Choice(name=i, value=i) for i in fileextension])
    async def listimg(self,
                      interaction: discord.Interaction,
                      ext: Optional[str] = "all"):
        listimg = self.RandomImageProcesser.imageJson.listimg(ext)
        if (listimg):
            listimg += '\n**請注意，要叫出這裡的圖片關鍵字前需加反斜線(\\\)，\n若列出的關鍵字本身有自帶反斜線或開頭為az的就不用了。**'
            await interaction.response.send_message(content=listimg,
                                                    ephemeral=True)
            self.logger.info(f"向{interaction.user.name}回傳了圖片庫。副檔名:{ext}")
        else:
            await interaction.response.send_message(
                content=f"圖庫中不存在任何副檔名為{ext}的圖。", ephemeral=True)
            self.logger.debug(
                f"{interaction.user.name}試圖檢視副檔名為{ext}的所有圖片，但圖片庫未有任何符合條件的圖片。")

    @app_commands.command(
        name="random_list",
        description="列出所有可用的隨機觸發名稱。若有指定隨機觸發名，則改為回傳該隨機觸發名會觸發的圖片名稱。")
    @app_commands.describe(ext="圖檔副檔名(Ex: .jpg )，若不選擇預設為輸出全部",
                           random_name="指定的隨機觸發名")
    @app_commands.choices(
        ext=[app_commands.Choice(name=i, value=i) for i in fileextension])
    async def listrandom(self,
                         interaction: discord.Interaction,
                         ext: Optional[str] = None,
                         random_name: Optional[str] = None):
        listimg = self.RandomImageProcesser.listRandom(ext, random_name)
        if ext is None:
            ext = '無'
        if random_name:
            if (listimg):
                await interaction.response.send_message(content=listimg,
                                                        ephemeral=True)
                self.logger.info(
                    f"向{interaction.user.name}回傳了關於 {random_name} 副檔名:{ext}的隨機圖庫。"
                )
            else:
                await interaction.response.send_message(
                    content=f"隨機觸發名{random_name}不存在於隨機圖庫中。", ephemeral=True)
                self.logger.info(
                    f"{interaction.user.name}試圖檢視隨機觸發名 {random_name} 副檔名:{ext}，但隨機圖庫未有該隨機觸發名。"
                )

        else:
            if (listimg):
                await interaction.response.send_message(content=listimg,
                                                        ephemeral=True)
                self.logger.info(f"向{interaction.user.name}回傳了隨機圖片庫。副檔名:{ext}")
            else:
                await interaction.response.send_message(
                    content=f"隨機圖庫中不存在任何副檔名為{ext}的圖。", ephemeral=True)
                self.logger.info(
                    f"{interaction.user.name}試圖檢視副檔名為{ext}的所有隨機圖片，但隨機圖片庫未有任何符合條件的圖片。"
                )

    @app_commands.command(name="word_search", description="列出指定隨機觸發名的關聯字。")
    @app_commands.describe(random_name="隨機觸發名。")
    async def listrelationword(self, interaction: discord.Interaction,
                               random_name: str):
        try:
            if self.RandomImageProcesser.checkRandomName(random_name):
                listword = self.RandomImageProcesser.getRelatedWord(
                    random_name)
                if (listword):
                    await interaction.response.send_message(content=listword,
                                                            ephemeral=True)
                    self.logger.info(
                        f"向{interaction.user.name}回傳了關於 {random_name} 的關聯字。")
                else:
                    await interaction.response.send_message(
                        content=f"關聯字庫中不存在 {random_name} 的關聯字。",
                        ephemeral=True)
                    self.logger.info(
                        f"{interaction.user.name}試圖檢視關聯字庫中 {random_name} 的關聯字，但關聯字庫中不存在該關聯字。"
                    )
            else:
                await interaction.response.send_message(
                    content=f"隨機觸發名{random_name}不存在於隨機圖庫中。", ephemeral=True)
                self.logger.info(
                    f"{interaction.user.name}試圖檢視關聯字庫中 {random_name} 的關聯字，但隨機圖庫中不存在該隨機觸發名。"
                )
        except:
            self.logger.error("", exc_info=True)

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if await self.returnimage(self.RandomImageProcesser.getRandomImage,
                                  message):
            return

        for i in fileextension:
            if message.content.endswith(i):
                flag = False
                if await self.returnimage(
                        self.RandomImageProcesser.getRandomImage, message):
                    return
                else:
                    if await self.returnimage(
                            self.RandomImageProcesser.imageJson.getimg,
                            message):
                        return


async def setup(bot: commands.Bot):
    await bot.add_cog(ImageManager(bot))
