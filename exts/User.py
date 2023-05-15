from selfcord import Extender
from aioconsole import aprint
import selfcord

class Ext(Extender, name="User", description="User related commands here"):
    def __init__(self, bot: selfcord.Bot) -> None:
        self.bot = bot
        self.presence_toggle = False

    @Extender.cmd(description="Steals a users PFP", aliases=['getpfp'])
    async def stealpfp(self, ctx, id: str):
        """Steals the pfp of a mentioned user, or specified ID. Abundant usage of this command in quick succession can lead to locking.
        """
        user = await self.bot.get_user(id)
        await self.bot.change_pfp(user.avatar_url)
        await ctx.reply("Successfully changed PFP")

    @Extender.cmd(description="Sets PFP as specified url")
    async def setpfp(self, ctx, url: str):
        """Sets the pfp to a specified URL. Abundant usage of this command in quick succession can lead to locking.
        """
        await self.bot.change_pfp(url)
        await ctx.reply("Successfully changed PFP")

    @Extender.cmd(description="Edit bio")
    async def editbio(self, ctx, *, bio: str):
        """Changes the bio to one stated by the user.
        """
        await ctx.message.delete()
        await self.bot.edit_profile(bio=bio)

    @Extender.cmd(description="Changes hypesquad house")
    async def hypesquad(self, ctx, house: str):
        """Changes the hypesquad house to one stated by the user
        """
        await ctx.message.delete()
        await self.bot.change_hypesquad(house)

    @Extender.cmd(description="Sends a friend request", aliases=["addfriend"])
    async def friend(self, ctx, id: str):
        """Attempts to send a friend requets to a mentioned user, or specified ID.
        """
        await self.bot.add_friend(id)
        await ctx.reply("Successfully sent friend request")

    @Extender.cmd(description="Gathers information regarding a user", aliases=['userinfo'])
    async def whois(self, ctx, user: str):
        """Attempts to gather information regarding a user. Can gather profile data, basic user data such as date of creation and mutual friends.
        """
        user = await self.bot.get_user(user)
        msg = f"```ini\n[ {user} ]\n\n"
        msg += f"[ ID ] : {user.id}\n[ Bot? ] : {user.bot_acc}\n"
        tok = user.b64token.replace("==", "")
        msg += f"[ B64Token ] : {tok}\n"
        msg += f"[ Created at ] : {user.created_at}\n"

        profile = await user.get_profile()
        if profile != None:
            msg += f"[ Premium ] : {profile.premium_type}\n"
            msg += f"[ Mutual Guilds ] : {[guild.name for guild in profile.mutual_guilds]}\n"

            msg += f"[ Connected Accounts ] : \n"
            for account in profile.connected_accounts:
                msg += f"{account.name} : {account.type}\n"
            msg += f"[ Bio ] :\n{profile.bio}\n"
        msg += f"[ Mutual Friends ] : \n"
        for friend in (await user.get_mutual_friends()):
            msg += f"{friend}\n"
        msg += "```"
        msg += f"**BANNER:**{user.banner_url}\n**AVATAR:**{user.avatar_url}"

        await ctx.reply(msg)

    @Extender.cmd(description="Shows avatar of person", aliases=['av'])
    async def avatar(self, ctx, user: str):
        """Displays avatar of user
        """
        user = await self.bot.get_user(user)
        await ctx.reply(f"{user.avatar_url}")

    @Extender.cmd(description="Shows banner of person")
    async def banner(self, ctx, user: str):
        """Displays banner of user
        """
        user = await self.bot.get_user(user)
        await ctx.reply(f"{user.banner_url}")

    @Extender.cmd(description="Toggles the presence/status logger", aliases=["presencelog", "preslogger", "presencelogger", "clientlog", "clientlogger"])
    async def plog(self, ctx, toggle):
        if toggle.lower() == "on" or toggle.lower() == "true":
            self.presence_toggle = True
            await ctx.reply(f"```ini\n[ Presence Logger is ON ]```")
        elif toggle.lower() == "off" or toggle.lower() == "false":
            self.presence_toggle = False
            await ctx.reply(f"```ini\n[ Presence Logger is OFF ]```")

    @Extender.on("presence_update")
    async def presence_logger(self, user, status, last_modified, client_status, activity):
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

