import discord, logging
from discord import app_commands
from discord.ext import commands
from typing import Optional

ADMIN = [1144650057132540046, 573818863419129876]


# 定義名為 lkkCog 的 Cog
class lkkCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger: logging.Logger = None

    def is_admin(self,
                 ctx: Optional[commands.Context] = None,
                 Interaction: Optional[discord.Interaction] = None):
        if ctx:
            for i in ADMIN:
                role = discord.utils.get(ctx.guild.roles, id=i)  # Get the role
                if role in ctx.author.roles:  # Check if the author has the role
                    self.logger.info(f"{ctx.author.name}通過了是否為管理員檢查。")
                    return True
        elif Interaction:
            for i in ADMIN:
                role = discord.utils.get(Interaction.guild.roles, id=i)
                if role in Interaction.user.roles:
                    self.logger.info(f"{Interaction.user.name}通過了是否為管理員檢查。")
                    return True
        self.logger.info(f"{Interaction.user.name}未能通過管理員檢查。")
        return False

    def is_admin_check_decorator(self):

        def predicate(Interaction: discord.Interaction):
            for i in ADMIN:
                role = discord.utils.get(Interaction.guild.roles, id=i)
                if role in Interaction.user.roles:
                    self.logger.info(f"{Interaction.user.name}通過了是否為管理員檢查。")
                    return True
            return False

        return app_commands.check(predicate)


def is_admin_check(Interaction: discord.Interaction):
    for i in ADMIN:
        role = discord.utils.get(Interaction.guild.roles, id=i)
        if role in Interaction.user.roles:
            return True
    return False


def is_admin_check_decorator():
    return app_commands.check(is_admin_check)
