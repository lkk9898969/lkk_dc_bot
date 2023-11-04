import discord,json
from discord.ext import commands
from core.lkkcog import lkkCog
from core.log import loggerhandler
from typing import Optional
import random
random.seed()

admincommand=[["updateimg","\{觸發名.副檔名\} \{超連結\}","用於新增新圖片，副檔名只支持 .jpg 或 .gif。",
        "此為1對1(1個關鍵字對應1個圖片)，若關鍵字已經被新增過的，原本的連結會直接被蓋掉，所以使用之前最好查一下關鍵字有沒有被新增過了。"],
        ["updaterandom","\{圖片庫觸發名.副檔名\} \{隨機觸發名\}","用於新增隨機觸發，此為主要的觸發方式。\n注意:隨機觸發名**｢不用｣**副檔名。",
        "此為1對多(1個隨機關鍵字對應多個圖片觸發名)，不會覆蓋掉之前已經存在過的圖片觸發名。另外沒有刪除方法，要刪除請用/apply_to或私訊告知我(湯麵)"],
        ["updateword","\{隨機觸發名\} \{*多個關聯字\}",
        "新增關聯字。關聯字會觸發 隨機觸發名 的圖片。簡單來說會將關聯字直接替換成隨機觸發名去調用隨機圖片庫。",
        "此為多對多(1個隨機觸發名可以關聯多個關聯字、1個關聯字也可以被多個隨機觸發名關聯)。若想更加了解我在打啥可以問我(湯麵)。"]]
command=[["老王語錄","\{語錄\}","用於新增老王語錄","無"]]
scolds=["不要再妄想你是管理員了!","麻煩不要太自戀好嗎?",
        "你484看不懂中文?","權限沒有這麼好拿，同學。",
        "你以為你誰啊?","笑死。","你如果覺得我很嗆就不該亂用這個指令!"]

