import discord
from discord import app_commands
from discord.ext import commands
from core.log import loggerhandler
from core.lkkcog import lkkCog
from core.quotes import quotes
from core.relationword import relationword
from typing import Optional

quotesfile="quotes.json"

class quotesmanager(lkkCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        logname="quotes_manager"
        self.logger=loggerhandler("lkkdc."+logname,logname)
        self.quotes=quotes(self.logger,quotesfile)
        self.relationword=relationword(self.logger,"quotes_relationword.json")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"extension {__name__}載入完成。")

    def __adddquotes(self,index,data):
        try:
            if self.quotes.addquotes(index,data):
                self.logger.info(f"{index}新增了語錄{data}")
                return 0
            else:
                self.logger.info(f"{index}新增語錄{data}時失敗。原因:該語錄已存在。")
                return 1
        except:
            self.logger.error(f"{index}新增語錄失敗。",exc_info=True)
            return False

    async def quotes_autocomplete(self,interaction: discord.Interaction,current: str,) -> list[app_commands.Choice[str]]:
        index = self.quotes.listindex()
        if current:
            return [app_commands.Choice(name=j, value=i) for i,j in enumerate(index) if current.lower() in j.lower()]
        else:
            return [app_commands.Choice(name=j, value=i) for i,j in enumerate(index)]

    @commands.command(name='uqw')
    async def updatequotesword(self,ctx:commands.Context,mainword:str,*words:str):
        if self.is_admin(ctx):
            try:
                if words:
                    for i in words:
                        self.relationword.addrelationword(mainword,i)
                    await ctx.reply(f"新增成功!")
                else:
                    await ctx.reply("請輸入至少1個關聯字!")
                    self.logger.info(f"{ctx.author.name}嘗試新增關聯字但未給定關聯字。")
            except:
                self.logger.error("",exc_info=True)

    @commands.command()
    @commands.is_owner()
    async def refreshq(self,ctx:commands.Context):
        self.quotes.refresh()
        await ctx.reply("quotes刷新完成。")

    @commands.command(name='老王語錄')
    async def C_WONG_adddquote1(self,ctx:commands.Context,data:str):
        index='老王語錄'
        if (result:=self.__adddquotes(index,data))==0:
            await ctx.reply("新增成功!")
        elif result==1:
            await ctx.reply("新增失敗! 該語錄已存在。")
        else:
            await ctx.reply("新增失敗! 原因請請教湯麵")
        
    
    @app_commands.command(name='c_wong',description="新增老王語錄")
    @app_commands.describe(data="請將語錄輸入於此。")
    async def C_WONG_adddquote2(self,interaction: discord.Interaction,data:str):
        index='老王語錄'
        if (result:=self.__adddquotes(index,data))==0:
            await interaction.response.send_message("新增成功!",ephemeral=True)
        elif result==1:
            await interaction.response.send_message("新增失敗! 該語錄已存在。",ephemeral=True)
        else:
            await interaction.response.send_message("新增失敗! 原因請請教湯麵",ephemeral=True)

    @app_commands.command(name='quotes_search',description="查找語錄")
    @app_commands.describe(index="選取想要查找的語錄。")
    @app_commands.autocomplete(index=quotes_autocomplete)
    async def quotes_search(self,interaction: discord.Interaction,index:int):
        qindex=self.quotes.listindex()
        try:
            result=self.quotes.listquotes(qindex[index])
            if result:
                await interaction.response.send_message(result,ephemeral=True)
                self.logger.info(f"向{interaction.user.name}回傳了{qindex[index]}")
            else:
                await interaction.response.send_message("該語錄不存在。",ephemeral=True)
        except:
            self.logger.error('',exc_info=True)
        pass

    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        for i in self.quotes.listindex():
            if message.content==i:
                await message.reply(content=self.quotes.getquotes(i))
                self.logger.info(f"向#{message.channel.name}回傳了老王語錄。")
                return
        if result:=self.relationword.getrelationword(message.content):
            await message.reply(content=self.quotes.getquotes(result))
            self.logger.info(f"向#{message.channel.name}回傳了老王語錄。")
            return
    

async def setup(bot:commands.Bot):
    await bot.add_cog(quotesmanager(bot))