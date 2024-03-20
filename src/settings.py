import discord
from discord import app_commands
from discord.ext import commands
from motor.core import AgnosticClient

from lib.db import MongoDB
from lib.LithumBot import LithumBot
from lib.views import edit_lang


class user_setting(commands.GroupCog, name="user-settings"):
    def __init__(self, bot: LithumBot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
        self.client: AgnosticClient = MongoDB().getdb("localhost", 27017)
        self.db = self.client.lithum
        self.userData = self.db.userData

    @app_commands.command(name="lang", description="Botの言語を変更します。")
    @app_commands.checks.cooldown(2, 60)
    async def set_lang(self, interaction: discord.Interaction):
        v = edit_lang(
            bot=self.bot, user=interaction.user, userData=self.userData, timeout=None
        )
        await interaction.response.send_message(view=v)


async def setup(bot: commands.Bot):
    await bot.add_cog(user_setting(bot))
