import math

# import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

# import orjson as json
from reactionmenu import ViewButton, ViewMenu

from lib.db import MongoDB
from lib.func import VERIFICATIONLEVEL, UserFlags
from lib.LithumBot import LithumBot

cd = 4
yn = {"True": "Yes", "False": "No"}


class utils(commands.GroupCog, name="tools"):
    def __init__(self, bot: LithumBot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
        self.client = MongoDB().getdb("localhost", 27017)
        self.db = self.client.lithum
        self.userData = self.db.userData

    @app_commands.command(name="guild", description="サーバーの情報を取得します。")
    @app_commands.checks.cooldown(5, 30)
    async def guild(self, interaction: discord.Interaction, guild_id: str):
        udata = await self.userData.find_one({"userId": interaction.user.id})
        if udata is None:
            udata = {
                "userId": interaction.user.id,
                "bot": {"lang": "ja"},
            }  # ダミーデータ生成
            await self.userData.insert_one(udata)
        await interaction.response.defer()
        acolor = discord.Color.blue()

        try:
            guild: discord.Guild = self.bot.get_guild(int(guild_id))
        except discord.NotFound:
            embed = discord.Embed(
                title="404 Not Found",
                description=self.bot.translation.getText(
                    'Guild "_{}" not found, please check if Bot is added.',
                    lang=udata["bot"]["lang"],
                ).replace("_{}", guild_id),
            )
            await interaction.followup.send(embed=embed)
            return
        title = self.bot.translation.getText(
            "_{}'s information", lang=udata["bot"]["lang"]
        ).replace("_{}", guild.name)
        embed = discord.Embed(title=title, color=acolor)

        users = guild.member_count
        member_count = str(users) + self.bot.translation.getText(
            text=" users", lang=udata["bot"]["lang"]
        )
        if users is None:
            member_count = self.bot.translation.getText(
                text="Failed to get member count", lang=udata["bot"]["lang"]
            )
        discriminator = ""
        owner = self.bot.translation.getText(text="unknown", lang=udata["bot"]["lang"])
        owner_id = ""
        guild_owner = await self.bot.fetch_user(guild.owner_id)
        if guild.owner_id is not None:
            owner = guild_owner.name
            owner_id = " (ID:" + str(guild.owner_id) + ")"
            if guild_owner.discriminator is not None:
                if not guild_owner.discriminator == "0":
                    discriminator = "#" + guild_owner.discriminator
        embed.add_field(
            name=self.bot.translation.getText(
                text="Guild Owner", lang=udata["bot"]["lang"]
            ),
            value=owner + discriminator + owner_id,
        )

        embed.add_field(
            name=self.bot.translation.getText(
                text="member count", lang=udata["bot"]["lang"]
            ),
            value=member_count,
            inline=True,
        )
        embed.add_field(
            name=self.bot.translation.getText(
                text="Verification Level", lang=udata["bot"]["lang"]
            ),
            value=self.bot.translation.getText(
                text=VERIFICATIONLEVEL[guild.verification_level],
                lang=udata["bot"]["lang"],
            ),
            inline=False,
        )
        embed.add_field(
            name=self.bot.translation.getText(
                text="Boost Level", lang=udata["bot"]["lang"]
            ),
            value=self.bot.translation.getText(text="level ", lang=udata["bot"]["lang"])
            + str(guild.premium_tier),
            inline=True,
        )
        embed.add_field(
            name=self.bot.translation.getText(
                text="Boost Count", lang=udata["bot"]["lang"]
            ),
            value=str(guild.premium_subscription_count),
            inline=True,
        )

        times = guild.created_at.timestamp()
        embed.add_field(
            name=self.bot.translation.getText(
                text="created at", lang=udata["bot"]["lang"]
            ),
            value=f"<t:{math.floor(times)}:R>",
            inline=False,
        )

        guild_icon_url = "https://ui-avatars.com/api/?name={}".format(
            guild.name.replace(" ", "+").replace("　", "+")
        )
        if guild.icon:
            guild_icon_url = guild.icon.url

        embed.set_thumbnail(url=guild_icon_url)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="user", description="ユーザー情報を取得します。")
    @app_commands.checks.cooldown(5, 30)
    async def user(self, interaction: discord.Interaction, user: discord.User):
        udata = await self.userData.find_one({"userId": interaction.user.id})
        if udata is None:
            udata = {
                "userId": interaction.user.id,
                "bot": {"lang": "ja"},
                "is_dummy": True,
            }  # ダミーデータ生成
            await self.userData.insert_one(udata)
        await interaction.response.defer()
        avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
        if user.avatar:
            avatar_url = user.avatar.url
        menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)
        acolor = discord.Color.default()
        discriminator = ""
        if user.accent_color:
            acolor = user.accent_colour
        if not user.discriminator == "0":
            discriminator = "#" + user.discriminator
        """
        ustat = ustat_dct[user.status.name]
        user_stat = ustat["emoji"] + " " + self.bot.translation.getText(
            text=ustat["name"], lang=udata["bot"]["lang"]
        )
        embed.add_field(
            name=self.bot.translation.getText(
                text="status", lang=udata["bot"]["lang"]
            ),
            value=user_stat,
            inline=True,
        )
        """
        title = self.bot.translation.getText(
            "_{}'s information", lang=udata["bot"]["lang"]
        ).replace("_{}", user.name + discriminator)
        embed = discord.Embed(title=title, color=acolor)

        embed.add_field(
            name=self.bot.translation.getText(
                text="is bot?", lang=udata["bot"]["lang"]
            ),
            value=self.bot.translation.getText(
                text=yn[str(user.bot)], lang=udata["bot"]["lang"]
            ),
            inline=True,
        )
        times = user.created_at.timestamp()
        embed.add_field(
            name=self.bot.translation.getText(
                text="created at", lang=udata["bot"]["lang"]
            ),
            value=f"<t:{math.floor(times)}:R>",
            inline=False,
        )
        in_guild = False
        if interaction.guild.get_member(user.id):
            in_guild = True

        embed.add_field(
            name=self.bot.translation.getText(
                text="Are you on this server?", lang=udata["bot"]["lang"]
            ),
            value=self.bot.translation.getText(
                text=yn[str(in_guild)], lang=udata["bot"]["lang"]
            ),
            inline=False,
        )
        badges = discord.Embed(title=title, color=acolor)
        embed.set_thumbnail(url=avatar_url)
        badges.set_thumbnail(url=avatar_url)
        badges.add_field(
            name=self.bot.translation.getText(
                text="Badges owned", lang=udata["bot"]["lang"]
            ),
            value="",
            inline=False,
        )
        if not user.public_flags.all() == []:
            for i in user.public_flags.all():
                try:
                    badges.add_field(
                        name="",
                        value=UserFlags[i.name]["emoji"]
                        + " | "
                        + self.bot.translation.getText(
                            text=UserFlags[i.name]["name"], lang=udata["bot"]["lang"]
                        ),
                        inline=False,
                    )
                except KeyError:
                    pass
        else:
            badges.add_field(
                name="",
                value=self.bot.translation.getText(
                    text="This user does not have a badge.", lang=udata["bot"]["lang"]
                ),
                inline=False,
            )
        menu.add_page(embed)
        menu.add_page(badges)

        menu.add_button(
            ViewButton(
                style=discord.ButtonStyle.primary,
                label="<",
                custom_id=ViewButton.ID_PREVIOUS_PAGE,
            )
        )
        menu.add_button(
            ViewButton(
                style=discord.ButtonStyle.success,
                label=">",
                custom_id=ViewButton.ID_NEXT_PAGE,
            )
        )

        await menu.start()


async def setup(bot: commands.Bot):
    await bot.add_cog(utils(bot))
