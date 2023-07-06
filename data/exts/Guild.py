import asyncio
import random

import selfcord
from aioconsole import aprint
from selfcord import Bot, Context, Extender

from .. import TextEmbed


class Ext(Extender, name="Guild", description="Guild related commands here"):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @Extender.cmd(description="Ban user from guild")
    async def ban(self, ctx: Context, user: selfcord.User):
        """Bans a user from the guild the command was sent in"""
        await ctx.message.delete()
        await ctx.guild.ban(user.id)
        await ctx.reply(f"Banned {user.name}", delete_after=60)

    @Extender.cmd(description="Kick user from guild")
    async def kick(self, ctx: Context, user: selfcord.User):
        """Kicks a user from the guild the command was sent in"""
        await ctx.message.delete()
        await ctx.guild.kick(user.id)
        await ctx.reply(f"Kicked {user.name}", delete_after=60)

    @Extender.cmd(description="Timeout user from guild")
    async def timeout(
        self, ctx: Context, user: selfcord.User, hours: int = 0, mins: int = 1, seconds: int = 60
    ):
        """Timeout a user from the guild the command was sent in"""
        await ctx.message.delete()
        await ctx.guild.timeout(user.id, hours, mins, seconds)
        await ctx.reply(f"Timeout {user.name}", delete_after=60)

    @Extender.cmd(description="Display server information")
    async def serverinfo(self, ctx: Context):
        guild = ctx.guild
        msg = TextEmbed().title(guild.name)
        msg.add_field("ID", guild.id)
        msg.add_field("Region", guild.region)
        msg.add_field("Owner", (await self.bot.get_user(guild.owner_id)).name)
        msg.add_field("Members", guild.member_count)
        msg.add_field("Roles", len(guild.roles))
        msg.add_field("Channels", len(guild.channels))
        msg.add_field("Emojis", len(guild.emojis))
        msg.add_field("Splash", guild.splash)
        msg.add_field("MFA Level", guild.mfa_level)
        msg.add_field("Verification Level", guild.verification_level)
        msg.add_items("Features", guild.features)
        msg.add_field("Explicit Content Filter", guild.explicit_content_filter)
        msg.add_field("Icon", guild.icon_url)
        await ctx.reply(msg, delete_after=60)
        
