import asyncio
import inspect
import json
import logging
import os

import selfcord
from aioconsole import aprint
from colorama import Fore as Color

from utils import logo

with open("./config.json", "r") as f:
    config = json.load(f)

prefixes = config.get("prefixes")
token = config.get("token")

bot = selfcord.Bot(prefixes=prefixes, inbuilt_help=False, eval=True, debug=True)


@bot.on("ready")
async def ball(time):
    for item in os.listdir("./exts"):
        if item.endswith(".py"):
            await bot.load_extension(f"exts.{item[:-3]}")
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
            key="sheepshead_fish",
        ),
    )

@bot.cmd(description="Load other extensions via urls", aliases=['install', 'loadext'])
async def skid(ctx, url: str):
    await bot.load_extension(url=url, dir="exts")

@bot.cmd(description="The Help Command", aliases=["h"])
async def help(ctx, cat=None):
    """The help command, dedicated to viewing all commands, extensions and information regarding commands."""
    if cat is None:
        msg = f"```ini\n[ Aeterna Selfbot ]\n"
        msg += f"[ {bot.user} ]\nType <prefix>help <ext_name> to view commands relating to a specific extension. Type <prefix>help <cmd_name> to view information regarding a command.\n[ .Prefixes ] : {bot.prefixes}\n\n"
        msg += f"[ .Commands ]\n"
        for command in bot.commands:
            msg += f". {command.name}: {command.description}\n"
        msg += "\n[ .Extensions ]\n"
        for ext in bot.extensions:
            msg += f"[ {ext.name} ] : [ {ext.description} ]\n"

        msg += f"```"
        return await ctx.reply(f"{msg}", delete_after=60)

    else:
        name = cat.lower()
        for ext in bot.extensions:
            if name == ext.name.lower():
                msg = f"```ini\n[ Aeterna Selfbot ]\n"
                msg += f"[ {bot.user} ]\n\nType <prefix>help <ext_name> to view commands relating to a specific extension. Type <prefix>help <cmd_name> to view information regarding a command.\n\n[ .Prefixes ] : {bot.prefixes}\n\n"
                msg += f"[ .Commands ]\n"
                for command in ext.commands:
                    if command.ext == ext.ext:
                        msg += f". {command.name}: {command.description}\n"

                msg += f"```"
                return await ctx.reply(f"{msg}", delete_after=60)
        else:
            for cmd in bot.commands:
                if name == cmd.name.lower():
                    msg = f"```ini\n[ Aeterna Selfbot ]\n"
                    msg += f"[ {bot.user} ]\n\nType <prefix>help <ext_name> to view commands relating to a specific extension. Type <prefix>help <cmd_name> to view information regarding a command.\n\n[ .Prefixes ] : {bot.prefixes}\n\n"
                    msg += f"[ .{cmd.name} ]\n"
                    msg += f"[ Description ] :  {cmd.description} \n"
                    msg += f"[ Long Description ] :\n{cmd.func.__doc__}\n"
                    msg += f"[ Aliases ] : {cmd.aliases} \n"
                    args = inspect.signature(cmd.func)
                    msg += f"\n[ Example Usage ] :\n[ {bot.prefixes[0]}{cmd.aliases[0]}"
                    for arg in args.parameters.keys():
                        if arg == "self" or arg == "ctx":
                            continue
                        msg += f" <{arg}>"
                    msg += f" ]"

                    msg += f"```"
                    return await ctx.reply(f"{msg}", delete_after=60)
            for ext in bot.extensions:
                for cmd in ext.commands:
                    if name == cmd.name.lower():
                        msg = f"```ini\n[ Aeterna Selfbot ]\n"
                        msg += f"[ {bot.user} ]\n\nType <prefix>help <ext_name> to view commands relating to a specific extension. Type <prefix>help <cmd_name> to view information regarding a command.\n\n[ .Prefixes ] : {bot.prefixes}\n\n"
                        msg += f"[ .{cmd.name} ]\n"
                        msg += f"[ Description ] :  {cmd.description} \n"
                        msg += f"[ Long Description ] :\n{cmd.func.__doc__}\n"
                        msg += f"[ Aliases ] :  {cmd.aliases} \n"
                        args = inspect.signature(cmd.func)
                        msg += f"\n[ Example Usage ] :\n[ {bot.prefixes[0]}{cmd.aliases[0]}"
                        for arg in args.parameters.keys():
                            if arg == "self" or arg == "ctx":
                                continue
                            msg += f" <{arg}>"
                        msg += f" ]"

                        msg += f"```"
                        return await ctx.reply(f"{msg}", delete_after=60)


bot.run(token)
