import discord
import time
from discord import app_commands
from discord.ext import commands
from core.lkk_log import loggerhandler
from core.lkkcog import lkkCog, is_admin_check
from core.Quotes import Quotes
from typing import Optional

quotesfile = "quotes.json"


class QuotesManager(lkkCog):

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        logname = "QuotesManager"
        self.logger = loggerhandler("lkkdc." + logname,
                                    logname + time.strftime("-%Y%m%d"),
                                    cwd="log",
                                    logfile_level="DEBUG",
                                    attachConsole=False)
        self.quotes = Quotes(self.logger, quotesfile)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"extension {__name__}載入完成。")

    def __addQuote(self, name, data):
        try:
            if self.quotes.checkNameStrict(name):
                if self.quotes.addQuote(name, data):
                    self.logger.info(f"{name}新增語錄成功。")
                    return 0

                self.logger.info(f"{name}新增語錄時失敗。原因:該語錄已存在。")
                return 1

            self.logger.info(f"{name}新增語錄時失敗。原因:該語錄分類不存在。")
            return 2
        except:
            self.logger.error(f"{name}新增語錄失敗。", exc_info=True)
            return -1

    async def _add_c_wong(self,
                          data: str,
                          ctx: commands.Context = None,
                          interaction: discord.Interaction = None):
        if ctx is None and interaction is None:
            return
        if ctx is not None:
            author = ctx.author.name
            reply = ctx.reply
        else:
            author = interaction.user.name
            reply = lambda x: interaction.response.send_message(x,
                                                                ephemeral=True)

        if self.__addQuote('老王語錄', data) == 0:
            await reply("新增成功!")
            self.logger.info(f"{author}新增了老王語錄。")
        elif self.__addQuote('老王語錄', data) == 1:
            await reply("新增失敗! 該語錄已存在。")
        else:
            await reply("新增失敗! 原因請請教湯麵")
            self.logger.info(f"{author}新增老王語錄時因未知原因導致新增失敗。")

    async def _updateQuoteWords(self,
                                mainword: str,
                                *words: str,
                                ctx: commands.Context = None,
                                interaction: discord.Interaction = None):
        if ctx is None and interaction is None:
            return
        if ctx is not None:
            reply = ctx.reply
        else:
            reply = lambda x: interaction.response.send_message(x,
                                                                ephemeral=True)

        if words:
            for i in words:
                if not self.quotes.addRelated(mainword, i):
                    await reply(f"關聯字{i}已存在於{mainword}關聯字中。")
                    self.logger.info(
                        f"{ctx.author.name}嘗試新增關聯字{i}到{mainword}但關聯字已存在。")
            await reply(f"新增成功!")
        else:
            await reply("請輸入至少1個關聯字!")
            self.logger.info(f"{ctx.author.name}嘗試新增關聯字但未給定關聯字。")

    async def quoteNameAutoComplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        name = self.quotes.listName()
        self.logger.debug(f"name: {name}")
        if current:
            return [
                app_commands.Choice(name=i, value=i) for i in name
                if current.lower() in i.lower()
            ]
        else:
            return [app_commands.Choice(name=i, value=i) for i in name]

    async def quoteIndexAutoComplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        try:
            selectedName = str(interaction.namespace["name"])
        except KeyError:
            return []

        if self.quotes.checkNameStrict(selectedName):
            quoteList = self.quotes.getQuoteList(selectedName)
            if current:
                return [
                    app_commands.Choice(name=i, value=i)
                    for i in range(len(quoteList))
                    if current.lower() in str(i).lower()
                ]
            else:
                return [
                    app_commands.Choice(name=i, value=i)
                    for i in range(len(quoteList))
                ]
        else:
            return []

    @app_commands.command(name='quotes_search',
                          description="查找語錄，請給定語錄分類名稱與語錄順位。")
    @app_commands.describe(name="想要查找的語錄分類名稱。", index="第幾個語錄。")
    @app_commands.autocomplete(name=quoteNameAutoComplete,
                               index=quoteIndexAutoComplete)
    async def quotes_search(self, interaction: discord.Interaction, name: str,
                            index: int):
        try:
            if self.quotes.checkNameStrict(name):
                quote = self.quotes.getQuote(name, index)
                if quote:
                    await interaction.response.send_message(quote,
                                                            ephemeral=True)
                    self.logger.info(f"向{interaction.user.name}回傳了{quote}")
                    return
                await interaction.response.send_message("超出範圍!",
                                                        ephemeral=True)
                self.logger.info(
                    f"{interaction.user.name}嘗試查找{name}語錄時給定的位置超出範圍。")
            else:
                await interaction.response.send_message("該語錄分類不存在。",
                                                        ephemeral=True)
                self.logger.info(f"{interaction.user.name}嘗試查找一個不存在的語錄分類。")
        except:
            self.logger.error('', exc_info=True)

    @commands.command(name='updateQuoteWords', aliases=['uqw', 'UQW'])
    async def updateQuoteWords(self, ctx: commands.Context, mainword: str,
                               *words: str):
        if self.is_admin(ctx):
            self.logger.info(f"{ctx.author.name}使用了updatequotesword指令。")
            await self._updateQuoteWords(mainword, *words, ctx=ctx)

    # @app_commands.command(name='update_quote_word', description="更新語錄名稱關聯字。")
    # @app_commands.describe(mainword="語錄分類名稱", word="要新增的關聯字")
    # @app_commands.check(is_admin_check)
    # async def update_quote_words(self, interaction: discord.Interaction,
    #                              mainword: str, word: str):
    #     self.logger.info(f"{interaction.user.name}使用了update_quote_words指令。")
    #     await self._updateQuoteWords(mainword, word, interaction=interaction)

    @commands.command()
    @commands.is_owner()
    async def refreshq(self, ctx: commands.Context):
        self.quotes.refresh()
        await ctx.reply("quotes刷新完成。")

    @commands.command(name='老王語錄')
    async def add_C_WONG_QuoteCmd(self, ctx: commands.Context, data: str):
        self.logger.info(f"{ctx.author.name}使用了老王語錄指令。")
        await self._add_c_wong(data, ctx=ctx)

    @app_commands.command(name='c_wong', description="新增老王語錄")
    @app_commands.describe(data="請將語錄輸入於此。")
    async def add_C_WONG_QuoteApp(self, interaction: discord.Interaction,
                                  data: str):
        self.logger.info(f"{interaction.user.name}使用了c_wong指令。")
        await self._add_c_wong(data, interaction=interaction)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        result = self.quotes.getQuote(message.content)
        if result:
            await message.reply(content=result)
            self.logger.info(f"向#{message.channel.name}回傳了語錄。")
            return

        temp = message.content.replace(" ", "")
        digit = ''.join(filter(str.isdigit, temp))
        if digit == '':
            return
        else:
            digit = int(digit)

        temp = temp.replace(str(digit), "")
        if self.quotes.checkName(temp):
            result = self.quotes.getQuote(temp, digit - 1)
            if result:
                await message.reply(content=result)
                self.logger.info(
                    f"向#{message.channel.name}回傳了指定順位的語錄。順位:{digit}")
                return
            else:
                await message.reply(content="指定順位超出範圍!", delete_after=5)
                self.logger.info(
                    f"{message.author.name}嘗試查找{temp}語錄時給定的位置超出範圍。")


async def setup(bot: commands.Bot):
    await bot.add_cog(QuotesManager(bot))
