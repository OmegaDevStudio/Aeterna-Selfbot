from selfcord import Extender
from aioconsole import aprint

class Ext(Extender, name="User", description="User related commands here"):
    def __init__(self, bot) -> None:
        self.bot = bot

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




