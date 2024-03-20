import asyncio
from time import time

import discord
from discord.ext import commands
from motor.core import AgnosticClient

from lib.db import MongoDB
from lib.LithumBot import LithumBot


class bump(commands.Cog, name="bump"):
    def __init__(self, bot: LithumBot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
        self.client: AgnosticClient = MongoDB().getdb("localhost", 27017)
        self.db = self.client.lithum
        self.guildData = self.db.guildData

    async def bump_notify(self, channel, lang="ja"):
        if lang == "en":
            embed = discord.Embed(
                title="bump notification",
                description="It is time to bump!\n</bump:947088344167366698> to increase the server's ranking!",
                color=discord.Colour.blue(),
            )
            await channel.send(embed=embed)
            return
        embed = discord.Embed(
            title="bump通知",
            description="bumpの時間です！\n</bump:947088344167366698>を実行してサーバーの順位を上げましょう！",
            color=discord.Colour.blue(),
        )
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        settings = await self.guildData.find_one({"guildId": message.guild.id})
        settings = {"bump": {"enable": True}, "up": {"enable": True}}
        if message.author.id == 302050872383242240 and message.embeds[0].description:
            if message.embeds[0].description.find("表示順をアップしたよ") != -1:
                if settings["bump"]["enable"]:
                    bumptime = time() + 7200
                    embed = discord.Embed(
                        title="bumpを検知",
                        description=f"bumpを検知しました。\n<t:{str(int(bumptime))}:R>に通知します。",
                        color=discord.Colour.blue(),
                    )
                    await message.channel.send(embed=embed)
                    await asyncio.sleep(7200)
                    await self.bump_notify(message.channel)
            elif message.embeds[0].description.find("Bump done") != -1:
                if settings["bump"]["enable"]:
                    bumptime = time() + 3600
                    embed = discord.Embed(
                        title="bump is detected.",
                        description=f"Notify after <t:{str(int(bumptime))}:R>.",
                        color=discord.Colour.blurple(),
                    )
                    await message.channel.send(embed=embed)
                    await asyncio.sleep(3600)
                    await self.dissoku_up_Notify(message.channel, lang="en")

async def setup(bot: commands.Bot):
    await bot.add_cog(bump(bot))
