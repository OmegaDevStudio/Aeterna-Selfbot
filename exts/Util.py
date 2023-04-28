from selfcord import Extender
from aioconsole import aprint
from aiohttp import ClientSession
import re


class Ext(Extender, name="Util", description="Uttility related commands here"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.nitro_toggle = False
        self.msg_toggle = False
        self.inv_toggle = False
        self.INVITE_REGEX = re.compile(r"(http://|https://|)(discord.gg/|canary.discord.com/invite/|ptb.discord.com/invite/|discordapp.com/invite/|discord.com/invite/)[A-z]{3,20}")
        self.NITRO_REGEX = re.compile(r"(http://|https://|)(discord.com/gifts/|discordapp.com/gifts/|discord.gift/|canary.discord.com/gifts/|ptb.discord.com/gifts)([a-zA-Z0-9]{5,18})")



    @Extender.cmd(description="Gathers information regarding token", aliases=['tdox', 'tinfo'])
    async def tokeninfo(self, ctx, _token: str):
        """Gathers information regarding a token, works for both bot tokens and user tokens.
        """
        await ctx.message.delete()
        async with ClientSession() as session:
            async with session.get("https://discord.com/api/v9/users/@me", headers={"authorization": f"Bot {_token}"})as resp:
                if resp.status == 200:
                    data = await resp.json()

                    msg = f"```ini\n[ Token Information ]\n\n"
                    for key, value in data.items():
                        msg += f"[ {key} ] : [ {value} ]\n"

                    msg += "```"
                    await ctx.send(f"{msg}")
                else:
                    async with session.get("https://discord.com/api/v9/users/@me", headers={"authorization": f"{_token}"})as resp:
                        if resp.status == 200:
                            data = await resp.json()

                            msg = f"```ini\n[ Token Information ]\n\n"
                            for key, value in data.items():
                                msg += f"[ {key} ] : [ {value} ]\n"

                            msg += "```"
                            await ctx.send(f"{msg}")
                        else:
                            data = await resp.json()
                            await ctx.send(f"{data} ---- {resp.status}")

    @Extender.cmd(description="Toggles Nitro Sniper", aliases=['nsnipe', 'nsniper'])
    async def nitrosniper(self, ctx, toggle):
        """Toggles the nitro sniper, the nitro sniper attempts to redeem any nitro gift code immediately as the gateway receives it. Information whether the redeeming of the gift was successful or not is displayed via the console.
        """
        if toggle.lower() == "on" or toggle.lower() == "true":
            self.nitro_toggle = True
            await ctx.reply(f"```ini\n[ Nitro Sniper is ON ]```")
        elif toggle.lower() == "off" or toggle.lower() == "false":
            self.nitro_toggle = False
            await ctx.reply(f"```ini\n[ Nitro Sniper is OFF ]```")

    @Extender.cmd(description="Toggles Message Logger", aliases=['msgsniper', 'msglogger', 'msgsnipe', 'msnipe'])
    async def messagesniper(self, ctx, toggle):
        """Toggles the message sniper, attempts to display deleted messages via the console, can only gather the full data of deleted messages after the bot starts running since they are cached, messages prior are not cached and therefore cannot be completely logged.
        """
        if toggle.lower() == "on" or toggle.lower() == "true":
            self.msg_toggle = True
            await ctx.reply(f"```ini\n[ Message Logger is ON ]```")
        elif toggle.lower() == "off" or toggle.lower() == "false":
            self.msg_toggle = False
            await ctx.reply(f"```ini\n[ Message Logger is OFF ]```")

    @Extender.cmd(description="Toggles Invite Logger", aliases=['invlog', 'invlogger', 'ilog', 'ilogger'])
    async def invitelogger(self, ctx, toggle):
        """Toggles the invite logger, attempts to display any/all invites posted in chat via the console.
        """
        if toggle.lower() == "on" or toggle.lower() == "true":
            self.inv_toggle = True
            await ctx.reply(f"```ini\n[ Invite Logger is ON ]```")
        elif toggle.lower() == "off" or toggle.lower() == "false":
            self.inv_toggle = False
            await ctx.reply(f"```ini\n[ Invite Logger is OFF ]```")

    @Extender.cmd(description="Purges all messages in chat", aliases=['wipe'])
    async def purge(self, ctx, amount: int = None):
        await ctx.purge(amount)

    @Extender.on("message_delete")
    async def message_logger(self, message):
        if self.msg_toggle:
            if message.author != None:
                if message.author.id != self.bot.user.id:
                    if message.guild != None:
                        await aprint(f"""MESSAGE LOGGED:
SERVER: {message.guild.name}
CHANNEL: {message.channel.name}
CONTENT:
{message.author}: {message.content}
        """)
                    else:
                        await aprint(f"""MESSAGE LOGGED:
CHANNEL: {message.channel}
CONTENT:
{message.author}: {message.content}
                        """)

    @Extender.on("message")
    async def invite_logger(self, message):
        if self.inv_toggle:
            matches = self.INVITE_REGEX.findall(message.content)
            if len(matches) > 0:
                if message.guild != None:
                    await aprint(f"""Guild Invite Logged:
SERVER: {message.guild.name}
CHANNEL: {message.channel.name}
INVITE: {matches}

                                """)
                else:

                    await aprint(f"""Guild Invite Logged:
CHANNEL: {message.channel.name}
INVITE: {matches}
                                """)

    @Extender.on("message")
    async def nitro_logger(self, message):
        if self.nitro_toggle:
            matches = self.NITRO_REGEX.findall(message.content)
            if len(matches) > 0:
                for match in matches:
                    await self.bot.redeem_nitro(match[2])






