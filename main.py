import asyncio
import os
import math
import statistics

import discord
from discord_ext_help.help import extension as helpext

import config
from lib.error import handler
from lib.logger import log
from lib.LithumBot import LithumBot

bot = LithumBot(command_prefix="/sln ", intents=discord.Intents.all())
deh = helpext(bot)
logger = log().getlogger()

@bot.event
async def setup_hook():
    bot.load_translation("./translations")
    await bot.load_extension("jishaku")
    for file in os.listdir("./src"):
        if os.path.isfile(os.path.join("./src", file)):
            if file.endswith(".py"):
                await bot.load_extension(f"src.{file[:-3]}")
                logger.info("loaded extension: " + f"src.{file[:-3]}")
    command = await bot.tree.sync()
    await deh.regist_ids(command)


@bot.tree.command(name="help", description="コマンド一覧を表示します")
async def help(interaction: discord.Interaction):
    await interaction.response.defer()
    await deh.generate(interaction)


@bot.tree.error
async def on_error(
    interaction: discord.Interaction, error: discord.app_commands.AppCommandError
) -> None:
    await handler(bot=bot, interaction=interaction, error=error)


@bot.event
async def on_ready():
    deh.config["embed_title"] = "{}のコマンド一覧".format(bot.user.name)
    deh.config["description_not_found"] = "このコマンドの説明はありません。"
    deh.config["description_not_found_group"] = (
        "このコマンドグループの説明はありません。"
    )
    logger.info("logged in: {}".format(bot.user.name))
    while True:
        servers = str("{:,}".format(int(len(bot.guilds))))
        await bot.change_presence(
            activity=discord.Activity(
                name="/help | {} servers".format(servers),
                type=discord.ActivityType.playing,
            ),
            status=discord.Status.dnd,
        )
        await asyncio.sleep(15)
        servers = str("{:,}".format(int(len(bot.guilds))))
        users = str("{:,}".format(int(len(bot.users))))
        await bot.change_presence(
            activity=discord.Activity(
                name="{} servers | {} users".format(servers, users),
                type=discord.ActivityType.playing,
            ),
            status=discord.Status.dnd,
        )
        pings = []
        for i in range(15):
            raw = bot.latency
            ping = round(raw * 1000)
            pings.append(ping)
            await asyncio.sleep(1)
        users = str("{:,}".format(int(len(bot.users))))
        ping = str(math.floor(statistics.mean(pings)))
        await bot.change_presence(
            activity=discord.Activity(
                name="{} users | ping: {}ms".format(users, ping),
                type=discord.ActivityType.playing,
            ),
            status=discord.Status.dnd,
        )
        await asyncio.sleep(15)


bot.run(config.token)
