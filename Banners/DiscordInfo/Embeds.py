from .Modules import *
import discord
from datetime import datetime

def apply_en_embed() -> list[discord.Embed]:
    embeds = [
        discord.Embed(
            title='Application Steps',
            colour=0x9BBEC8,
            description=(
                '1. Click the **Tickets** button to access the application form.\n'
                '2. Fill out the form with detailed and thoughtful answers.\n'
                '3. Use the ticket to interact with our team during the interview process.\n\n'
                'Take your time—this is your chance to make a great first impression!'
            )
        ).set_footer(text="We’re looking forward to meeting you!"),

        discord.Embed(
            title='Join TriskCraft',
            colour=0xDDF2FD,
            description='We’re excited to have you join our community! Follow the steps below to become part of TriskCraft.'
        ).set_author(name="TriskCraft SMP", icon_url=config['Thumbnail']),
    ]
    return embeds

def apply_es_embed() -> list[discord.Embed]:
    embeds = [
        discord.Embed(
            title='Pasos para Aplicar',
            colour=0x9BBEC8,
            description=(
                '1. Haz clic en el botón **Tickets** para acceder al formulario de aplicación.\n'
                '2. Completa el formulario con respuestas detalladas y cuidadosas.\n'
                '3. Usa el ticket para interactuar con nuestro equipo durante el proceso de entrevista.\n\n'
                'Tómate tu tiempo—¡es tu oportunidad de causar una buena primera impresión!'
            )
        ).set_footer(text="¡Esperamos conocerte pronto!"),

        discord.Embed(
            title='Únete a TriskCraft',
            colour=0xDDF2FD,
            description='¡Estamos emocionados de que te unas a nuestra comunidad! Sigue los pasos a continuación para ser parte de TriskCraft.'
        ).set_author(name="TriskCraft SMP", icon_url=config['Thumbnail']),
    ]
    return embeds

