from discord.ext import commands
import discord,logging
from typing import Optional


admin=[1144650057132540046,573818863419129876]
# 定義名為 lkkCog 的 Cog
class lkkCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger:logging.Logger=None

    def is_admin(self,ctx:Optional[commands.Context]=None,Interaction:Optional[discord.Interaction]=None):
        if ctx:
            for i in admin:
                role = discord.utils.get(ctx.guild.roles, id=i) # Get the role
                if role in ctx.author.roles: # Check if the author has the role
                    self.logger.info(f"{ctx.author.name}通過了是否為管理員檢查。")
                    return True
        elif Interaction:
            for i in admin:
                role = discord.utils.get(Interaction.guild.roles, id=i)
                if role in Interaction.user.roles:
                    self.logger.info(f"{Interaction.user.name}通過了是否為管理員檢查。")
                    return True
        self.logger.info(f"{Interaction.user.name}未能通過管理員檢查。")
        return False
