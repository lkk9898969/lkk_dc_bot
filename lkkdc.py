import discord, asyncio, json, time
from aioconsole import ainput as input_async
from pathlib import Path
from discord.ext import commands
from lkk_log import loggerhandler

cogs = "cogs"
botjson = "lkk.json"


class lkkdc(commands.Bot):

    def __init__(self, owner_id: int):
        intents = discord.Intents.default()
        intents.message_content = True
        activity = discord.Activity(
            type=discord.ActivityType.custom, name="custom", state="打/看指令表"
        )
        super().__init__(command_prefix="$", intents=intents, activity=activity)
        self.owner_id = owner_id

    async def setup_hook(self) -> None:
        await self.load_extensions()
        slash = await self.tree.sync()
        logger.info(f"載入 {len(slash)} 個斜線指令")

    # 當機器人完成啟動時
    async def on_ready(self):
        logger.info(f"目前登入身份 --> {self.user}")

    # 一開始bot開機需載入全部程式檔案
    async def load_extensions(self):
        p = Path(".")
        for file in list(p.glob(f"./{cogs}/*.py")):
            cog = f"{cogs}.{file.name[:-3]}"
            logger.info(f"載入{cog}。")
            await self.load_extension(cog)


def init():
    global logger, data
    logname = "lkkdc"
    logger = loggerhandler(
        "", logname + time.strftime("-%Y%m%d"), cwd="log", logfile_level="DEBUG"
    )

    with open(botjson, "r", encoding="utf-8") as file:
        data = json.load(file)
    logger.info(f"載入資料成功，持有者ID={data['OWNER_ID']}")


async def clicmd_list(cmd: str, **kwargs):
    match cmd.lower():
        case "stop" | "exit":
            logger.info("Stop bot.")
            await kwargs["bot"].close()
            exit(0)


async def main():
    bot = lkkdc(int(data["OWNER_ID"]))
    asyncio.create_task(bot.start(data["TOKEN"]))
    while True:
        inputs = str(await input_async())
        logger.info(inputs)
        cmd = bot.get_command(inputs)
        if cmd:
            await bot.invoke(cmd)
        elif await clicmd_list(inputs, bot=bot):
            pass
        else:
            logger.error(f"{inputs} command not found!")


# 確定執行此py檔才會執行
if __name__ == "__main__":
    init()
    asyncio.run(main())
    logger.info("on_disconnect")
