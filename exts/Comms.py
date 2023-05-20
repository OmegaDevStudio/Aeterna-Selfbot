from aioconsole import aprint
from selfcord import Bot, Context, DMChannel, Extender, Message, User


class Ext(Extender, name="Comms", description="Communication related commands here"):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.users: list[User] = []
        self.toggle: bool = False

    @Extender.cmd(description="Add a user to Comms")
    async def add(self, ctx: Context, user: str):
        """Adds a user to the communication list used to interact between dms"""
        user: User = await self.bot.get_user(user)
        self.users.append(user)
        await ctx.reply(f"Successfully appended {user.name} to Comms list")

    @Extender.cmd(description="Removes a user from the comms list")
    async def remove(self, ctx: Context, user: str):
        """Deletes the user from the communications list for ineraction between dms"""
        user: User = await self.bot.get_user(user)
        self.users.remove(user)
        await ctx.reply(f"Successfully removed {user.name} from the Comms list")

    @Extender.cmd(description="Displays the users in the comms list", aliases=["show"])
    async def display(self, ctx: Context):
        """Displays the users in the communications list for interaction between dms"""
        msg = "```ini\nCommunications List\n"
        for user in self.users:
            msg += f"[ {user.name} ]\n"
        msg += "```"
        await ctx.reply(msg)

    @Extender.cmd(description="Clears the comms list", aliases=["remove-all"])
    async def clear(self, ctx: Context):
        """Removes all users from the communications list for interaction between dms"""
        self.users.clear()
        await ctx.reply("Cleared Comms list")

    @Extender.cmd(description="Toggles the comms session")
    async def toggles(self, ctx: Context):
        """Toggles communications session, simple toggle with no arguments. Default off."""
        self.toggle = False if self.toggle else False
        await ctx.reply(f"Set toggle to {self.toggle}")

    @Extender.on("message")
    async def comms_msg(self, message: Message):
        if self.toggle:
            if message.author.id is not self.bot.user.id:
                if isinstance(message.channel, DMChannel) and message.author.id in [
                    user.id for user in self.users
                ]:
                    print(message.author.id, [user.id for user in self.users])
                    for user in self.users:
                        try:
                            if message.author.id == user.id:
                                continue
                            channel = await self.bot.create_dm(int(user.id))
                            await channel.send(
                                f"```ini\n[ {user.name} ] : {message.content}```"
                            )

                        except Exception as e:
                            await aprint(f"{e}")
