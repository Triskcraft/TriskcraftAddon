from .TaskLog import show_tasks
from .Modules import *
import traceback
import asyncio
import os
import discord
from datetime import datetime

async def thread(name: str, channel: discord.TextChannel):
    """Busca un thread activo por nombre dentro del canal especificado."""
    threads = await channel.guild.active_threads()
    for t in threads:
        if t.name == name and t.parent_id == channel.id:
            return t
    raise ValueError(f"No se encontró el thread '{name}' en el canal {channel.name}")

async def members_creator(client: McDisClient, loop: bool = True):
    """Este proceso actualiza el canal con un banner y mensajes de bienvenida."""
    channel = client.get_channel(config['Channel ID'])

    while True:
        try:
            messages = [msg async for msg in channel.history(limit=None, oldest_first=True)]
            banner_image = discord.File(os.path.join(os.path.dirname(__file__), 'Banner.png'))
            banner = await banner_embed(client)

            if len(messages) == 0:
                await channel.send(embed=banner, file=banner_image)
            elif len(messages) == 1 and messages[0].author.id == client.user.id:
                await messages[0].edit(embed=banner)
            else:
                await channel.purge(limit=100)
                continue

            if not loop:
                break

        except asyncio.CancelledError:
            return

        except Exception:
            print(f'Error:\n{traceback.format_exc()}')

        else:
            await asyncio.sleep(24 * 60 * 60)

async def members_extras(client: McDisClient):
    """Carga y descarga extensiones adicionales para tareas y comportamientos de miembros."""
    from .TaskLog import update_log
    await update_log(client)

    extensions = ["Banners.MembersInfo.TaskCommand", "Banners.MembersInfo.TaskBehaviour"]
    
    for extension in extensions:
        if extension in client.extensions:
            await client.unload_extension(extension)
        await client.load_extension(extension)

    await client.tree.sync()

async def banner_embed(client: McDisClient) -> discord.Embed:
    """Genera un embed con la información del servidor y tareas actuales."""
    years = int(((datetime.today() - datetime.strptime(config['Foundation Date'], "%d/%m/%Y")).days) // 365.25)
    days = int((datetime.today() - datetime.strptime(config['Foundation Date'], "%d/%m/%Y")).days % 365.25)
    channel = client.get_channel(config['Channel ID'])

    try:
        announcements = await thread('Announcements', channel)
    except ValueError:
        msg = await channel.send("Creando hilo de anuncios...")
        announcements = await msg.create_thread(
            name='Announcements',  # Corregí el typo 'Announcements'
            reason='Hilo para anuncios importantes del servidor'
        )
        await msg.delete()

    if years == 0:
        active_days = f'Tiempo activo: {days} días'
    elif days == 0:
        active_days = f'Tiempo activo: {years} años'
    else:
        active_days = f'Tiempo activo: {years} años {days} días'

    # Evitar errores si alguna clave falta en config, usando get con valor por defecto
    ip_server = config.get("IP Server", "Desconocida")
    ip_all_the_mods = config.get("IP All The Mods", "Desconocida")
    seed = config.get("Seed", "Desconocido")
    discord_invite = config.get("Discord Invite", "#")
    link_youtube = config.get("Link YouTube", "#")
    link_twitter = config.get("Link Twitter", "#")
    link_twitch = config.get("Link Twitch", "#")
    thumbnail = config.get("Thumbnail", "")

    embed = discord.Embed(
        title='Bienvenido a TriskCraft',
        description='Un servidor técnico decorativo donde construimos proyectos increíbles y nos divertimos juntos.',
        colour=0x2f3136
    ).add_field(
        name='> Información del Servidor',
        value=(
            f'||```prolog\n'
            f'Ip:                                         {ip_server}\n'
            f'Ip All The Mods:                                         {ip_all_the_mods}\n'
            f'Seed:                                       {seed}```||\n'
        ),
        inline=False
    ).add_field(
        name='> Tiempo Activo',
        value=active_days,
        inline=True
    ).add_field(
        name='> Anuncios Importantes',
        value=f'Revisa los últimos anuncios en <#{announcements.id}>.',
        inline=True
    ).add_field(
        name='> Reglas del Servidor',
        value=(
            '- No filtrar mecanismos fuera del servidor.\n'
            '- No se tolerará ningún tipo de toxicidad.\n'
            '- Quien grifee el servidor será baneado permanentemente.\n'
            '- Está prohibido generar mundo sin razón.\n'
            '- Quien filtre la ip será baneado del servidor permanentemente.\n'
        ),
        inline=False
    ).add_field(
        name='> Tareas de Proyectos',
        value=show_tasks(client),
        inline=False
    ).add_field(
        name='> Consejos para Nuevos Miembros',
        value=(
            '- Usa los `tickets` si necesitas ayuda.\n'
            '- Revisa los canales de texto para más información.\n'
            '- ¡No dudes en preguntar si tienes dudas!'
        ),
        inline=False
    ).add_field(
        name='> Enlaces Útiles',
        value=(
            f'<:discord:1349581598055596122> [Discord]({discord_invite}) | '
            f'<:youtube:1349581532213547018> [YouTube]({link_youtube}) | '
            f'<:twitter:1349581573602807881> [Twitter]({link_twitter}) | '
            f'<:twitch:1349581616263200889> [Twitch]({link_twitch})'
        ),
        inline=False
    ).set_thumbnail(url=thumbnail) \
    .set_footer(text='¡Diviértete y construye algo increíble!')

    return embed
