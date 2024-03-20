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
    @app_commands.describe(lang="bot language")
    @app_commands.choices(
        lang=[
            app_commands.Choice(name="日本語", value="ja_JP"),
            app_commands.Choice(name="English (American)", value="en_US"),
        ]
    )
    async def set_lang(self, interaction: discord.Interaction, lang: app_commands.Choice[str]):
        await interaction.response.defer()
        udata = await self.userData.find_one({"userId": interaction.user.id})
        if udata is None:
            udata = {
                "userId": interaction.user.id,
                "bot": {"lang": lang.value},
            }
            await self.userData.insert_one(udata)
        else:
            await self.userData.update_one(
                {"userId": interaction.user.id},
                {"$set": {"bot": {"lang": lang.value}}},
            )
            udata["bot"]["lang"] = lang.value
        embed = discord.Embed(
            title=self.bot.translation.getText(
                text="success", lang=udata["bot"]["lang"]
            ),
            description=self.bot.translation.getText(
                text="Changed bot language to _{}.",
                lang=udata["bot"]["lang"],
            ).replace("_{}", lang.name),
            color=discord.Colour.green()
        )
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(user_setting(bot))
