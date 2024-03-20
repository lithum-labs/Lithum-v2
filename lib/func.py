import asyncio

import discord
from discord.ext import commands

verification_level = discord.VerificationLevel


class func_inter:
    async def disable_dm(interaction: discord.Interaction):
        """
        ダイレクトメッセージ内で特定の操作を無効にする(スラッシュコマンド)
        """
        if not interaction.guild:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="このコマンドはダイレクトメッセージでは無効に設定されています。"
                ),
                ephemeral=True,
            )
            return True
        else:
            return False


class func_ctx:
    async def disable_dm(ctx: commands.Context):
        ctx.bot.translation.getText()
        """
        ダイレクトメッセージ内で特定の操作を無効にする(メッセージコマンド)
        """
        if not ctx.guild:
            msg = await ctx.reply(
                embed=discord.Embed(
                    title="このコマンドはダイレクトメッセージでは無効に設定されています。"
                )
            )
            await asyncio.sleep(2.5)
            await msg.delete()
            return True
        else:
            return False


VERIFICATIONLEVEL = {
    verification_level.none: "unlimited",
    verification_level.low: "Email authentication required",
    verification_level.medium: "Members must authenticate their email and 5 minutes must elapse after account registration.",
    verification_level.high: "Members must authenticate their email and have been in the guild for at least 5 minutes after registering their Discord account and for at least 10 minutes.",
    verification_level.highest: "Members must complete the phone number verification for their Discord account.",
}

PERMISSIONS = {
    "add_reactions": "Add Reactions",
    "administrator": "Adminstrator",
    "attach_files": "Attach Files",
    "ban_members": "Ban Members",
    "change_nickname": "Change Nickname",
    "connect": "Connect",
    "create_instant_invite": "Create Instant Invite",
    "create_private_threads": "Create Private Threads",
    "create_public_threads": "Create Public Threads",
    "deafen_members": "Deafen Members",
    "embed_links": "Embed Links",
    "external_emojis": "External Emojis",
    "external_stickers": "External Stickers",
    "kick_members": "Kick Members",
    "manage_channels": "Manage Channels",
    "manage_emojis": "Manage Emojis",
    "manage_events": "Manage Events",
    "manage_guild": "Manage Guild",
    "manage_messages": "Manage Messages",
    "manage_nicknames": "Manage Nicknames",
    "manage_roles": "Manage Roles",
    "manage_threads": "Manage Threads",
    "manage_webhooks": "Manage Webhooks",
    "mention_everyone": "Mention @everyone, @here, and All Roles",
    "moderate_members": "Timeout Members",
    "move_members": "Move Members",
    "mute_members": "Mute Members",
    "priorite_spealer": "Priority Speaker",
    "read_message_history": "Read Message History",
    "read_messages": "Read Messages",
    "request_to_speak": "Request to Speak",
    "send_messages_in_threads": "Send Messages in Threads",
    "send_messages": "Send Messages",
    "send_tts_messages": "Send TTS Messages",
    "speak": "Speak",
    "stream": "Video",
    "use_application_commands": "Use Application Commands",
    "use_embedded_activities": "Use Embedded Activities",
    "use_voice_activation": "Use Voice Activation",
    "view_audit_log": "View Audit Log",
    "view_guild_insights": "View Guild Insights",
}

UserFlags = {
    "staff": {"emoji": "<:discordstaff:1194674614945714217>", "name": "Discord Staff"},
    "partner": {
        "emoji": "<:discordpartner:1194674607333052476>",
        "name": "Discord Partner",
    },
    "hypesquad": {
        "emoji": "<:hypesquad:1194674633501327380>",
        "name": "HypeSquad Events Member",
    },
    "hypesquad_bravery": {
        "emoji": "<:bravery:1194674568607060119>",
        "name": "HypeSquad Bravery",
    },
    "hypesquad_brilliance": {
        "emoji": "<:brilliance:1194674575288565881>",
        "name": "HypeSquad Brilliance",
    },
    "hypesquad_balance": {
        "emoji": "<:balance:1194674684126580747>",
        "name": "HypeSquad Balance",
    },
    "early_supporter": {
        "emoji": "<:earlysupporter:1194674620754841660>",
        "name": "Early Supporter",
    },
    "bug_hunter": {
        "emoji": "<:bughunter_1:1194674581479366706>",
        "name": "Bug Hunter (lv.1)",
    },
    "bug_hunter_level_2": {
        "emoji": "<:bughunter_2:1194674588865531944>",
        "name": "Bug Hunter (lv.2)",
    },
    "verified_bot": {"emoji": ":white_check_mark:", "name": "Verified Bot"},
    "verified_bot_developer": {
        "emoji": "<:earlyverifiedbotdev:1194674627587362897>",
        "name": "Early Verified Bot Developer",
    },
    "discord_certified_moderator": {
        "emoji": "<:certifiedmod:1194674594842411119>",
        "name": "Discord Moderator Program Alumni",
    },
    "active_developer": {
        "emoji": "<:activedeveloper:1194674654426705980>",
        "name": "Active Developer",
    },
}

ustat_dct = {
    "online": {
        "emoji": "🟢",
        "name": "online",
    },
    "idle": {
        "emoji": "🌙",
        "name": "idle",
    },
    "dnd": {
        "emoji": "🔴",
        "name": "dnd",
    },
    "do_not_disturb": {
        "emoji": "🔴",
        "name": "dnd",
    },
    "offline": {
        "emoji": "⚫",
        "name": "offline",
    },
    "invisible": {
        "emoji": "❓",
        "name": "unknown",
    },
}
