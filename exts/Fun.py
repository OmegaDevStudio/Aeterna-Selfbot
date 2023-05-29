import asyncio
import random

from aioconsole import aprint
from selfcord import Bot, Context, Extender, User, Voiceable


class Ext(Extender, name="Fun", description="General Fun commands here"):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.copy: User | None = None

    @Extender.cmd(description="Spams call")
    async def call(self, ctx: Context):
        """Spams call in a group or dm channel via quickly joining, ringing and then leaving."""
        await ctx.message.delete()
        for i in range(10):
            if isinstance(ctx.channel, Voiceable):
                await ctx.channel.video_call()
                await ctx.channel.leave_call()
                await asyncio.sleep(0.5)

    @Extender.cmd(description="Spam message")
    async def spam(self, ctx: Context, amount: int, *, message: str):
        """Spams messages in the dedicated text channel"""
        await ctx.message.delete()
        await ctx.spam(amount, message)

    @Extender.cmd(description="Calculate someones level of gayness", aliases=["grate"])
    async def gayrate(self, ctx: Context, person: str):
        """Attempts to rate someones level of homosexuality. This is calculated by the amount of hairs on their thighs. Less hair is often associated with being a femboy and therefore gay."""
        user: User = await self.bot.get_user(person)
        rng = random.randint(1, 100)
        msg = f"{user.name} is {rng}% Gay :rainbow_flag:"
        await ctx.reply(msg)

    @Extender.cmd(
        description="Calculate someones level of racism", aliases=["racerate"]
    )
    async def racistrate(self, ctx: Context, person: str):
        """Attempts to rate someones level of racism. THis is calculated by gathering their ancestral history and determining links."""
        user: User = await self.bot.get_user(person)
        rng = random.randint(1, 100)
        await ctx.reply(f"{user.name} is {rng}% Racist :rage:")

    @Extender.cmd(description="Express love for balls")
    async def balls(self, ctx: Context):
        """Express love for big black balls"""
        colors = ["❤️🖤❤️", "🖤❤️🖤"]
        index = 0
        msg = f"{colors[index]} balls {colors[index]}"
        message = await ctx.send(msg)
        for _ in range(5):
            await asyncio.sleep(1.7)
            index = (index + 1) % 2
            msg = f"{colors[index]} balls {colors[index]}"
            await message.edit(msg)

    @Extender.cmd(description="Copies a users messages", aliases=["copy"])
    async def copycat(self, ctx: Context, user: str = None):
        """Copies a users messages, omit user parameter to turn off"""
        if user is not None:
            user: User = await self.bot.get_user(user)
            self.copy: User = user
            await ctx.reply(f"Began copying {user.name}")
        else:
            await ctx.reply(f"Stopped copying {self.copy.name}")
            self.copy = None

    @Extender.cmd(description="Esex command", aliases=["esex"])
    async def sex(self, ctx: Context):
        """Does the esex. Change pasta.txt for whatever copypasta, separate by lines"""
        with open("./pasta.txt", encoding="utf-8") as f:
            file = f.read().splitlines()
        for sent in file:
            await ctx.edit(content=sent)
            await asyncio.sleep(2)

    @Extender.on("message")
    async def copy_msg(self, message):
        if self.copy is not None:
            if message.author.id == self.copy.id:
                channel = message.channel
                await channel.send(message.content)
                if len(attachments) > 0:
                    msg = "\n".join([atch.proxy_url for atch in message.attachments])
                    await channel.send(message)
