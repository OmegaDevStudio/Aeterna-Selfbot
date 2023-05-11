from selfcord import Extender
from aioconsole import aprint
import asyncio
import random

class Ext(Extender, name="Guild", description="Guild related commands here"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Extender.cmd(description="Ban user from guild")
    async def ban(self, ctx, user: str):
        """Bans a user from the guild the command was sent in
        """
        await ctx.message.delete()
        await self.bot.get_user(user)
        await ctx.guild.ban(user)

    @Extender.cmd(description="Kick user from guild")
    async def kick(self, ctx, user: str):
        """Kicks a user from the guild the command was sent in
        """
        await ctx.message.delete()
        await self.bot.get_user(user)
        await ctx.guild.kick(user)

    @Extender.cmd(description="Timeout user from guild")
    async def timeout(self, ctx, user: str, hours : int = 0, mins : int = 1, seconds: int = 60):
        """Timeout a user from the guild the command was sent in
        """
        await ctx.message.delete()
        await self.bot.get_user(user)
        await ctx.guild.timeout(user, hours, mins, seconds)