# bot.py
import os

import random
import discord

from discord.ext import tasks, commands

from dotenv import load_dotenv

from asyncio import sleep

from pinturillo import Pinturillo


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Skribbot(commands.Bot):
    VERSION =  "v1.3"

    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.pinturillo = None
        self.ready_list  = []
        self.minimo = 4
        self.old_URL = ""
    
    def set_pinturillo(self):
        room_config = self.get_cog('Config').room_config
        self.pinturillo = Pinturillo(room_config=room_config)
    
    def update_config(self):
        room_config = self.get_cog('Config').room_config
        self.pinturillo.update_config(room_config=room_config)

    def new_pinturillo(self):
        return Pinturillo()


    async def on_ready(self):
         print("The bot is ready!")

    #     elif message.content == ".help":
    #         channelMessage, directMessage = self.messageHelp(message)
    #         response = channelMessage
    #         await message.author.send(directMessage)

    # # @tasks.loop(hours=24)
    # # async def printer(self):

client = Skribbot(command_prefix=["."])
client.remove_command('help')
client.load_extension('cogs.ReadyCommands')
client.load_extension('cogs.Config')
client.load_extension('cogs.GameManagement')
client.load_extension('cogs.JokeCommands')
client.load_extension('cogs.OtherCommands')
client.run(TOKEN)