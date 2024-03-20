import discord
import motor.core

from lib.LithumBot import LithumBot


async def check_author(interaction: discord.Interaction, author: discord.User):
    if interaction.user.id == author.id:
        return True
    return False


class edit_lang(discord.ui.View):
    def __init__(
        self,
        bot: LithumBot,
        user: discord.User,
        userData: motor.core.AgnosticCollection,
        timeout=180,
    ):
        super().__init__(timeout=timeout)
        self.user = user
        self.userData = userData
        self.bot = bot

    @discord.ui.select(
        cls=discord.ui.Select,
        placeholder="What is your favorite fruit?",
        options=[
            discord.SelectOption(
                label="日本語",
                default=True,
                emoji="🇯🇵",
                value={"lang": "ja", "name": "日本語"},
            ),
            discord.SelectOption(
                label="American English",
                emoji="🇺🇸",
                value={"lang": "en", "name": "American English"},
            ),
            """
            discord.SelectOption(
                label="繁體中文",
                emoji="🇹🇼",
                value={"lang": "zh-TW", "name": "繁體中文"},
            ),
            discord.SelectOption(
                label="简体中文",
                emoji="🇨🇳",
                value={"lang": "zh-CN", "name": "简体中文"},
            ),
            """
        ],
        min_values=1,
        max_values=1,
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        udata = await self.userData.find_one({"userId": interaction.user.id})
        if udata is None:
            udata = {
                "userId": interaction.user.id,
                "bot": {"lang": select.values[0]["lang"]},
            }
        if await check_author(interaction, self.user):
            select.values
            if udata is None:
                await self.userData.insert_one(udata)
            else:
                await self.userData.update_one(
                    {"userId": interaction.user.id},
                    {"$set": {"bot": {"lang": select.values[0]["lang"]}}},
                )
                udata["bot"]["lang"] = select.values[0]
            embed = discord.Embed(
                title=self.bot.translation.getText(
                    text="success", lang=udata["bot"]["lang"]
                ),
                description=self.bot.translation.getText(
                    text="Changed bot language to _{}.",
                    lang=udata["bot"]["lang"],
                ).replace("_{}", select.values[0]["name"]),
            )
            await interaction.followup.send(embed)
        embed = discord.Embed(
            title=self.bot.translation.getText(text="error", lang=udata["bot"]["lang"]),
            description=self.bot.translation.getText(
                text="You are not allowed to manipulate this dropdown.",
                lang=udata["bot"]["lang"],
            ),
        )
        await interaction.followup.send(embed=embed)
