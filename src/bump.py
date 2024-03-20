import asyncio
from time import time

import discord
from discord.ext import commands
from motor.core import AgnosticClient
import orjson

from lib.db import MongoDB
from lib.LithumBot import LithumBot


class user_setting(commands.Cog, name="user-setting"):
    def __init__(self, bot: LithumBot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
        self.client: AgnosticClient = MongoDB().getdb("localhost", 27017)
        self.db = self.client.lithum
        self.guildData = self.db.guildData
        self.up_servers = {}

    async def dissoku_up_Notify(self, channel, lang="ja"):
        if lang == "en":
            embed = discord.Embed(
                title="up notification",
                description="It is time to UP!\n</dissoku up:828002256690610256> to increase the server's ranking!",
                color=discord.Colour.blue(),
            )
            await channel.send(embed=embed)
            return
        embed = discord.Embed(
            title="up通知",
            description="upの時間です！\n</dissoku up:828002256690610256>を実行してサーバーの順位を上げましょう！",
            color=discord.Colour.blue(),
        )
        await channel.send(embed=embed)

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
    async def on_message_edit(self, messsage_before: discord.Message, message: discord.Message):
        settings = await self.guildData.find_one({"guildId": message.guild.id})
        settings = {"bump": {"enable": True}, "up": {"enable": True}}
        if message.author.id == 761562078095867916:
            self.up_servers[str(message.guild.id)] = True
            with open("./dissoku/up_emb.json", "w", encoding="utf-8") as f:
                f.write(orjson.dumps(message.embeds[0].to_dict()).decode("utf-8"))
            if "をアップしたよ" in message.embeds[0].fields[0].name:
                if settings["up"]["enable"]:
                    bumptime = time() + 3600
                    embed = discord.Embed(
                        title="upを検知",
                        description=f"upを検知しました。\n<t:{str(int(bumptime))}:R>に通知します。",
                        color=discord.Colour.blurple(),
                    )
                    await message.channel.send(embed=embed)
                    await asyncio.sleep(3600)
                    await self.dissoku_up_Notify(message.channel)
                    self.up_servers.pop(str(message.guild.id))
            elif "I've bumped up" in message.embeds[0].fields[0].name:
                self.up_servers[str(message.guild.id)] = True
                if settings["up"]["enable"]:
                    bumptime = time() + 3600
                    embed = discord.Embed(
                        title="up is detected.",
                        description=f"Notify after <t:{str(int(bumptime))}:R>.",
                        color=discord.Colour.blurple(),
                    )
                    await message.channel.send(embed=embed)
                    await asyncio.sleep(3600)
                    await self.dissoku_up_Notify(message.channel, lang="en")
                    self.up_servers.pop(str(message.guild.id))

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
    await bot.add_cog(user_setting(bot))
