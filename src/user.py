import math

# import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from lib.LithumBot import LithumBot

# import orjson as json
from reactionmenu import ViewMenu, ViewButton


cd = 4
VerificationLevel = discord.VerificationLevel


class utils(commands.GroupCog, name="tools"):
    def __init__(self, bot: LithumBot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
        self.verification_level = {
            VerificationLevel.none: "unlimited",
            VerificationLevel.low: "Email authentication required",
            VerificationLevel.medium: "Members must authenticate their email and 5 minutes must elapse after account registration.",
            VerificationLevel.high: "Members must authenticate their email and have been in the guild for at least 5 minutes after registering their Discord account and for at least 10 minutes.",
            VerificationLevel.highest: "Members must complete the phone number verification for their Discord account.",
        }

    @app_commands.command(name="guild", description="Retrieve guild information.")
    async def guild(self, interaction: discord.Interaction, guild_id: str):
        await interaction.response.defer()
        acolor = discord.Color.default()
        guild: discord.Guild = await self.bot.fetch_guild(int(guild_id))
        title = "{} information".format(guild.name)
        embed = discord.Embed(title=title, color=acolor)
        
        member_count = str(guild.member_count) + self.bot.translation.getText("ユーザー")
        if guild.member_count is None:
            member_count = self.bot.translation.getText("エラーが発生しました： メンバー数の値は None です。")
        discriminator = ""
        owner = self.bot.translation.getText("不明")
        owner_id = ""
        if guild.owner is not None:
            owner = guild.owner.name
            owner_id = " (ID:" + guild.owner.id + ")"
            if guild.owner.discriminator is not None:
                if not guild.owner.discriminator == "0":
                   discriminator = "#" + guild.owner.discriminator
        embed.add_field(
            name=self.bot.translation.getText("サーバーオーナー"), value=owner + discriminator + owner_id
        )

        embed.add_field(
            name=self.bot.translation.getText("メンバー数"),
            value=member_count,
            inline=False,
        )
        embed.add_field(
            name=self.bot.translation.getText("認証レベル"),
            value=self.verification_level[guild.verification_level],
            inline=False,
        )
        embed.add_field(
            name=self.bot.translation.getText("ブーストレベル"),
            value=self.bot.translation.getText("レベル ") + str(guild.premium_tier),
            inline=False,
        )
        embed.add_field(
            name=self.bot.translation.getText("ブースト数"),
            value=str(guild.premium_subscription_count),
            inline=False,
        )

        times = guild.created_at.timestamp()
        embed.add_field(
            name=self.bot.translation.getText("作成日"),
            value=f"<t:{math.floor(times)}:R>",
            inline=False,
        )

        guild_icon_url = "https://ui-avatars.com/api/?name={}".format(guild.name.replace(' ', "+").replace('　', '+'))
        if guild.icon:
            guild_icon_url = guild.icon.url
        else:
            print(guild_icon_url)

        embed.set_thumbnail(url=guild_icon_url)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="user", description="Retrieve user information.")
    async def user(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()
        menu = ViewMenu(interaction, menu_type=ViewMenu.TypeEmbed)
        acolor = discord.Color.default()
        discriminator = ""
        if user.accent_color:
            acolor = user.accent_colour
        if not user.discriminator == "0":
            discriminator = "#" + user.discriminator
        title = "{}'s information".format(user.name + discriminator)
        embed = discord.Embed(title=title, color=acolor)
        embed.add_field(name=self.bot.translation.getText("Bot？"), value=user.bot, inline=False)
        times = user.created_at.timestamp()
        embed.add_field(
            name=self.bot.translation.getText("作成日"),
            value=f"<t:{math.floor(times)}:R>",
            inline=False,
        )
        in_guild = False
        if interaction.guild.get_member(user.id):
            in_guild = True

        embed.add_field(
            name=self.bot.translation.getText("このサーバーにいる？"), value=in_guild, inline=False
        )
        badges = discord.Embed(title=title, color=acolor)
        avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
        if user.avatar:
            avatar_url = user.avatar.url
        embed.set_thumbnail(url=avatar_url)
        badges.set_thumbnail(url=avatar_url)
        badges.add_field(name=self.bot.translation.getText("所持しているバッジ"), value="", inline=False)
        if not user.public_flags.all() == []:
            for i in user.public_flags.all():
                try:
                    badges.add_field(
                        name="",
                        value=UserFlags[i] + " | " + UserFlags["name"][i],
                        inline=False,
                    )
                except KeyError:
                    pass
        else:
            badges.add_field(
                name="", value=self.bot.translation.getText("このユーザーはバッジを所持していません。"), inline=False
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