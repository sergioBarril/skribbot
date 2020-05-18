import discord
from discord.ext import commands

import random

class GameManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    # # **************************************
    # #      G A M E     M A N A G E M E N T
    # # **************************************

    @commands.command()
    async def replay(self, ctx):
        if self.bot.pinturillo:
            self.bot.pinturillo.quit()

        await ctx.send("Creando nueva sala...")
        self.bot.set_pinturillo()
        self.bot.pinturillo.run()

        self.bot.old_URL = ""
        
        await ctx.send(f'¡Oído cocina! Aquí tienes el enlace de la nueva sala: {self.bot.pinturillo.URL}')
        
    @commands.command()
    async def link(self, ctx):
        """
        Returns current link (or previous, if the game has already started)
        """
        if self.bot.pinturillo and self.bot.pinturillo.URL:
            response  = f"Aquí tienes: {self.bot.pinturillo.URL}"

        elif not self.bot.old_URL:
            response = f"Aún no he abierto ninguna sala..."

        else:
            response = f"La última vez los dejé en {self.bot.old_URL}... ¿Si corres quizá los pillas?"
            
        return await ctx.send(response)

    @commands.command()
    async def start(self, ctx):
        """
        Handles the start of the game (emptying the readyList, and closing the browser window)
        """
        if self.bot.pinturillo is None:
            return await ctx.send(
                "Start qué, si no aún no hay nada preparado... Haz .ready anda"
            )
        
        if not self.bot.pinturillo.URL or self.bot.pinturillo.URL == "Loading...":
            return await ctx.send(
                "Aún no estamos en la sala, cálmate y dale a .ready si no lo has hecho ya"
            )
        
        if self.bot.pinturillo.start_game():
            self.bot.old_URL = self.bot.pinturillo.URL
            self.bot.pinturillo = None
            self.bot.ready_list = []
            return await ctx.send("¡A jugarrrr~!")
        
        return await ctx.send("Estoy yo solo todavía, espera a que entre la gente")

def setup(bot):
    bot.add_cog(GameManagement(bot))
    