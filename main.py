import asyncio
import inspect
import json
import logging
import os

import selfcord
from aioconsole import aprint
from colorama import Fore as Color

from data.utils import TextEmbed, logo

with open("./config.json", "r") as f:
    config = json.load(f)

prefixes = config.get("prefixes")
token = config.get("token")

bot = selfcord.Bot(prefixes=prefixes, inbuilt_help=False, eval=True, debug=True)


@bot.on("ready")
async def ball(time):
    for item in os.listdir("./data/exts"):
        if item.endswith(".py"):
            await bot.load_extension(f"data.exts.{item[:-3]}")
    await asyncio.sleep(0.5)
    # os.system("cls" if os.name == "nt" else "clear")
    await logo()
    await aprint(
        f"""{Color.BLUE}
CONNECTED TO:
USER: {bot.user}
GUILDS: {len(bot.user.guilds)}
FRIENDS: {len(bot.user.friends)}

STARTUP:  {time:0.2f} seconds{Color.RESET}"""
    )
    await bot.change_presence(
        status="Online",
        afk=False,
        activity=selfcord.Activity.Game(
            name="Aeterna",
            details="With your mother",
            state="vibing",
            buttons={
                "Server": "https://discord.gg/9KtaxZKewk",
                "Wrapper": "https://pypi.org/project/selfcord.py/",
            },
            application_id="1100082565811015720",
            key="neovim",
        ),
    )

@bot.on("message")
async def stuff(message):
    if message.guild_id == "920709476724649984":
        print(message)


@bot.cmd(description="Load other extensions via urls", aliases=['install', 'loadext'])
async def skid(ctx, url: str):
    await bot.load_extension(url=url, dir="data/exts")

@bot.cmd(description="The Help Command", aliases=["h"])
async def help(ctx, cat=None):
    """The help command, dedicated to viewing all commands, extensions and information regarding commands."""
    if cat is None:
        msg = TextEmbed()
        msg.title("Aeterna Selfbot")
        msg += f"Logged in as **`{bot.user}`**\n"
        msg.description("Type <prefix>help <ext_name> to view commands relating to a specific extension. Type <prefix>help <cmd_name> to view information regarding a command.")
        msg.add_field("Prefixes", "  ".join(bot.prefixes))
        msg.subheading("Commands")
        for command in bot.commands:
            msg.add_field(command.name, command.description)
        msg.subheading("Extensions")
        for ext in bot.extensions:
            msg.add_field(ext.name, ext.description)
        return await ctx.reply(f"{msg}", delete_after=60)

    name = cat.lower()
    for ext in bot.extensions:
        if name == ext.name.lower():
            msg = TextEmbed().title("Aeterna Selfbot")
            msg.add_field(ext.name, ext.description)
            msg.add_manual(f"Logged in as **`{bot.user}`**\n")
            msg.description("Type <prefix>help <ext_name> to view commands relating to a specific extension. Type <prefix>help <cmd_name> to view information regarding a command.")
            msg.add_field("Prefixes", "  ".join(bot.prefixes))
            msg.subheading("Commands")                
            for command in ext.commands:
                if command.ext == ext.ext:
                    msg.add_field(command.name, command.description)

            return await ctx.reply(f"{msg}", delete_after=60)
    for cmd in bot.commands:
        if name == cmd.name.lower():
            msg = TextEmbed().title("Aeterna Selfbot")
            msg.add_manual(f"Logged in as **`{bot.user}`**\n")
            msg.description("Type <prefix>help <ext_name> to view commands relating to a specific extension. Type <prefix>help <cmd_name> to view information regarding a command.")
            msg.add_field("Prefixes", "  ".join(bot.prefixes))
            msg.subheading(cmd.name)
            msg.add_field("Description", cmd.description)
            msg.add_field("Long Description", cmd.func.__doc__)
            msg.add_field("Aliases", "  ".join(cmd.aliases))
            args = inspect.signature(cmd.func)
            msg.subheading("Example Usage")
            msg.add_manual(f"`{bot.prefixes[0]}{cmd.aliases[0]}")
            for arg in args.parameters.keys():
                if arg == "self" or arg == "ctx":
                    continue
                msg.add_manual(f" <{arg}>")
            msg.add_manual("`")

            return await ctx.reply(f"{msg}", delete_after=60)
    for ext in bot.extensions:
        for cmd in ext.commands:
            if name == cmd.name.lower():
                msg = TextEmbed().title("Aeterna Selfbot")
                msg.add_manual(f"Logged in as **`{bot.user}`**\n")
                msg.description("Type <prefix>help <ext_name> to view commands relating to a specific extension. Type <prefix>help <cmd_name> to view information regarding a command.")
                msg.add_field("Prefixes", "  ".join(bot.prefixes))
                msg.subheading(cmd.name)
                msg.add_field("Description", cmd.description)
                msg.add_field("Long Description", cmd.func.__doc__)
                msg.add_field("Aliases", "  ".join(cmd.aliases))
                args = inspect.signature(cmd.func)
                msg.subheading("Example Usage")
                msg.add_manual(f"`{bot.prefixes[0]}{cmd.aliases[0]}")
                for arg in args.parameters.keys():
                    if arg == "self" or arg == "ctx":
                        continue
                    msg.add_manual(f" <{arg}>")
                msg.add_manual("`")
                return await ctx.reply(f"{msg}", delete_after=60)

while True: # Very cool if bot breaks
    bot.run(token)
