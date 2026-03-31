import discord
from discord.ext import commands, tasks
import requests

TWITCH_CLIENT_ID = "i1tvzhv64gscjhrac7znd5pb943dz3"
TWITCH_ACCESS_TOKEN = "n7act4npuyjnqcqof6qrd7ervpcrve"
TWITCH_USERS = ["snakemateo", "kys_us"]
DISCORD_CHANNEL_ID = 1372448870344429608
ROLE_ID_ALLOWED = 1202775128006459453

notified_streamers = set()

class TwitchLiveNotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_streams.start()

    def cog_unload(self):
        self.check_streams.cancel()

    @tasks.loop(minutes=1)
    async def check_streams(self):
        headers = {
            "Client-ID": TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}"
        }

        for user in TWITCH_USERS:
            response = requests.get(f"https://api.twitch.tv/helix/streams?user_login={user}", headers=headers)

            if response.status_code != 200:
                continue

            data = response.json()
            if data.get("data"):
                if user not in notified_streamers:
                    stream = data["data"][0]
                    title = stream["title"]
                    game_name = stream.get("game_name", "Jugando algo")
                    thumbnail_url = stream["thumbnail_url"].replace("{width}", "1280").replace("{height}", "720")
                    url = f"https://twitch.tv/{user}"

                    embed = discord.Embed(
                        title=f"{title}",  
                        color=0x9146FF,
                        url=url  
                    )
                    embed.set_author(name=user) 
                    embed.set_image(url=thumbnail_url + f"?cache={stream['id']}")  
                    embed.set_footer(
                        text=f"Twitch Stream - {game_name}",
                        icon_url="https://static.twitchcdn.net/assets/favicon-32-e29e246c157142c94346.png" 
                    )

                    channel = self.bot.get_channel(DISCORD_CHANNEL_ID)
                    if channel:
                        await channel.send(f"Ey! **{user}** está en directo, pásate por ahí @everyone")
                        await channel.send(embed=embed)

                    notified_streamers.add(user)
            else:
                if user in notified_streamers:
                    notified_streamers.remove(user)

    @check_streams.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

    @commands.hybrid_group(name="twitch", with_app_command=True, description="Gestiona los usuarios de Twitch a notificar")
    async def twitch(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Usa `/twitch add <usuario>`, `/twitch remove <usuario>` o `/twitch list`")

    @twitch.command(name="add", description="Añade un usuario de Twitch a la lista de notificación")
    @commands.has_role(ROLE_ID_ALLOWED)
    async def add(self, ctx, usuario: str):
        usuario = usuario.lower()
        if usuario in TWITCH_USERS:
            await ctx.send(f"El usuario `{usuario}` ya está en la lista.")
        else:
            TWITCH_USERS.append(usuario)
            await ctx.send(f"Usuario `{usuario}` añadido a la lista de notificaciones.")

    @twitch.command(name="remove", description="Quita un usuario de Twitch de la lista de notificación")
    @commands.has_role(ROLE_ID_ALLOWED)
    async def remove(self, ctx, usuario: str):
        usuario = usuario.lower()
        if usuario not in TWITCH_USERS:
            await ctx.send(f"El usuario `{usuario}` no está en la lista.")
        else:
            TWITCH_USERS.remove(usuario)
            if usuario in notified_streamers:
                notified_streamers.remove(usuario)
            await ctx.send(f"Usuario `{usuario}` removido de la lista de notificaciones.")

    @twitch.command(name="list", description="Muestra la lista de usuarios Twitch que se notifican")
    async def list(self, ctx):
        if not TWITCH_USERS:
            await ctx.send("No hay usuarios en la lista de notificaciones.")
            return

        lista = "\n".join(f"- {user}" for user in TWITCH_USERS)
        embed = discord.Embed(
            title="Usuarios Twitch monitorizados",
            description=lista,
            color=0x9146FF
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TwitchLiveNotify(bot))