def banner_en_embed():
    years = int(((datetime.today() - datetime.strptime(config['Foundation Date'], "%Y-%m-%d")).days) // 365.25)
    days = int((datetime.today() - datetime.strptime(config['Foundation Date'], "%Y-%m-%d")).days % 365.25)

    active_days = f'{years} years {days} days' if years and days else f'{years or days} {"years" if years else "days"}'

    embed = discord.Embed(
        title='About TriskCraft',
        colour=0x2f3136,
        description='Welcome to TriskCraft, a technical and decorative Minecraft server where we build amazing projects and have fun together.'
    ).add_field(
        name='Server Information',
        value=(f'**Active Time:** {active_days}\n'
               f'**Founded:** {config["Foundation Date"].replace("-","/")}\n'
               f'**Version:** 1.21'),
        inline=True
    ).add_field(
        name='Important Links',
        value=(f'{config["Emoji Overviewer"]} [Overviewer]({config["Link Overviewer"]})\n'
               f'{config["Emoji YouTube"]} [YouTube]({config["Link YouTube"]})\n'
               f'{config["Emoji Discord"]} [Discord]({config["Discord Invite"]})\n'
               f'{config["Emoji Twitter"]} [Twitter]({config["Link Twitter"]})\n'
               f'{config["Emoji Twitch"]} [Twitch]({config["Link Twitch"]})'),
        inline=True
    ).add_field(
        name='How to Join',
        value='Click the **Apply** button and follow the instructions to start your journey with us!',
        inline=False
    ).add_field(
        name='Server Specifications',
        value=(

            '\n🟢 • Processor: Intel Xeon E2386G\n'
            '🟡 • Location: Germany\n'
            '🟢 • Servers: SMP, Mirror, CMP, Plugins\n'
            '\n\nFor more details, feel free to ask a staff member.'
        ),
        inline=False
    ).set_thumbnail(url=config['Thumbnail']) \
    .set_footer(text='Switch to Spanish using the Es button.')
    
    return embed

def banner_es_embed():
    years = int(((datetime.today() - datetime.strptime(config['Foundation Date'], "%Y-%m-%d")).days) // 365.25)
    days = int((datetime.today() - datetime.strptime(config['Foundation Date'], "%Y-%m-%d")).days % 365.25)

    active_days = f'{years} años {days} días' if years and days else f'{years or days} {"años" if years else "días"}'

    embed = discord.Embed(
        title='Sobre TriskCraft',
        colour=0x2f3136,
        description='Bienvenido a TriskCraft, un servidor de Minecraft técnico decorativo donde construimos proyectos increíbles y nos divertimos juntos.'
    ).add_field(
        name='Información del Servidor',
        value=(f'**Tiempo Activo:** {active_days}\n'
               f'**Fundación:** {config["Foundation Date"].replace("-","/")}\n'
               f'**Versión:** 1.21'),
        inline=True
    ).add_field(
        name='Enlaces Importantes',
        value=(f'{config["Emoji Overviewer"]} [Overviewer]({config["Link Overviewer"]})\n'
               f'{config["Emoji YouTube"]} [YouTube]({config["Link YouTube"]})\n'
               f'{config["Emoji Discord"]} [Discord]({config["Discord Invite"]})\n'
               f'{config["Emoji Twitter"]} [Twitter]({config["Link Twitter"]})\n'
               f'{config["Emoji Twitch"]} [Twitch]({config["Link Twitch"]})'),
        inline=True
    ).add_field(
        name='Cómo Unirse',
        value='Haz clic en el botón **Apply** y sigue las instrucciones para comenzar tu aventura con nosotros.',
        inline=False
    ).add_field(
        name='Especificaciones del Servidor',
        value=(
            '\n🟢 • Procesador: Ryzen 7 9700x\n'
            '🟡 • Ubicación: Francia\n'
            '🟢 • Servidores: SMP, Mirror, CMP, Plugins\n'
            '\n\nPara más detalles, pregunta a un miembro del staff.'
        ),
        inline=False
    ).set_thumbnail(url=config['Thumbnail']) \
    .set_footer(text='Switch to Spanish using the Es button.')  # Este texto se mantiene como estaba.
    
    return embed

def hardware_info_en_embed() -> discord.Embed:
    embed = discord.Embed(
        title='TriskCraft Hardware Details',
        colour=0x2f3136
    ).add_field(
        name='Host Information',
        value=(
            '\n• Type: Dedicated Server\n'
            '• Location: Germany\n'
            '• Processor: Intel Xeon E2386G\n'
            '• Servers: SMP, Mirror, CMP, Plugins\n'
        ),
        inline=False
    ).add_field(
        name='Server Mods',
        value=(
            '\n- Syncmatica\n'
            '- EssentialCarefulBreak\n'
            '- Starlight\n'
            '- Lithium\n'
            '- PCA-Protocol\n'
        ),
        inline=True
    ).add_field(
        name='Server Rules',
        value=(
            '\n- AccurateBlockPlacement\n'
            '- CombineXPOrbs\n'
            '- MissingTools\n'
            '- OptimizedTNT\n'
            '- ShadowItemsFix\n'
        ),
        inline=True
    )
    return embed

def hardware_info_es_embed() -> discord.Embed:
    embed = discord.Embed(
        title='Detalles del Hardware de TriskCraft',
        colour=0x2f3136
    ).add_field(
        name='Información del Host',
        value=(
            '\n• Tipo: Servidor Dedicado\n'
            '• Ubicación: Francia\n'
            '• Procesador: Ryzen 7 9700x\n'
            '• Servidores: SMP, Mirror, CMP, Plugins\n'
        ),
        inline=False
    ).add_field(
        name='Mods del Servidor',
        value=(
            '\n- Syncmatica\n'
            '- EssentialCarefulBreak\n'
            '- Starlight\n'
            '- Lithium\n'
            '- PCA-Protocol\n'
        ),
        inline=True
    ).add_field(
        name='Reglas del Servidor',
        value=(
            '\n- AccurateBlockPlacement\n'
            '- CombineXPOrbs\n'
            '- MissingTools\n'
            '- OptimizedTNT\n'
            '- ShadowItemsFix\n'
        ),
        inline=True
    )
    return embed

def rules_en_embed() -> list[discord.Embed]:
    embeds = [
        discord.Embed(
            title='TriskCraft Rules',
            colour=0xDDF2FD,
            description='To ensure a positive experience for everyone, please follow these rules while on the server.'
        ).set_author(name="TriskCraft SMP", icon_url=config['Thumbnail']),

        discord.Embed(
            title='Terms of Service',
            colour=0x164863,
            description='By participating in this server, you agree to Discord’s terms of service: [[Discord TOS]](https://discord.com/terms).'
        ).set_footer(text='Violating these rules may result in a ban.'),

        discord.Embed(
            title='Voice Channels',
            colour=0x427D9D,
            description='Be respectful in voice channels. Avoid disruptive behavior and sensitive topics like politics or sports.'
        ),

        discord.Embed(
            title='Text Channels',
            colour=0x9BBEC8,
            description='Keep text channels friendly and productive. Avoid spamming, inappropriate content, or controversial topics.'
        )
    ]
    return embeds

def rules_es_embed() -> list[discord.Embed]:
    embeds = [
        discord.Embed(
            title='Reglas de TriskCraft',
            colour=0xDDF2FD,
            description='Para garantizar una experiencia positiva para todos, por favor sigue estas reglas mientras estés en el servidor.'
        ).set_author(name="TriskCraft SMP", icon_url=config['Thumbnail']),

        discord.Embed(
            title='Términos del Servicio',
            colour=0x164863,
            description='Al participar en este servidor, aceptas los términos de servicio de Discord: [[Discord TOS]](https://discord.com/terms).'
        ).set_footer(text='Incumplir estas reglas puede resultar en un baneo.'),

        discord.Embed(
            title='Canales de Voz',
            colour=0x427D9D,
            description='Sé respetuoso en los canales de voz. Evita comportamientos disruptivos y temas sensibles como política o deportes.'
        ),

        discord.Embed(
            title='Canales de Texto',
            colour=0x9BBEC8,
            description='Mantén los canales de texto amigables y productivos. Evita el spam, contenido inapropiado o temas polémicos.'
        )
    ]
    return embeds