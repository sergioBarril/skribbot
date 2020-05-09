# bot.py
import os

import random
import discord
from dotenv import load_dotenv

from asyncio import sleep

from pinturillo import Pinturillo


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

class Skribbot(discord.Client):

    def __init__(self):
        super().__init__()
        self.pinturillo = None
        self.readyList  = []

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, name=GUILD)
        print(
            f'{self.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content == '.ready':
            self.messageReady(message)

        elif message.content == '.unready':
            self.messageUnready(message)
        
        elif message.content == '.link':
            self.messageLink(message)

        elif message.content == '.readyList':
            self.messageReadyList(message)       
                        

    def messageReady(self, message):
        """
        Handles the action if the message received was .ready
        """
        response = ""
      
        # FIRST MESSAGE
        if self.pinturillo is None:
            self.pinturillo = Pinturillo()
            # self.addReady(message.author)
            response = "Venga va, ¿quién más se apunta? ¡Ya hay 1/4! @everyone"

        # IF NOT ADDED ALREADY
        elif self.addReady(message.author):
            response = "¡Perfecto, {}!".format(message.author.mention)

            if len(self.readyList) >= 2:
                response += " ¡Somos suficientes para que no dé pena!"
                if not self.pinturillo.URL:
                    self.pinturillo.URL = "Loading"
                    await message.channel.send("Cargando sala...")
                    self.pinturillo.run()
                    response += "Aquí tenéis el enlace: {}".format(self.pinturillo.URL)
                
            else:
                response += " Ya somos {}/4".format(len(self.readyList))
        await message.channel.send(response)

    def messageUnready(self, message):
        """
        Handles the message if the content was ".unready"
        """
        if message.author in self.readyList:
            self.readyList.remove(message.author)
            response = "Terrible, {}. Eso es porque tienes miedo...".format(message.author.name)
        else:
            response = "Pero si no habías hecho ready, so merluzo."
        await message.channel.send(response)

    def messageLink(self, message):
        response = ""
        if len(self.readyList) > 1:
            response  = "Aquí tienes: {}".format(self.pinturillo.URL)
        await message.channel.send(response)

    def messageReadyList(self, message):
        if not self.readyList:
            response = "No hay nadie todavía."
        else:
            response = "Gente ready: {}.".format([person.name for person in self.readyList])
        await message.channel.send(response)

    def addReady(self, user):
        # if user not in self.readyList:
        self.readyList.append(user)
        return True
        # return False

client = Skribbot()
client.run(TOKEN)