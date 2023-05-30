from aioconsole import aprint
from selfcord import (Bot, Context, DMChannel, Extender, GroupChannel, Message,
                      Messageable, User)


class Ext(Extender, name="Comms", description="Communication related commands here"):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.users: list[User] = []
        self.channels: list[GroupChannel] = []
        self.toggle: bool = True

    @Extender.cmd(description="Add a user/channel to Comms")
    async def add(self, ctx: Context, user: str):
        """Adds a user/channel to the communication list used to interact between dms"""
        chan: GroupChannel | None = self.bot.get_channel(user)
        if chan is None:
            user: User = await self.bot.get_user(user)
            self.users.append(user)
            await ctx.reply(f"Successfully appended `{user.name}` to Comms list")
        else:
            self.channels.append(chan)
            await ctx.reply(f"Successfully appended `{chan.name}` to Comms list")

    @Extender.cmd(description="Removes a user/channel from the comms list")
    async def remove(self, ctx: Context, user: str):
        """Deletes the user/channel from the communications list for ineraction between dms"""
        channel: GroupChannel | None = self.bot.get_channel(user)
        if channel is None:
            user: User = await self.bot.get_user(user)
            self.users.remove(user)
            await ctx.reply(f"Successfully removed `{user.name}` from the Comms list")
        else:
            self.channels.remove(channel)
            await ctx.reply(
                f"Successfully removed `{channel.name}` from the Comms list"
            )

    @Extender.cmd(description="Displays the users in the comms list", aliases=["show"])
    async def display(self, ctx: Context):
        """Displays the users in the communications list for interaction between dms"""
        msg = "```ini\nCommunications List\n\nUsers\n"
        for user in self.users:
            msg += f"[ {user.name} ]\n"
        msg += "\n\nChannels\n"
        for channel in self.channels:
            msg += f"[ {channel.name} ]\n"
        msg += "```"
        await ctx.reply(msg)

    @Extender.cmd(description="Clears the comms list", aliases=["remove-all"])
    async def clear(self, ctx: Context):
        """Removes all users from the communications list for interaction between dms"""
        self.users.clear()
        self.channels.clear()
        await ctx.reply("Cleared Comms list")

    @Extender.cmd(description="Toggles the comms session")
    async def toggles(self, ctx: Context):
        """Toggles communications session, simple toggle with no arguments. Default off."""
        self.toggle = not self.toggle
        await ctx.reply(f"Set toggle to {self.toggle}")

    @Extender.on("message")
    async def comms_msg(self, message: Message):
        if self.toggle:
            if message.author != self.bot.user:
                if (
                    isinstance(message.channel, DMChannel)
                    and message.author in self.users
                ):
                    for user in self.users:
                        if message.author == user:
                            continue
                        channel = await self.bot.create_dm(int(user.id))
                        await channel.send(
                            f"```ini\n[ {message.author.name} ] : {message.content}```"
                        )

                    for channel in self.channels:
                        if message.channel == channel:
                            continue

                        await channel.send(
                            f"```ini\n[ {message.author.name} ] : {message.content}```"
                        )

                if (
                    isinstance(message.channel, GroupChannel)
                    and message.channel in self.channels
                ):
                    for channel in self.channels:
                        if message.channel == channel:
                            continue
                        await channel.send(
                            f"```ini\n[ {message.author.name} ] : {message.content}```"
                        )
                    for user in self.users:
                        if message.author == user:
                            continue
                        channel = await self.bot.create_dm(int(user.id))
                        await channel.send(
                            f"```ini\n[ {message.author.name} ] : {message.content}```"
                        )
