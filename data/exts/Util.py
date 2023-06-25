import datetime
import os
import re
import sys
from time import time

import aiohttp
import selfcord
from aioconsole import aprint
from aiohttp import ClientSession
from selfcord import Bot, Context, Extender, Message

from .. import TextEmbed


class Ext(Extender, name="Util", description="Utility related commands here"):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.nitro_toggle: bool = False
        self.msg_toggle: bool = False
        self.inv_toggle: bool = False
        self.afk_message: bool | None = None
        self.timestamp: int = 0
        self.INVITE_REGEX = re.compile(
            r"(http://|https://|)(discord.gg/|canary.discord.com/invite/|ptb.discord.com/invite/|discordapp.com/invite/|discord.com/invite/)[A-z]{3,20}"
        )
        self.NITRO_REGEX = re.compile(
            r"(http://|https://|)(discord.com/gifts/|discordapp.com/gifts/|discord.gift/|canary.discord.com/gifts/|ptb.discord.com/gifts)([a-zA-Z0-9]{5,18})"
        )
    @Extender.cmd(
        description="Gather information regarding an IP address, IPv4 only", aliases=['ipdox', 'geoip']
    )
    async def ipinfo(self, ctx: Context, ip: str):
        await ctx.message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://ip-api.com/json/{ip}") as resp:
                json = await resp.json()
                msg = TextEmbed().title("IP Geolocation")
            for key, value in json.items():
                msg.add_field(key, value)
            await ctx.send(msg, delete_after=60)
    @Extender.cmd(
        description="Gathers information regarding token", aliases=["tdox", "tinfo"]
    )
    async def tokeninfo(self, ctx: Context, _token: str):
        """Gathers information regarding a token, works for both bot tokens and user tokens."""
        await ctx.message.delete()
        data = await self.bot.http.request(
            "get", "/users/@me", headers={"authorization": f"Bot {_token}"}
        )
        if data is None:
            data = await self.bot.http.request(
                "get", "/users/@me", headers={"authorization": _token}
            )
        if data is not None:
            msg = TextEmbed("Token Information")
            for key, value in data.items():
                msg.add_field(key, value)
            await ctx.send(msg, delete_after=60)
        else:
            await ctx.send("Token is Invalid!", delete_after=60)

    @Extender.cmd(description="Toggles Nitro Sniper", aliases=["nsnipe", "nsniper"])
    async def nitrosniper(self, ctx: Context, toggle: str):
        """Toggles the nitro sniper, the nitro sniper attempts to redeem any nitro gift code immediately as the gateway receives it. Information whether the redeeming of the gift was successful or not is displayed via the console."""
        if toggle.lower() == "on" or toggle.lower() == "true":
            self.nitro_toggle = True
            await ctx.reply("**Nitro Sniper is ON**", delete_after=60)
        elif toggle.lower() == "off" or toggle.lower() == "false":
            self.nitro_toggle = False
            await ctx.reply("**Nitro Sniper is OFF**", delete_after=60)

    @Extender.cmd(
        description="Toggles Message Logger",
        aliases=["msgsniper", "msglogger", "msgsnipe", "msnipe"],
    )
    async def messagesniper(self, ctx: Context, toggle: str):
        """Toggles the message sniper, attempts to display deleted messages via the console, can only gather the full data of deleted messages after the bot starts running since they are cached, messages prior are not cached and therefore cannot be completely logged."""
        if toggle.lower() == "on" or toggle.lower() == "true":
            self.msg_toggle = True
            await ctx.reply("**Message Logger is ON**", delete_after=60)
        elif toggle.lower() == "off" or toggle.lower() == "false":
            self.msg_toggle = False
            await ctx.reply("**Message Logger is OFF**", delete_after=60)

    @Extender.cmd(
        description="Toggles Invite Logger",
        aliases=["invlog", "invlogger", "ilog", "ilogger"],
    )
    async def invitelogger(self, ctx: Context, toggle: str):
        """Toggles the invite logger, attempts to display any/all invites posted in chat via the console."""
        if toggle.lower() == "on" or toggle.lower() == "true":
            self.inv_toggle = True
            await ctx.reply("**Invite Logger is ON**", delete_after=60)
        elif toggle.lower() == "off" or toggle.lower() == "false":
            self.inv_toggle = False
            await ctx.reply("**Invite Logger is OFF**", delete_after=60)

    @Extender.cmd(description="Purges all messages in chat", aliases=["wipe"])
    async def purge(self, ctx: Context, amount: int = 100):
        """Purges all your own messages in the chat."""
        await ctx.message.delete()
        await ctx.purge(amount)

    @Extender.cmd(description="Sets AFK status for user")
    async def afk(self, ctx: Context, *, message: str):
        self.afk_message = message
        self.timestamp = int(time())
        await ctx.send(f">>> # USER IS AFK\n*{message}*\n**<t:{self.timestamp}:R>**")

    @Extender.cmd(description="Snipes last send message")
    async def snipe(self, ctx: Context):
        for message in reversed(self.bot.user.deleted_messages):
            if message.channel == ctx.channel:
                msg = TextEmbed().title("Sniped Message").add_field(f"{datetime.datetime.fromtimestamp(message.deleted_time).strftime('%H:%M:%S')} | {message.author.name}", message.content)
                if len(message.attachments) > 0:
                    for atch in message.attachments:
                        msg += f"{atch.proxy_url}\n"
                return await ctx.reply(msg, delete_after=60)

    @Extender.on("message_delete")
    async def message_logger(self, message):
        if self.msg_toggle:
            if message.author != None:
                if message.author != self.bot.user:
                    if message.guild != None:
                        await aprint(
                            f"""MESSAGE LOGGED:
SERVER: {message.guild.name}
CHANNEL: {message.channel.name}
CONTENT:
{message.author}: {message.content}
        """
                        )
                    else:
                        await aprint(
                            f"""MESSAGE LOGGED:
CHANNEL: {message.channel}
CONTENT:
{message.author}: {message.content}
                        """
                        )

    @Extender.on("message")
    async def invite_logger(self, message):
        if self.inv_toggle:
            matches = self.INVITE_REGEX.findall(message.content)
            if len(matches) > 0:
                if message.guild != None:
                    await aprint(
                        f"""Guild Invite Logged:
SERVER: {message.guild.name}
CHANNEL: {message.channel.name}
INVITE: {matches}

                                """
                    )
                else:
                    await aprint(
                        f"""Guild Invite Logged:
CHANNEL: {message.channel.name}
INVITE: {matches}
                                """
                    )

    @Extender.on("message")
    async def nitro_logger(self, message):
        if self.nitro_toggle:
            matches = self.NITRO_REGEX.findall(message.content)
            if len(matches) > 0:
                for match in matches:
                    await self.bot.redeem_nitro(match[2])

    @Extender.on("message")
    async def afk_checker(self, message: Message):
        if self.afk_message is not None:
            for user in message.mentions:
                if user == self.bot.user:
                    await message.channel.reply(f">>> # USER IS AFK\n*{message}*\n**<t:{self.timestamp}:R>**")
            if (message.author == self.bot.user) and (not self.afk_message in message.content):
                self.afk_message = None
