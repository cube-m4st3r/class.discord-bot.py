import os
import platform
import time

import config
import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from classes.database import Database

MY_GUILD = discord.Object(id=config.botConfig["hub-server-guild-id"])

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(command_prefix='!-&%', intents=intents)

    async def setup_hook(self):
        for foldername, subfolders, filenames in os.walk('./commands'):
            for fileName in filenames:
                if fileName.endswith('.py'):
                    # Construct the module path by removing the './' prefix
                    module_path = os.path.join(foldername, fileName)[2:-3].replace(os.path.sep, '.')

                    try:
                        # Dynamically import the module
                        module = __import__(module_path, fromlist=['setup'])

                        if hasattr(module, 'setup') and callable(getattr(module, 'setup')):
                            await self.load_extension(module_path)
                            print(f"Loaded extension: {module_path}")
                        else:
                            print(f"Ignoring {fileName}: 'setup' function not found.")
                    except (AttributeError, ImportError) as e:
                        print(f"Ignoring {fileName}: {e}")
                        # Handle the exception (file doesn't have the required setup or is not compatible)

        await self.tree.sync(guild=MY_GUILD)

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(f"{prfx} Logged in as {Fore.YELLOW} {self.user.name}")
        print(f"{prfx} Bot ID {Fore.YELLOW} {str(self.user.id)}")
        print(f"{prfx} Discord Version {Fore.YELLOW} {discord.__version__}")
        print(f"{prfx} Python Version {Fore.YELLOW} {str(platform.python_version())}")
        print(f"{prfx} Bot Version 0.1")
        print(f"{prfx} Slash CMDs Synced: {Fore.YELLOW + str(len(await self.tree.fetch_commands(guild=MY_GUILD)))} Commands")
        if Database():
            print(f"Database connection successful.")


client = Client()
client.run(config.botConfig["token"])
