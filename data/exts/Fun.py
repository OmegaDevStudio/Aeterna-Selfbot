import asyncio
import random
import string

import aiohttp
from aioconsole import aprint
from faker import Faker
from selfcord import Bot, Context, Extender, Profile, User, Voiceable

from .. import TextEmbed


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
        msg = f"{user.name} is **{rng}%** Gay :rainbow_flag:"
        await ctx.reply(msg, delete_after=60)

    @Extender.cmd(
        description="Calculate someones level of racism", aliases=["racerate"]
    )
    async def racistrate(self, ctx: Context, person: str):
        """Attempts to rate someones level of racism. THis is calculated by gathering their ancestral history and determining links."""
        user: User = await self.bot.get_user(person)
        rng = random.randint(1, 100)
        await ctx.reply(f"{user.name} is **{rng}%** Racist :rage:", delete_after=60)

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
            if user == self.bot.user:
                return
            self.copy: User = user
            await ctx.reply(f"Began copying **{user.name}**", delete_after=60)
        else:
            await ctx.reply(f"Stopped copying **{self.copy.name}**", delete_after=60)
            self.copy = None

    @Extender.cmd(description="Does Otax on specified user", aliases=["hack"])
    async def otax(self, ctx: Context, user: str):
        """Hacks a user, displaying their entire token, name, and other credentials. Very scary otax"""
        await ctx.message.delete()
        user: User = await self.bot.get_user(user)
        message = "```ini\n[ Began Otax.rs ]```"

        msg = await ctx.send(message)
        await asyncio.sleep(1.5)
        await msg.edit("```ini\n[ Decrypting User token... ]```")
        await asyncio.sleep(1.5)
        await msg.edit("```ini\n[ Using SQL Injection... ]```")
        await asyncio.sleep(1.5)
        await msg.edit("```ini\n[ Gathering IP and DNS records... ]```")
        await asyncio.sleep(1.5)
        await msg.edit("```ini\n[ Gathering User Credentials... ]```")
        await asyncio.sleep(1.5)
        await msg.edit("```ini\n[ EXIF Location gathering... ]```")
        await asyncio.sleep(1.5)
        message = await msg.edit("```ini\n[ OTAX Completed... ]```")
        await asyncio.sleep(2)
        hobbies = [
            "Gaming",
            "Crossdressing",
            "OnlyFans",
            "FIFA",
            "Dick",
            "Stripping",
            "Redditor",
            "Touching balls",
            "Spreading Legs",
            "Knitting Sweaters",
            "Watching Porn",
            "Breathing oxygen",
            "Watching paint dry",
            "Being a hoe",
            "Being Pegged",
            "Pegging",
        ]
        rs_status = [
            "Single",
            "Deprived of human interaction",
            "Allergic to Grass",
            "Can't keep a man",
            "Thot",
            "Full-time Thot",
            "Tiny Penis syndrome",
        ]
        fake = Faker()
        msg = f"```ini\n[ {user} ]\n\n"
        msg += f"[ ID ] : {user.id}\n[ Bot? ] : {user.bot_acc}\n"
        msg += f"[ Name ] : {fake.name()}\n"
        tok = user.b64token.replace("==", "")
        x = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        x1 = "".join(
            random.choices(
                string.ascii_letters + string.digits, k=random.randint(27, 35)
            )
        )
        msg += f"[ Token ] : {tok}.{x}.{x1}\n"
        msg += f"[ Created at ] : {user.created_at}\n"
        msg += f"[ Interests/Hobbies ] : {random.choices(hobbies, k=3)}\n"
        msg += f"[ Relationship Status ] : {random.choice(rs_status)}\n"
        profile: Profile = await user.get_profile()
        if profile is not None:
            msg += f"[ Premium ] : {profile.premium_type}\n"
            msg += "[ Mutual Guilds ] : \n"
            for guild in profile.mutual_guilds:
                msg += f"{guild.name}\n"

            msg += "[ Connected Accounts ] : \n"
            for account in profile.connected_accounts:
                msg += f"{account.name} : {account.type}\n"
            msg += f"[ Bio ] :\n{profile.bio}\n"
        msg += f"[ Address ] : {fake.address()}\n"
        msg += f"[ Credit Card ] : {fake.credit_card_full()}\n"
        msg += "[ Mutual Friends ] : \n"
        for friend in await user.get_mutual_friends():
            msg += f"{friend}\n"
        msg += "```"
        msg += f"**BANNER:**{user.banner_url}\n**AVATAR:**{user.avatar_url}"
        await message.edit(msg, delete_after=60)

    @Extender.cmd(description="Esex command", aliases=["esex"])
    async def sex(self, ctx: Context):
        """Does the esex. Change pasta.txt for whatever copypasta, separate by lines"""
        with open("./pasta.txt", encoding="utf-8") as f:
            file = f.read().splitlines()
        for sent in file:
            await ctx.edit(content=sent)
            await asyncio.sleep(2)

    @Extender.cmd(description="Question the magic 8 ball", aliases=['8ball'])
    async def magic8ball(self, ctx: Context, *, question: str):
        """Ask the magic 8 ball questions and it shall answer truthfully."""
        responses = [
            'As I see it, yes.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Don’t count on it.',
            'It is certain.',
            'It is decidedly so.',
            'Most likely.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Outlook good.',
            'Reply hazy, try again.',
            'Signs point to yes.',
            'Very doubtful.',
            'Without a doubt.',
            'Yes.',
            'Yes – definitely.',
            'You may rely on it.',
        ]
        response = random.choice(responses)
        await ctx.reply(f"```ini\n[ Question ]\n{question}\n\n[ Answer ]\n{response}```", delete_after=60)

    @Extender.cmd(description="Responds with a very funny dad joke", aliases=['djoke'])
    async def dadjoke(self, ctx: Context):
        """Responds with a very funny dad joke. Incredible humour ngl."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://icanhazdadjoke.com",
                headers={"accept": "application/json"}
            ) as resp:
                json = await resp.json()
        await ctx.reply(f"{json['joke']}", delete_after=60)

    @Extender.cmd(description="Calculates length of penis for a user", aliases=['dick', 'shlong', 'pp'])
    async def penis(self, ctx: Context, user: str):
        user = await self.bot.get_user(user)
        await ctx.reply(f">>> # {user.name} penis\n\n**8{'=' * random.randint(1,10)}D**", delete_after=60)

    @Extender.cmd(description="Sends cool cat pics", aliases=['gato'])
    async def cat(self, ctx: Context):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search"
            ) as resp:
                json = await resp.json()
        await ctx.reply(f"{json[0]['url']}", delete_after=60)



    @Extender.cmd(description="Sends cool dog pic", aliases=['doggo'])
    async def dog(self, ctx: Context):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thedogapi.com/v1/images/search?limit=10"
            ) as resp:
                json = await resp.json()
        await ctx.reply(f"{json[0]['url']}", delete_after=60)

    @Extender.cmd(description="Starts a poll")
    async def poll(self, ctx: Context, question: str, *options):
        if len(options) > 10:
            await ctx.reply("Can't create poll with more than 10 options")
        
        msg = f">>> # Poll Question\n{question}\n"
        msg += "## Options\n"
        for index, option in enumerate(options):
            msg += f"**`{option}`**\n"
        message = await ctx.send(msg, delete_after=60)
        reactions = [
            "0️⃣",
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣"
        ]
        for i in range(len(options)):
            await message.react(reactions[i])



        
    @Extender.on("message")
    async def copy_msg(self, message):
        if self.copy is not None:
            if message.author == self.copy:
                channel = message.channel
                msg = message.content
                if len(message.attachments) > 0:
                    for atch in message.attachments:
                        msg += f"\n{atch.proxy_url}\n"
                    await channel.send(msg, delete_after=60)
                else:
                    await channel.send(msg, delete_after=60)
