from datetime import datetime

import selfcord
from aioconsole import aprint
from selfcord import Bot, Context, Extender, Profile, User

from .. import TextEmbed


class Ext(Extender, name="User", description="User related commands here"):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.presence_toggle: bool = False

    @Extender.cmd(description="Steals a users PFP", aliases=["getpfp"])
    async def stealpfp(self, ctx: Context, user: selfcord.User):
        """Steals the pfp of a mentioned user, or specified ID. Abundant usage of this command in quick succession can lead to locking."""
        
        await self.bot.change_pfp(user.avatar_url)
        await ctx.reply("Successfully changed PFP", delete_after=60)

    @Extender.cmd(description="Sets PFP as specified url")
    async def setpfp(self, ctx: Context, url: str):
        """Sets the pfp to a specified URL. Abundant usage of this command in quick succession can lead to locking."""
        await self.bot.change_pfp(url)
        await ctx.reply("Successfully changed PFP", delete_after=60)

    @Extender.cmd(description="Edit bio")
    async def editbio(self, ctx: Context, *, bio: str):
        """Changes the bio to one stated by the user."""
        await ctx.message.delete()
        await self.bot.edit_profile(bio=bio)

    @Extender.cmd(description="Changes hypesquad house")
    async def hypesquad(self, ctx: Context, house: str):
        """Changes the hypesquad house to one stated by the user"""
        await ctx.message.delete()
        await self.bot.change_hypesquad(house)

    @Extender.cmd(description="Sends a friend request", aliases=["addfriend"])
    async def friend(self, ctx: Context, id: str):
        """Attempts to send a friend requets to a mentioned user, or specified ID."""
        await self.bot.add_friend(id)
        await ctx.reply("Successfully sent friend request", delete_after=60)

    @Extender.cmd(
        description="Gathers information regarding a user", aliases=["userinfo"]
    )
    async def whois(self, ctx: Context, user: selfcord.User):
        """Attempts to gather information regarding a user. Can gather profile data, basic user data such as date of creation and mutual friends."""
        
        msg = TextEmbed().title(f"Whois {user}")
        tok = user.b64token.replace("==", "")
        msg.add_field("ID", user.id)
        msg.add_field("Bot?", user.bot_acc)
        msg.add_field("B64 Token", tok)
        msg.add_field("Created at", user.created_at)
        msg.add_field("Public Flags", user.public_flags)
        msg.add_field("Raw Public Flags", user.raw_public_flags)

        profile: Profile = await user.get_profile()
        if profile is not None:
            msg.add_field("Premium", profile.premium_type)
            msg.add_items("Mutual Guilds", profile.mutual_guilds, attr="name")
            msg.add_manual("**`Connected Accounts`**\n")
            for acc in profile.connected_accounts:
                msg.add_field(acc.type, acc.name)
            msg.add_field("Bio\n", profile.bio)
        msg.add_items("Mutual Friends", await user.get_mutual_friends(), attr="name")
        msg.add_field("Banner", user.banner_url)
        msg.add_field("Avatar", user.avatar_url)
        await ctx.reply(msg, delete_after=60)

    @Extender.cmd(description="Shows avatar of person", aliases=["av"])
    async def avatar(self, ctx: Context, user: selfcord.User):
        """Displays avatar of user"""
        await ctx.reply(f"{user.avatar_url}", delete_after=60)

    @Extender.cmd(description="Shows banner of person")
    async def banner(self, ctx: Context, user: selfcord.User):
        """Displays banner of user"""
        await ctx.reply(f"{user.banner_url}", delete_after=60)

    @Extender.cmd(
        description="Toggles the presence/status logger",
        aliases=[
            "presencelog",
            "preslogger",
            "presencelogger",
            "clientlog",
            "clientlogger",
        ],
    )
    async def plog(self, ctx: Context, toggle: str):
        if toggle.lower() == "on" or toggle.lower() == "true":
            self.presence_toggle = True
            await ctx.reply("**Presence Logger is ON**", delete_after=60)
        elif toggle.lower() == "off" or toggle.lower() == "false":
            self.presence_toggle = False
            await ctx.reply("**Presence Logger is OFF**", delete_after=60)

    @Extender.on("presence_update")
    async def presence_logger(
        self,
        user: User | str,
        status: str,
        last_modified: datetime,
        client_status: dict,
        activity: str,
    ):
        if self.presence_toggle:
            if not hasattr(user, "name"):
                user = await self.bot.get_user(user)
            msg = f"""
USER: {user}
STATUS: {status}\n"""
            if last_modified != None:
                msg += f"LAST MODIFIED: {last_modified}\n"
            if client_status != None:
                msg += "CLIENT:\n"
                for key, value in client_status.items():
                    msg += f"{key} : {value}\n"
            if activity != None:
                msg += f"ACTIVITY:\n{activity}"
            await aprint(msg)
