import os
import yaml
import discord
from datetime import datetime, timedelta
from discord.ext import commands
from mcdis_rcon.classes import McDisClient
from Classes.AeServer import AeServer

CONFIG_PATH = os.path.join('.mdaddons', 'Config', 'activity.yml')

def ensure_config():
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            yaml.dump({}, f)

def save_activity(username):
    now = datetime.utcnow().isoformat()
    try:
        with open(CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        data = {}
    data[username] = now
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(data, f)

def get_weekly_users():
    try:
        with open(CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        return []
    week_ago = datetime.utcnow() - timedelta(days=7)
    return [
        user for user, timestamp in data.items()
        if datetime.fromisoformat(timestamp) >= week_ago
    ]

class ActivityCog(commands.Cog):
    def __init__(self, client: McDisClient):
        self.client = client

        self.config = {
            'Thumbnail': 'https://i.postimg.cc/HsmZT5St/Triskcraft-logo.png',
            'Embed Colour': 0x2f3136
        }

        ensure_config()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.client.is_command(message.content, 'activity'):
            # Guardar actividad de todos los jugadores conectados en todos los servidores
            for server in self.client.servers:
                server: AeServer
                bots = server.bots
                for player in server.online_players:
                    if player not in bots:
                        save_activity(player)

            await self.send_activity_embed(message.channel)

    @commands.Cog.listener()
    async def on_mc_chat_message(self, username, message):
        if message.strip().lower() == "!!activity":
            for server in self.client.servers:
                server: AeServer
                bots = server.bots
                for player in server.online_players:
                    if player not in bots:
                        save_activity(player)

            users = get_weekly_users()
            if users:
                response = "🧾 Jugadores conectados esta semana:\n» " + "\n» ".join(users)
            else:
                response = "No se ha conectado ningún jugador esta semana."
            await self.client.send_chat_message(response)

    async def send_activity_embed(self, destination):
        users = get_weekly_users()
        n = 30  # máximo de jugadores a mostrar

        if not users:
            embed = discord.Embed(
                title="📅 Actividad semanal",
                colour=self.config['Embed Colour'],
                description="No se ha conectado ningún jugador esta semana."
            )
            embed.set_thumbnail(url=self.config['Thumbnail'])
            await destination.send(embed=embed)
            return

        users = sorted(users)
        show_index = ""
        show_players = ""

        for i, player in enumerate(users[:n], start=1):
            show_index += f"{i:02}\n"
            show_players += f"{player.capitalize():>16}\n"

        embed = discord.Embed(
            title="📅 Actividad semanal",
            colour=self.config['Embed Colour']
        )
        embed.set_footer(
            icon_url='https://cdn.discordapp.com/attachments/1308623970068594729/1349576831375900742/Triskcraft_logo.png?ex=67d39ade&is=67d2495e&hm=89c5dae3be0fd735e49285f0a16f985cf44746e4fb5b0891087c1ae820c25550&',
            text='TriskCraft activity [Top activos - 7 días]'
        )
        embed.set_thumbnail(url=self.config['Thumbnail'])

        embed.add_field(name="‎ ", value=f'```\n{show_index}```', inline=True)
        embed.add_field(name="**Jugador**", value=f'```\n{show_players}```', inline=True)

        await destination.send(embed=embed)

async def setup(client: McDisClient):
    await client.add_cog(ActivityCog(client))
