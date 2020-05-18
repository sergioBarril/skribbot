import discord
from discord.ext import commands

import os

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def screenshot(self, ctx):
        fotorillo = self.bot.new_pinturillo()
        fotorillo.run(self.bot.old_URL)

        filename = fotorillo.screenshot()
        fotorillo.quit()

        try:
            await ctx.send(file=discord.File(f'{filename}'))
            os.remove(filename)
        except:
            await ctx.send("Error")
    

    # # *********************************
    # #            H E L P
    # # *********************************
    @commands.command()
    async def help(self, ctx):
        channel_message = f'Perfecto, {ctx.message.author.mention}, te he enviado los comandos por MD.'
        direct_message = (
            f"¡Hola! Al habla Skribbot ({self.bot.VERSION}). Aquí van los diferentes comandos:\n\n"
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
            ".terrible : Lanza este comando para que el bot entre a tu partida a valorar el dibujo.\n\n"
            ".screenshot : Lanza este comando para hacer un screenshot de la partida actual.\n\n"
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

        await ctx.message.author.send(direct_message)
        await ctx.send(channel_message)

def setup(bot):
    bot.add_cog(OtherCommands(bot))