class CommandCogs(lkkCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        logname="command"
        self.logger=loggerhandler("lkkdc."+logname,logname)

    @commands.Cog.listener()
    async def on_ready(self):
        self.__owner = await self.bot.fetch_user(410712052655456267)
        self.logger.info(f"extension {__name__}載入完成。")

    @commands.command()
    @commands.is_owner()
    async def refresh(self,ctx:commands.Context):
        await ctx.invoke(self.bot.get_command('refreshr'))
        await ctx.invoke(self.bot.get_command('refreshq'))

    @discord.app_commands.command(name='help',description='湯麵機器人指令列表')
    async def helpc(self,interaction:discord.Interaction):
        try:
            slash=self.bot.tree.get_commands(type=discord.AppCommandType.chat_input)
            slashcommands=[i.name for i in slash]
            result='斜線指令:\n'
            for i in slashcommands:
                result+=i+'\n'
            result+='斜線指令詳情請在<#470227564577947658>使用{/指令名稱}查看。\n'
            result="一般指令:\n    輸入指令時\{\}請忽略，那只是在告訴你那是個參數。\n"
            for i in command:
                result+=f"${i[0]}\n格式: ${i[0]} {i[1]}\n功能:{i[2]}\n附註:{i[3]}\n"
            await interaction.response.send_message(result,ephemeral=True)
            self.logger.info(f"{interaction.user.name}查看了一般人用的指令表。")
        except:
            self.logger.error('',exc_info=True)

    @discord.app_commands.command(name="help_admin",description="(管理員用) 查詢指令用法")
    @discord.app_commands.describe(command_name="指定的指令，可空白。")
    async def adminhelp(self,interaction:discord.Interaction,command_name:Optional[str]):
        if self.is_admin(Interaction=interaction):
            try:
                result="可用指令:\n    輸入指令時\{\}請忽略，那只是在告訴你那是個參數。\n"
                if command_name:
                    for i in admincommand:
                        if i[0] in command_name:
                            result+=f"${i[0]}\n格式: ${i[0]} {i[1]}\n功能:{i[2]}\n附註:{i[3]}\n"
                            break
                else:
                    for i in admincommand:
                        result+=f"${i[0]}\n格式: ${i[0]} {i[1]}\n功能:{i[2]}\n附註:{i[3]}\n"
                await interaction.response.send_message(result,ephemeral=True)
                self.logger.info(f"{interaction.user.name}查看了管理員用的指令表。")
            except:
                self.logger.error("",exc_info=True)
        else:
            await interaction.response.send_message(f"這個指令只有管理員才能使用! {random.choice(scolds)}",delete_after=5)
            self.logger.info(f"{interaction.user.name}嘗試查看指令表但被機器人嘲笑了一番。")

    @discord.app_commands.command(name="apply_to",description="申請新增觸發圖檔，經過我(湯麵)審核後再行更新。")
    @discord.app_commands.describe(filename="觸發名稱，例如 吃披薩.gif",url="圖檔的URL連結。")
    async def apply(self,interaction: discord.Interaction,filename : str, url: str):
        if (url.startswith("http")):
            json.dump({filename : url},open("image_apply.json",'a',encoding='utf-8'),ensure_ascii=False)
            with open("image_apply.json",'a',encoding='utf-8') as f:
                f.write('\n')
            await interaction.response.send_message("已申請。")
            await self.__owner.send(content=f"{interaction.user.name}申請了圖片，觸發名{filename}，圖片網址{url}")
            self.logger.info(f"{interaction.user.name}申請了圖片，觸發名{filename}")

    
    @discord.app_commands.command(name="link_help",description="教您如何將您的 WOWS帳號 與 DC水表機器人 連結。")
    async def link_help1(self,interaction: discord.Interaction):
        await interaction.response.send_message("https://media.discordapp.net/attachments/631827617938538508/1160935048485273600/2023-10-09_214118.png?ex=65367804&is=65240304&hm=aacab01c8b60c690bccb944aaba808ddf57e92b1a7fc031ceb17c04bccb60f08&=&width=575&height=552",ephemeral=True)
    @commands.command()
    async def link_help(self,ctx : commands.Context):
        await ctx.reply("https://media.discordapp.net/attachments/631827617938538508/1160935048485273600/2023-10-09_214118.png?ex=65367804&is=65240304&hm=aacab01c8b60c690bccb944aaba808ddf57e92b1a7fc031ceb17c04bccb60f08&=&width=575&height=552")



    # 關鍵字觸發
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.channel.id==860390159114960936:
            if message.content.find("ISAC stopped tracking your account") != -1:
                try:
                    usermessage=await message.channel.get_partial_message(message.reference.message_id).fetch()
                    await usermessage.reply("您超過14天未使用.recent指令，所以水表機器人停止追蹤您的戰績了。請定期在14天內至少使用一次.recent指令。")
                    self.logger.info(f"提醒了{usermessage.author.name} 應於期間內重複使用.recent指令。")
                except:
                    self.logger.error("",exc_info=True)
            elif message.content.find("haven't linked") != -1:
                try:
                    usermessage=await message.channel.get_partial_message(message.reference.message_id).fetch()
                    try:
                        await usermessage.reply(f"{usermessage.mentions[0].mention}尚未link。\n使用/link 你的ID\n將你的DC與窩窩使帳號連結。\n如需更詳細的說明請輸入 /link_help 或 $link_help 。")
                    except IndexError:
                        await usermessage.reply(f"您尚未link。\n使用/link 你的ID\n將你的DC與窩窩使帳號連結。\n如需更詳細的說明請輸入 /link_help 或 $link_help 。")
                    self.logger.info(f"提醒了{usermessage.author.name} 如何使用link。")
                except:
                    self.logger.error("",exc_info=True)
            elif message.content.find("Successfully linked with") != -1:
                try:
                    interaction = message.interaction
                    await message.channel.send(f"<@{interaction.user.id}>您已經連結成功! 有以下注意事項 : \n"+
                                               "1. 水表機器人從現在開始才會記錄您的戰績，所以使用.recent me卻查不到戰績屬於正常。\n"+
                                               "2. 若太久(14天)未使用.recent me指令，機器人將會停止追蹤您的戰績。")
                    self.logger.info(f"提醒了{interaction.user.name} link後注意事項。")
                except:
                    self.logger.error("",exc_info=True)
            elif message.content.find("wasn't in the database") != -1:
                try:
                    usermessage=await message.channel.get_partial_message(message.reference.message_id).fetch()
                    result=usermessage.content.split('`')[1]
                    await usermessage.reply(f"此WG帳號`{result}`尚未被link，因此水表機器人沒有追蹤此帳號的戰績。")
                    self.logger.info(f"提醒了{usermessage.author.name}，{result}該帳號並未被link過因此沒有近期戰績。")
                except:
                    self.logger.error("",exc_info=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(CommandCogs(bot))