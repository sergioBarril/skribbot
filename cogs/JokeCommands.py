import discord
from discord.ext import commands

import random

class JokeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # ***********************************
    # #             B R O M A S
    # # ***********************************

    @commands.command(name="", aliases=["terrible", "impugno", "valorar"])
    async def broma(self, ctx):
        IMPUGNO_OPCIONES = [
            "Colorín, colorado, este game está impugnado.",
            "Esta partida queda oficialmente impugnada.",
            "Es que con customs no puedo.",
            "Puto teclado que se me ha quedado pillado.",
            "Es que tengo los dedos de mantequilla.",
            "Está claro: me he dejado.",     
        ]

        VALORAR_OPCIONES = [
                "Un dibujo terrible, 0/10",
                "Por culpa de este dibujo seguimos en Fase 0, 1/10",
                "Mi sobrino de 3 años lo haría mejor, 2/10",
                "Menudo puro, 3/10",
                "Se puede llegar a sacar, pero me faltan tres cervezas, 4/10",
                "Venga, aprobado porque no te quiero volver a ver el año que viene. 5/10",
                "Decente (para ser tú), 6/10",
                "Parecía malo, fue peor, pero al menos lo acerté yo. 7/10",
                "Oye pues ni tan mal,  8/10",
                "Es tan malo que es hasta bueno, 9/10",
                "Yo de ti lo pondría en el currículum, 10/10",
        ]

        TERRIBLE_OPCIONES = [
            "WTF QUÉ BASURA.",
            "Flareon.",
            "Putos customs.",
            "Aaaaaaah pues es verdad es buena. Una buena basura, quiero decir.",
            "Sí hombre, y qué más. Ban",
            "Está partida aún no ha acabado, y yo ya la he impugnado",
            "Puedes estar satisfecho: premio a la mayor basura de la noche",
            "Terriiiiiiiiiiiiible jajajaja",
            "Sigh.",
            "Acertar esto era más difícil que gimpear a GaW",
            "Yikes...",
            "Mira, mejor me callo...",
            f"'{ctx.message.author.name}' is voting to kick este matao (1/2)",
        ]

        router = {
            "impugno" : IMPUGNO_OPCIONES,
            "valorar" : VALORAR_OPCIONES,
            "terrible" : TERRIBLE_OPCIONES,
        }

        ingame_joke = ["terrible"]
        
        alias = ctx.invoked_with
        options = router[alias]
        joke = options[random.randint(0, len(options) - 1)]
        
        if alias in ingame_joke:
            prankturillo = self.bot.new_pinturillo()
            prankturillo.run(URL = self.bot.old_URL)
            prankturillo.type_in_chat(joke)
        else:
            await ctx.send(joke)

def setup(bot):
    bot.add_cog(JokeCommands(bot))