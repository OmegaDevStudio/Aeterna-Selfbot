from aioconsole import aprint
from colorama import Fore as Color


async def logo():
    await aprint(
        f"""{Color.LIGHTBLUE_EX}
▄▀█ █▀▀ ▀█▀ █▀▀ █▀█ █▄░█ ▄▀█
█▀█ ██▄ ░█░ ██▄ █▀▄ █░▀█ █▀█
                 """
    )
