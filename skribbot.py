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
VERSION =  "v1.3"

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
        """
        Handles what to do after receiving a message, based on its content
        """
        if message.author == self.user:
            return
        
        response = ""

        # MENSAJES EXACTOS
        if message.content == '.ready':
            response = await self.messageReady(message)
        
        if message.content == '.readyone':
            response  = await self.messageReady(message, everyone=True)

        elif message.content == '.unready':
            response = self.messageUnready(message)

        elif message.content == '.readyList':
            response = self.messageReadyList(message)
        
        elif message.content == '.voz':
            response = self.messageVoz(message)
        
        elif message.content== '.replay':
            response = await self.messageReplay(message)

        elif message.content == '.link':
            response = self.messageLink(message)

        elif message.content == ".start":
            response = self.messageStart(message)

        elif message.content == ".valorar":
            response = self.messageValorar()
        
        elif message.content == ".impugno":
            response = self.messageImpugno()

        elif message.content == ".help":
            channelMessage, directMessage = self.messageHelp(message)
            response = channelMessage
            await message.author.send(directMessage)
        

        # VARIABLES        
        elif message.content.startswith(".config"):
            response = self.messageConfig(message)
        
        elif message.content.split(' ')[0][1:] in Pinturillo.VALID_CONFIG_KEYS:
            response = self.messageShortConfig(message)

        if response:
            await message.channel.send(response)
                        
    # **************************************
    #     R E A D Y    &    U N R E A D Y
    # **************************************
    
    async def messageReady(self, message, everyone=False):
        """
        Handles the action if the message received was .ready
        """
        response = ""
      
        # FIRST MESSAGE
        if self.pinturillo is None:
            self.pinturillo = Pinturillo(roomConfig = self.roomConfig)
            self.addReady(message.author)

            mention = " @everyone" if everyone else ""
            
            response = f"Venga va, ¿quién más se apunta?{mention} ¡Ya hay 1/{self.minimo}!"

        # IF NOT ADDED ALREADY
        elif self.addReady(message.author):
            response = self.getReadyMessage(message)

            if len(self.readyList) >= self.minimo:
                response += " Pero bueno... ¡somos suficientes para que no dé pena!"
                if not self.pinturillo.URL:
                    self.pinturillo.URL = "Loading"
                    await message.channel.send("Cargando sala...")
                    self.pinturillo.run()
                    response += f" Aquí tenéis el enlace: {self.pinturillo.URL}"
                
            else:
                response += " Ya somos {}/{}".format(len(self.readyList), self.minimo)
        return response

    def addReady(self, user):
        """
        Auxiliary method that adds a user to the readyList. Returns True if added,
        and False if it was already there
        """
        if user not in self.readyList:
            self.readyList.append(user)
            return True
        return False

    def getReadyMessage(self, message):
        """
        Auxiliary method that returns a random message on .ready
        """
        mention = message.author.mention
        options = [
            f"¡Perfecto, {mention}!",
            f"No esperaba menos, {mention}.",
            f"¿Estás seguro de que no tienes otras cosas a hacer, {mention}?",
            f"¡Genial, {mention}!",
            f"Más te vale dibujar bien, {mention}.",
            f"🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷 🇦🇷",
        ]
        return options[random.randint(0, len(options) - 1)]

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

    def messageReadyList(self, message):
        """
        Returns the list of people that are Ready
        """
        if not self.readyList:
            response = "No hay nadie todavía."
        else:
            readyPeople = [person.name for person in self.readyList]
            stringPeople = ", ".join(readyPeople)
            response = "Gente ready: {}.".format(stringPeople)
        return response
    
    def messageVoz(self, message):
        """
        Mentions everyone who is in the readyList
        """
        if not self.readyList:
            return "Ve tú si quieres, pero no hay nadie más..."
        
        guild = message.guild
        inVoiceChannel = [member for voice_channel in guild.voice_channels for member in voice_channel.members]
        rezagados = [member for member in self.readyList if member not in inVoiceChannel]

        if rezagados:
            response = f"¡Ya estáis tardando en entrar al chat de voz!"
            for member in rezagados:
                response += f" {member.mention}"
        else:
            response = f"¡Pero si ya estáis todos! Deja de escribir, anda, que ya tenemos todos micro."
        
        return response

    # **************************************
    #      G A M E     M A N A G E M E N T
    # **************************************

    async def messageReplay(self, message):

        if self.pinturillo:
            self.pinturillo.quit()

        await message.channel.send("Creando nueva sala...")
        self.pinturillo = Pinturillo(roomConfig=self.roomConfig)
        self.pinturillo.run()

        self.oldURL = ""
        
        return f'¡Oído cocina! Aquí tienes el enlace de la nueva sala: {self.pinturillo.URL}'
        

    def messageLink(self, message):
        """
        Returns current link (or previous, if the game has already started)
        """
        if self.pinturillo is None or not self.pinturillo.URL:
            if not self.oldURL:
                response = f"Aún no he abierto ninguna sala..."
            else:
                response = f"La última vez los dejé en {self.oldURL}... ¿Si corres quizá los pillas?"

        if len(self.readyList) >= self.minimo:
            response  = "Aquí tienes: {}".format(self.pinturillo.URL)
        return response

    def messageStart(self, message):
        """
        Handles the start of the game (emptying the readyList, and closing the browser window)
        """
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
    
    # ***********************************
    #             B R O M A S
    # ***********************************

    def messageImpugno(self):
        """
        Handles the messages of impugnación of games
        """
        opciones = [
            "Colorín, colorado, este game está impugnado.",
            "Esta partida queda oficialmente impugnada.",
        ]
        return opciones[random.randint(0, len(opciones) - 1 )]

    def messageValorar(self):
        """
        Handles the valorations of screenshots
        """
        opciones = [
            "Un dibujo terrible, 0/10",
            "Mi sobrino de 3 años lo haría mejor, 2/10",
            "Se puede llegar a sacar, pero me faltan tres cervezas, 4/10",
            "Decente (para ser tú), 6/10",
            "Oye pues ni tan mal,  8/10",
            "Yo de ti lo pondría en el currículum, 10/10"
        ]
        
        return opciones[random.randint(0,5)]        


    #  **********************************
    #     C O N F I G U R A T I O N
    #  **********************************

    def messageConfig(self, message):
        """
        Handles explicit configuration. If no other parameters, the current config is shown.
        """
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
        """
        Handles configuration of only one parameter
        """
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
        """
        Auxiliary method that sets a configuration to the state
        """
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
        """
        Auxiliary method that gets current configuration
        """
        response = "\n**__Current configuration:__**\n"
        for key, value in self.roomConfig.items():
            response += f"**{key.capitalize()}**: _{value}_\n"
        return response

    def getParam(self, key):
        """
        Auxiliary method that returns the configuration of a given parameter.
        """
        value = self.minimo if key == 'minimo' else self.roomConfig[key]
        return f'**{key.capitalize()}:** _{value}_'

    # *********************************
    #            H E L P
    # *********************************

    def messageHelp(self, message):
        channelMessage = f'Perfecto, {message.author.mention}, te he enviado los comandos por MD.'
        directMessage = (
            f"¡Hola! Al habla Skribbot ({VERSION}). Aquí van los diferentes comandos:\n\n"
            "**READY**\n"
            "```"
            ".ready : Te añade a la lista de gente lista para jugar. Si sois suficientes, crea una partida.\n\n"
            ".readyone : Lo mismo que el .ready, pero con un @everyone. Usar con moderación.\n\n"
            ".unready : Te elimina de la lista de gente lista para jugar. \n\n"
            ".readyList : Muestra la gente que está ready.\n\n"
            ".voz : Mención a gente que ha hecho ready pero no está en voz."
            "```\n"
            "**GAME MANAGEMENT**\n"
            "```"
            ".replay : Crea una nueva sala, independientemente de la gente que haya en .ready\n\n"
            ".link  : Muestra el enlace de la partida que va a empezar (o la en curso)\n\n"
            ".start : Empieza la partida de la sala, y echa al bot de ella. ¡Espera a que entren todos!"
            "```\n"
            "**MISCELÁNEAS**\n"
            "```"
            ".impugno : Lanza este comando para impugnar la partida anterior.\n\n"
            ".valorar : Lanza este comando para valorar la screenshot anterior.\n\n"
            "```\n"
            "**CONFIGURACIÓN**\n"
            "```"
            ".config : Muestra la configuración actual de la sala. Se puede encadenar este comando con los parámetros para actualizarlos:\n\n"
                "\t-language=spanish\n"
                "\t-rounds=4\n"
                "\t-customs=true\n"
                "\t-drawtime=80\n"
                "\t-onlycustoms=false\n"
                "\t-minimo=4  (mínimo de gente para empezar partida con .ready)\n"
            "\n\tAdemás, hay shortcuts:\n"
                "\t-customs es equivalente a customs=true, y nocustoms o sincustoms es equivalente a customs=false\n"
                "\t-onlycustoms es equivalente a onlycustoms=true, y mixed es equivalente a onlycustoms=false\n"
                "\t-english, ingles, inglés, spanish y español se pueden usar en vez de language=idioma\n"
            "\n\tAsí, un ejemplo sería:\n"
                "\t\t.config spanish customs mixto rounds=5 drawtime=60 minimo=3\n\n"
            ".{parametro} : Muestra el valor del parámetro. Se puede encadenar con un valor para asignárselo.\n"
            "\tAsí, .language te dice el idioma, y .language english cambia el idioma\n"
            "```\n"
        )

        return channelMessage, directMessage

client = Skribbot()
client.run(TOKEN)