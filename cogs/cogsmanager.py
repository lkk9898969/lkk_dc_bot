from discord.ext import commands
from core.lkkcog import lkkCog
from core.lkk_log import loggerhandler
from pathlib import Path
import importlib

cogs="cogs"
_core="core"



class cogsmanager(lkkCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        logname="cogsmanager"
        self.logger=loggerhandler("lkkdc."+logname,logname,consoleattach=False)

    def modulereload(self):
        p=Path(".")
        coremodule=[f"{_core}.{i.name[:-3]}" for i in list(p.glob(f"./{_core}/*.py"))]
        result=[importlib.import_module(i) for i in coremodule]
        for i in result:
            self.logger.info(f'模組{i.__name__}將重新載入。')
            importlib.reload(i)

    async def slashreload(self):
        slash=await self.bot.tree.sync()
        return len(slash)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"extension {__name__}載入完成。")

    # 載入指令程式檔案
    @commands.command()
    @commands.is_owner() # 管理者才能使用
    async def load(self, ctx:commands.Context, extension):
        self.logger.info(f'嘗試載入{extension}。')
        try:
            await self.bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} 已載入。')
            self.logger.info(f'{extension} 已載入。')
        except:
            self.logger.error("",exc_info=True)

    # 卸載指令檔案
    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx:commands.Context, extension):
        self.logger.info(f'嘗試卸載{extension}。')
        try:
            await self.bot.unload_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} 已卸載。')
            self.logger.info(f'{extension} 已卸載。')
        except:
            self.logger.error("",exc_info=True)

    # 重新載入程式檔案
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx:commands.Context, extension):
        # 如果直接更改程式碼的話就直接reload
        self.logger.info(f'嘗試更新{extension}。')
        try:
            self.logger.info('重新載入模組。')
            self.modulereload()
            self.logger.info('重新載入slash指令。')
            self.logger.info(f'已重新載入{await self.slashreload()}個指令。')
            await self.bot.reload_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} 已更新。')
            self.logger.info(f'{extension} 已更新。')
        except:
            self.logger.error("",exc_info=True)
        

async def setup(bot:commands.Bot):
    await bot.add_cog(cogsmanager(bot))