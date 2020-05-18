import discord

import random

from discord.ext import commands

class Config(commands.Cog):

    YES_OPTIONS = ("true", "si", "yes", "sí")
    NO_OPTIONS = ("false", "no")
    
    VALID_BOOLEAN = YES_OPTIONS + NO_OPTIONS
    VALID_ROUNDS = [str(i) for i in range(2, 11)]
    VALID_DRAWTIME = [str(i) for i in range(30, 181, 10)]
    VALID_LANGUAGES = ("English", "German", "Bulgarian", "Czech", "Danish",
        "Dutch", "Finnish", "French", "Estonian", "Greek", "Hebrew", "Hungarian",
        "Italian", "Korean", "Latvian", "Macedonian", "Norwegian", "Portuguese", "Polish", "Romanian",
        "Serbian", "Slovakian", "Spanish", "Sedish", "Tagalog", "Turkish")
    
    # List of implicit params
    VALID_SINGLE_PARAM = (
        "inglés", "english", "ingles", "español", "spanish",
        "onlycustoms", "mixed",
        "customs", "nocustoms", "sincustoms"
    )

    # VALIDATION FUNCTIONS BASED ON PARAMETER
    VALID_CONFIG = {
        "minimo" : lambda x : x.isdigit(),
        "customs" : lambda x, VALID_BOOLEAN = VALID_BOOLEAN : x in VALID_BOOLEAN,
        "language" :  lambda x, VALID_LANGUAGES = VALID_LANGUAGES : x in VALID_LANGUAGES,
        "rounds" : lambda x, VALID_ROUNDS = VALID_ROUNDS: x in VALID_ROUNDS,
        "drawtime" : lambda x, VALID_DRAWTIME = VALID_DRAWTIME : x in VALID_DRAWTIME,
        "onlycustoms" : lambda x, VALID_BOOLEAN = VALID_BOOLEAN : x in VALID_BOOLEAN
    }

    # CONVERSION FUNCTIONS BASED ON PARAMETER
    # Returns the param in a suitable format for insertion
    SET_CONFIG = {
        "minimo" : lambda minimo : int(minimo),
        "customs" : lambda boolean, YES_OPTIONS = YES_OPTIONS: boolean in YES_OPTIONS,
        "language" : lambda language : language.capitalize(),
        "rounds" :  lambda rounds : int(rounds),
        "drawtime" :  lambda time : int(time),
        "onlycustoms" : lambda boolean, YES_OPTIONS = YES_OPTIONS : boolean in YES_OPTIONS,
    }

    VALID_CONFIG_KEYS = VALID_CONFIG.keys()

    def __init__(self, bot):
        self.bot = bot
        
        self.room_config = {
            "minimo" : 4,
            "customs" : False,
            "language" : "Spanish",
            "rounds"  : 4,
            "drawtime" : 80,
            "onlycustoms" : False,
        }
    
    #  **********************************
    #     C O N F I G U R A T I O N
    #  **********************************    

    def is_valid(self, param_list):
        # BAD = PLACING
        if len(param_list) > 2 or len(param_list) == 0:
            return False
    
        # SINGLE PARAMETER 
        if len(param_list) == 1:
            return param_list[0] in self.VALID_SINGLE_PARAM
        
        # KEY-VALUE PAIR
        key, value = param_list
        if not key in self.VALID_CONFIG_KEYS:
            return False    
        return self.VALID_CONFIG[key](value)

    def set_param(self, param):
        # Direct language edit
        if 'spanish' == param or 'español' == param:
            self.room_config['language'] = 'Spanish'
        elif 'english' == param or 'inglés' == param or 'ingles' == param:
            self.room_config['language'] = 'English'

         # Direct customs edit
        elif 'customs' == param:
            self.room_config['customs'] = True
        elif 'nocustoms' == param or "sincustoms" == param:
            self.room_config['customs'] = False
                
        # Direct onlycustoms edit
        elif 'onlycustoms' == param:
            self.room_config['onlycustoms'] = True
        elif 'mixto' == param:
            self.room_config['onlyCustoms'] = False
        


    @commands.command()
    async def config(self, ctx, *args):
        """
        Handles explicit configuration. If no other parameters, the current config is shown.
        """
        # Just .config
        if not args:
            return await ctx.send(await self.get_config())
        
        # In case something fails
        ERROR_MODE = False
        error_message = "Operación cancelada:\n"
        config_copy = self.room_config.copy()

        # For every argument
        for word in args:
            param = word.lower().split("=")

            if self.is_valid(param):
                # Explicit parameters (e.g. language=spanish)
                if "=" in word:
                    key, value = param
                    self.room_config[key] = self.SET_CONFIG[key](value)
                
                else: # Implicit parameters
                    self.set_param(param[0])
            else:
                error_message += f"Error al leer el parámetro {word}\n"
                ERROR_MODE = True
            
        if ERROR_MODE:
            self.room_config = config_copy
            return await ctx.send(error_message)

        ready_cog = self.bot.get_cog('ReadyCommands')
        ready_cog.minimo = self.room_config['minimo']

        if self.bot.pinturillo is not None:
            self.bot.update_config()
        
        return await ctx.send("Configuration updated!")
    
    @commands.command(name="", aliases=list(VALID_CONFIG_KEYS))
    async def shortconfig(self, ctx, value = None):
        alias = ctx.invoked_with
        # Invalid command
        if alias not in Config.VALID_CONFIG_KEYS:
            return
        # Send current value for the param
        if value is None:
            return await ctx.send(f'**{alias.capitalize()}:** _{self.room_config[alias]}_')
        
        value = value.lower()

        if not Config.VALID_CONFIG[alias](value):
            return await ctx.send(f'El parámetro **{alias.capitalize()}** no acepta el valor _{value.capitalize()}_.')
        
        self.room_config[alias] = Config.SET_CONFIG[alias](value)
        if self.bot.pinturillo is not None:            
            self.bot.update_config()
        
        ready_cog = self.bot.get_cog('ReadyCommands')
        ready_cog.minimo = self.room_config['minimo']

        return await ctx.send(f'El parámetro **{alias.capitalize()}** ha sido actualizado a _{value.capitalize()}_.')
    
    async def get_config(self):
        """
        Auxiliary method that gets current configuration
        """
        response = "\n**__Current configuration:__**\n"
        for key, value in self.room_config.items():
            response += f"**{key.capitalize()}**: _{value}_\n"
        return response

    @commands.command(aliases=["oldurl", "oldURL", "old_URL", "old_Url"])
    async def old_url(self, ctx, URL = None):
        if URL is None:
            response  = f"La vieja URL es {self.bot.old_URL}" if self.bot.old_URL \
                else f"No tengo ninguna URL aún..."
            return await ctx.send(response)
        
        self.bot.old_URL = URL
        return await  ctx.send('La URL ha sido actualizada')

def setup(bot):
    bot.add_cog(Config(bot))