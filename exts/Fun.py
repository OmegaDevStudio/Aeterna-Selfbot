from selfcord import Extender
from aioconsole import aprint
import asyncio

class Ext(Extender, name="Fun", description="General Fun commands here"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Extender.cmd(description="Spams call")
    async def call(self, ctx):
        await ctx.message.delete()
        for i in range(10):
            await ctx.channel.call()
            await ctx.channel.leave()
            await asyncio.sleep(0.5)

    @Extender.cmd(description="Spam message")
    async def spam(self, ctx, amount: int, *, message: str):
        await ctx.message.delete()
        await ctx.spam(amount, message)
