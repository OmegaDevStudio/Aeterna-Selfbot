from selfcord import Extender
from aioconsole import aprint
import asyncio
import random

class Ext(Extender, name="Fun", description="General Fun commands here"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @Extender.cmd(description="Spams call")
    async def call(self, ctx):
        """Spams call in a group or dm channel via quickly joining, ringing and then leaving.
        """
        await ctx.message.delete()
        for i in range(10):
            await ctx.channel.call()
            await ctx.channel.leave()
            await asyncio.sleep(0.5)

    @Extender.cmd(description="Spam message")
    async def spam(self, ctx, amount: int, *, message: str):
        """Spams messages in the dedicated text channel
        """
        await ctx.message.delete()
        await ctx.spam(amount, message)

    @Extender.cmd(description="Rate someones gayness", aliases=['grate'])
    async def gayrate(self, ctx, person: int):
        """Attempts to rate someones level of homosexuality. This is calculated by the amount of hairs on their thighs. Less hair is often associated with being a femboy and therefore gay.
        """
        user = await self.bot.get_user(person)
        rng = random.randint(1, 100)
        msg = f"{user.name} is {rng}% Gay :rainbow_flag:"
        await ctx.reply(msg)

    @Extender.cmd(description="Express love for balls")
    async def balls(self, ctx):
        colors = ["❤️🖤❤️", "🖤❤️🖤"]
        index = 0
        msg = f"{colors[index]} balls {colors[index]}"
        message = await ctx.send(msg)
        for i in range(5):
            await asyncio.sleep(1.7)
            index = (index + 1) % 2
            msg = f"{colors[index]} balls {colors[index]}"
            await message.edit(msg)

