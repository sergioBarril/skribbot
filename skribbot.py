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
        self.roomConfig = {
            "customs" : True,
            "language" : "Spanish",
            "rounds"  : 4,
            "drawTime" : 80,
            "onlyCustoms" : False,
        }
        self.minimo = 4
        self.oldURL = ""
    
    async def on_ready(self):
        guild = discord.utils.get(self.guilds, name=GUILD)
        print(
            f'{self.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        response = ""

        if message.content == '.ready':
            response = await self.messageReady(message)

        elif message.content == '.unready':
            response = self.messageUnready(message)
        
        elif message.content == '.link':
            response = self.messageLink(message)

        elif message.content == '.readyList':
            response = self.messageReadyList(message)

        elif message.content == ".start":
            response = self.messageStart(message)

        # elif message.content == ".customs":
        # response = self.getCustoms()
        
        elif message.content.startswith(".config"):
            response = self.messageConfig(message)
        
        elif message.content.split(' ')[0][1:] in Pinturillo.VALID_CONFIG_KEYS:
            response = self.messageShortConfig(message)

        if response:
            await message.channel.send(response)
                        

    async def messageReady(self, message):
        """
        Handles the action if the message received was .ready
        """
        response = ""
      
        # FIRST MESSAGE
        if self.pinturillo is None:
            self.pinturillo = Pinturillo(roomConfig = self.roomConfig)
            self.addReady(message.author)
            response = "Venga va, ¿quién más se apunta? ¡Ya hay 1/{}! @everyone".format(self.minimo)

        # IF NOT ADDED ALREADY
        elif self.addReady(message.author):
            response = "¡Perfecto, {}!".format(message.author.mention)

            if len(self.readyList) >= self.minimo:
                response += " ¡Somos suficientes para que no dé pena!"
                if not self.pinturillo.URL:
                    self.pinturillo.URL = "Loading"
                    await message.channel.send("Cargando sala...")
                    self.pinturillo.run()
                    response += " Aquí tenéis el enlace: {}".format(self.pinturillo.URL)
                
            else:
                response += " Ya somos {}/{}".format(len(self.readyList), self.minimo)
        return response

    def messageUnready(self, message):
        """
        Handles the message if the content was ".unready"
        """
        if message.author in self.readyList:
            self.readyList.remove(message.author)
            response = "Terrible, {}. Eso es porque tienes miedo...".format(message.author.name)
        else:
            response = "Pero si no habías hecho ready, so merluzo."
        return response

    def messageLink(self, message):
        if self.pinturillo is None or not self.pinturillo.URL:
            if not self.oldURL:
                response = f"Aún no he abierto ninguna sala..."
            else:
                response = f"La última vez los dejé en {self.oldURL}... ¿Si corres quizá los pillas?"

        if len(self.readyList) >= self.minimo:
            response  = "Aquí tienes: {}".format(self.pinturillo.URL)
        return response

    def messageReadyList(self, message):
        if not self.readyList:
            response = "No hay nadie todavía."
        else:
            readyPeople = [person.name for person in self.readyList]
            stringPeople = ", ".join(readyPeople)
            response = "Gente ready: {}.".format(stringPeople)
        return response

    def messageStart(self, message):
        if self.pinturillo is None:
            return "Start qué, si no aún no hay nada preparado... Haz .ready anda"
        
        if not self.pinturillo.URL or self.pinturillo.URL == "Loading...":
            return "Aún no estamos en la sala, cálmate y dale a .ready si no lo has hecho ya"
        
        if self.pinturillo.startGame():
            self.oldURL = self.pinturillo.URL
            self.pinturillo = None
            self.readyList = []
            return"¡A jugarrrr~!"
        
        return "Estoy yo solo todavía, espera a que entre la gente"

    def messageConfig(self, message):
        words = message.content.split(" ")
        words.remove(".config")

        newConfig = self.roomConfig.copy()

        if not words:
            return self.getCurrentConfig()
        
        for word in words:
            param = word.lower()

            # Explicit parameters
            if '=' in param:
                key, value = param.split("=")
                self.setConfig(key, value, newConfig)

            # Direct language edit
            if 'spanish' == param or 'español' == param:
                newConfig['language'] = 'Spanish'
            if 'english' == param or 'inglés' == param or 'ingles' == param:
                newConfig['language'] = 'English'
            
            # Direct customs edit
            if 'customs' == param:
                newConfig['customs'] = True
            if 'nocustoms' == param or "sincustoms" == param:
                newConfig['customs'] = False
            
            # Direct onlycustoms edit
            if 'onlycustoms' == param:
                newConfig['onlyCustoms'] = True
            if 'mixto' == param:
                newConfig['onlyCustoms'] = False
        
        self.roomConfig = newConfig

        if self.pinturillo is not None and self.pinturillo.URL:
            self.pinturillo.roomConfig = self.roomConfig
            self.pinturillo.roomConfiguration()
        
        return "Configuration updated!"
    
    def messageShortConfig(self, message):
        if len(message.content.split(' ')) == 1:
            key = message.content.split(' ')[0][1:].lower()
            return self.getParam(key)
        else:
            key, value = message.content.split(' ')
            key = key[1:].lower()
        
        isUpdated = self.setConfig(key, value, self.roomConfig)

        if isUpdated:
            if self.pinturillo is not None and self.pinturillo.URL:
                self.pinturillo.roomConfig = self.roomConfig
                self.pinturillo.roomConfiguration()
            return f'{key.capitalize()} updated to {value}.'
        
        return f'{value.capitalize} is not a valid value for {key}'

    def setConfig(self, key, value, newConfig):
        YES_OPTIONS = ("true", "si", "yes", "sí")
        NO_OPTIONS = ("false", "no")

        if key == 'language':
            language = value.capitalize()
            if language in Pinturillo.VALID_LANGUAGES:
                newConfig['language'] = language
                return True

        if key == 'rounds':
            if value in Pinturillo.VALID_ROUNDS:
                newConfig['rounds'] = int(value)
                return True
        
        if key == 'customs':
            isCustoms = value.lower()
            if isCustoms in YES_OPTIONS:
                newConfig['customs'] = True
                return True
            elif isCustoms in NO_OPTIONS:
                newConfig['customs'] = False
                return True
        
        if key == 'onlycustoms':
            isCustoms = value.lower()
            if isCustoms in YES_OPTIONS:
                newConfig['onlyCustoms'] = True
                return True
            elif isCustoms in NO_OPTIONS:
                newConfig['onlyCustoms'] = False
                return True
        
        if key == 'drawtime':
            if value in Pinturillo.VALID_DRAWTIME:
                newConfig['drawTime'] = int(value)
                return True

        if key == 'minimo':
            if value.isdigit():
                self.minimo = int(value)
                return True

        
        return False
        

    def getCurrentConfig(self):
        response = "\n**__Current configuration:__**\n"
        for key, value in self.roomConfig.items():
            response += f"**{key.capitalize()}**: _{value}_\n"
        return response

    def getParam(self, key):
        value = self.minimo if key == 'minimo' else self.roomConfig[key]
        return f'**{key.capitalize()}:** _{value}_'


    def addReady(self, user):
        if user not in self.readyList:
            self.readyList.append(user)
            return True
        return False
    
    # def getCustoms(self):
    #     if self.pinturillo.customs:
    #         customs = self.pinturillo.customs
    #     elif self.pinturillo:
    #         customs = self.pinturillo.readCustoms()
    #     else:
    #         return []
        
    #     if len(customs) < 1999:
    #         return [f"```{customs}```"]
        
    #     list(map(strip, customs.split(',')))

        
        
        

client = Skribbot()
client.run(TOKEN)