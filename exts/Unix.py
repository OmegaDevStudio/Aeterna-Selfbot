import asyncio

from selfcord import Bot, Context, Extender


class Ext(
    Extender,
    name="Unix",
    description="CLI related commands here. Majority won't work unless the given program is installed. Used from a linux operating system.",
):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    @Extender.cmd(description="NMAP command")
    async def nmap(self, ctx: Context, *, msg: str):
        """The NMAP command, equivalent to nmap CLI tool. Does not require root permissions. Requires privileges for nmap."""
        val = await asyncio.subprocess.create_subprocess_shell(
            "nmap --privileged " + msg,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await val.communicate()
        if stdout:
            if len(stdout.decode()) < 1800:
                msg = f"```ini\n[ STDOUT ]\n{stdout.decode()}```"
                await ctx.reply(msg)
            else:
                for i in range(0, len(stdout.decode()), 1800):
                    msg = f"```ini\n[ STDOUT ]\n{stdout.decode()[i:i+1800]}```"
                    await ctx.reply(msg)
                    await asyncio.sleep(1.5)

        if stderr:
            if len(stderr.decode()) < 1800:
                msg = f"[ STDERR ]\n{stderr.decode()}"
            else:
                for i in range(0, len(stderr.decode()), 1800):
                    msg = f"```ini\n[ STDERR ]\n{stderr.decode()[i:i+1800]}"
                    await ctx.reply(msg)
                    await asyncio.sleep(1.5)

    @Extender.cmd(description="CAT command. Displays the contents of a file")
    async def cat(self, ctx: Context, *, path: str):
        """The CAT Command, equivalent to CAT cli tool. Does not require root permissions. Displays contents of a file. Uses a file path."""
        val = await asyncio.subprocess.create_subprocess_shell(
            "cat " + path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await val.communicate()
        if stdout:
            if len(stdout.decode()) < 1800:
                msg = f"```ini\n[ STDOUT ]\n{stdout.decode()}```"
                await ctx.reply(msg)
            else:
                for i in range(0, len(stdout.decode()), 1800):
                    msg = f"```ini\n[ STDOUT ]\n{stdout.decode()[i:i+1800]}```"
                    await ctx.reply(msg)
                    await asyncio.sleep(1.5)

        if stderr:
            if len(stderr.decode()) < 1800:
                msg = f"[ STDERR ]\n{stderr.decode()}"
            else:
                for i in range(0, len(stderr.decode()), 1800):
                    msg = f"```ini\n[ STDERR ]\n{stderr.decode()[i:i+1800]}"
                    await ctx.reply(msg)
                    await asyncio.sleep(1.5)

    @Extender.cmd(
        description="Nslookup command. Gathers information on a domain/ip address"
    )
    async def nslookup(self, ctx: Context, *, msg):
        """The Nslookup coomand, equivalent to the nslookup cli tool. Does not require root permissions. Shows IP address related to domains and dns records."""
        val = await asyncio.subprocess.create_subprocess_shell(
            "nslookup " + msg,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await val.communicate()
        if stdout:
            if len(stdout.decode()) < 1800:
                msg = f"```ini\n[ STDOUT ]\n{stdout.decode()}```"
                await ctx.reply(msg)
            else:
                for i in range(0, len(stdout.decode()), 1800):
                    msg = f"```ini\n[ STDOUT ]\n{stdout.decode()[i:i+1800]}```"
                    await ctx.reply(msg)
                    await asyncio.sleep(1.5)

        if stderr:
            if len(stderr.decode()) < 1800:
                msg = f"[ STDERR ]\n{stderr.decode()}"
            else:
                for i in range(0, len(stderr.decode()), 1800):
                    msg = f"```ini\n[ STDERR ]\n{stderr.decode()[i:i+1800]}"
                    await ctx.reply(msg)
                    await asyncio.sleep(1.5)

    @Extender.cmd(description="Curl command. Gather data from apis/domains.")
    async def curl(self, ctx: Context, *, msg):
        """The curl command. equivalent to the curl cli tool. Does not require root permissions. Gathers data from api endpoints or domains, can be used to test these api links."""
        val = await asyncio.subprocess.create_subprocess_shell(
            "curl " + msg,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await val.communicate()
        if stdout:
            if len(stdout.decode()) < 1800:
                msg = f"```ini\n[ STDOUT ]\n{stdout.decode()}```"
                await ctx.reply(msg)
            else:
                for i in range(0, len(stdout.decode()), 1800):
                    msg = f"```ini\n[ STDOUT ]\n{stdout.decode()[i:i+1800]}```"
                    await ctx.reply(msg)
                    await asyncio.sleep(1.5)

        if stderr:
            if len(stderr.decode()) < 1800:
                msg = f"[ STDERR ]\n{stderr.decode()}"
            else:
                for i in range(0, len(stderr.decode()), 1800):
                    msg = f"```ini\n[ STDERR ]\n{stderr.decode()[i:i+1800]}"
                    await ctx.reply(msg)
                    await asyncio.sleep(1.5)
