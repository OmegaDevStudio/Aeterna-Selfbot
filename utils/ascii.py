from colorama import Fore as Color
from aioconsole import aprint

async def logo():
    await aprint(f"""{Color.LIGHTBLUE_EX}
▄▀█ █▀▀ ▀█▀ █▀▀ █▀█ █▄░█ ▄▀█
█▀█ ██▄ ░█░ ██▄ █▀▄ █░▀█ █▀█
                 """)