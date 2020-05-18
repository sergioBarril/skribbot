import discord

import random

from discord.ext import commands

class ReadyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.minimo = 4
        self.ready_list = []
    
    @commands.command(name="ready", aliases=["readyone"])
    async def ready(self, ctx):
        """
        Handles the action if the message received was .ready
        """
        response = ""
        everyone = ctx.invoked_with == "readyone"

        # FIRST MESSAGE
        if self.bot.pinturillo is None and not self.bot.old_URL:
            self.bot.set_pinturillo()
            await self.add_ready(ctx.message.author)
            
            mention = " @everyone" if everyone else ""
            
            response = f"Venga va, ¿quién más se apunta?{mention} ¡Ya hay 1/{self.minimo}!"

        # IF NOT ADDED ALREADY
        elif await self.add_ready(ctx.message.author):
            response = await self.ready_message(ctx.message)

            if len(self.ready_list) >= self.minimo:
                response += " Pero bueno... ¡somos suficientes para que no dé pena!"
                if not self.bot.pinturillo.URL:
                    self.bot.pinturillo.URL = "Loading"
                    await ctx.send("Cargando sala...")
                    self.bot.pinturillo.run()
                    response += f" Aquí tenéis el enlace: {self.bot.pinturillo.URL}"
                
            else:
                response += " Ya somos {}/{}".format(len(self.ready_list), self.minimo)
        
        if response:
            await ctx.send(response)
        

    async def add_ready(self, user):
        """
        Auxiliary method that adds a user to the ready_list. Returns True if added,
        and False if it was already there
        """
        if user not in self.ready_list:
            self.ready_list.append(user)
            return True
        return False

    async def ready_message(self, message):
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

    @commands.command()
    async def unready(self, ctx):
        """
        Handles the message if the content was ".unready"
        """
        if ctx.message.author in self.ready_list:
            self.ready_list.remove(ctx.message.author)
            response = "Terrible, {}. Eso es porque tienes miedo...".format(ctx.message.author.name)
        else:
            response = "Pero si no habías hecho ready, so merluzo."
        
        await ctx.send(response)

    @commands.command(aliases=["readylist", "ready_list"])
    async def readyList(self, ctx):
        """
        Returns the list of people that are Ready
        """
        if not self.ready_list:
            response = "No hay nadie todavía."
        else:
            readyPeople = [person.name for person in self.ready_list]
            stringPeople = ", ".join(readyPeople)
            response = "Gente ready: {}.".format(stringPeople)
        await ctx.send(response)
    
    @commands.command()
    async def voz(self, ctx):
        """
        Mentions everyone who is in the ready_list
        """
        if not self.ready_list:
            return await ctx.send("Ve tú si quieres, pero no hay nadie más...")
        
        guild = ctx.message.guild
        inVoiceChannel = [member for voice_channel in guild.voice_channels for member in voice_channel.members]
        rezagados = [member for member in self.ready_list if member not in inVoiceChannel]

        if rezagados:
            response = f"¡Ya estáis tardando en entrar al chat de voz!"
            for member in rezagados:
                response += f" {member.mention}"
        else:
            response = f"¡Pero si ya estáis todos! Deja de escribir, anda, que ya tenemos todos micro."
        
        await ctx.send(response)

def setup(bot):
    bot.add_cog(ReadyCommands(bot))
    