import asyncio
import random

import selfcord
from aioconsole import aprint
from selfcord import Bot, Context, Extender


class Ext(Extender, name="Guild", description="Guild related commands here"):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @Extender.cmd(description="Ban user from guild")
    async def ban(self, ctx: Context, user: str):
        """Bans a user from the guild the command was sent in"""
        await ctx.message.delete()
        usr = await self.bot.get_user(user)
        await ctx.guild.ban(user)
        await ctx.reply(f"Banned {usr.name}")

    @Extender.cmd(description="Kick user from guild")
    async def kick(self, ctx: Context, user: str):
        """Kicks a user from the guild the command was sent in"""
        await ctx.message.delete()
        usr = await self.bot.get_user(user)
        await ctx.guild.kick(user)
        await ctx.reply(f"Kicked {usr.name}")

    @Extender.cmd(description="Timeout user from guild")
    async def timeout(
        self, ctx: Context, user: str, hours: int = 0, mins: int = 1, seconds: int = 60
    ):
        """Timeout a user from the guild the command was sent in"""
        await ctx.message.delete()
        usr = await self.bot.get_user(user)
        await ctx.guild.timeout(user, hours, mins, seconds)
        await ctx.reply(f"Timeout {usr.name}")
