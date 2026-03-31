import discord
from discord.ext import commands

# IDs de canales
CANAL_BIENVENIDA_ID = 1202732116543152211  # Canal donde se enviará el mensaje de bienvenida
CANAL_DATA_ID = 1202785595278098492        # Canal que se sugiere visitar

class WelcomeSystem:
    def __init__(self, bot):
        self.bot = bot

    async def send_welcome(self, member):
        if member.bot:
            return  # No damos bienvenida a bots

        canal_bienvenida = self.bot.get_channel(CANAL_BIENVENIDA_ID)
        canal_data = self.bot.get_channel(CANAL_DATA_ID)

        if canal_bienvenida and canal_data:
            mensaje = (
                f"👋 ¡Hola {member.mention}, bienvenido a **Triskcraft**! "
                f"Puedes mirar {canal_data.mention} para comenzar."
            )
            await canal_bienvenida.send(mensaje)
        else:
            print("Error: No se encontró uno de los canales de bienvenida o data.")

async def setup(bot):
    welcome_system = WelcomeSystem(bot)

    @bot.event
    async def on_member_join(member):
        await welcome_system.send_welcome(member)

    print("Sistema de bienvenida cargado correctamente")
