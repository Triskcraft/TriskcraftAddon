import discord
import asyncio
import traceback
import os

from mcdis_rcon.classes import McDisClient
from discord.ext import commands
from datetime import datetime
from typing import Union
import pandas as pd

tickets_log = f'{os.path.dirname(__file__)}/TicketSystem/TicketsLog.csv'
form_log = f'{os.path.dirname(__file__)}/Form/FormsLog.csv'

config = {      
    'Thumbnail'         : 'https://i.postimg.cc/HsmZT5St/Triskcraft-logo.png',
    'Discord Invite'    : 'https://discord.com/invite/VJQJRZehTG',
    'Link YouTube'      : 'https://www.youtube.com/@Triskcraft',
    'Link Twitter'      : 'https://x.com/TriskcraftSMP',
    'Link Twitch'       : 'https://www.twitch.tv/thevugx_',
    'Emoji Server'      : '<:Triskcraft:1349865708196204596>',
    'Emoji Discord'     : '<:Discord:1349581598055596122>',
    'Emoji YouTube'     : '<:Youtube:1349581532213547018>',
    'Emoji Twitch'      : '<:Twitch:1349581616263200889>',
    'Emoji Twitter'     : '<:Twitter:1349581573602807881>',
    'Emoji Overviewer'  : '🌐',
    'Link Overviewer'   : 'https://www.example.com/overviewer',  # Aquí agregamos la clave 'Link Overviewer pagina web de vicho' 
    'Foundation Date'   : '2024-10-21',    
    'Channel ID'        : 1202785595278098492
}


    
config_form = {      
    'Thumbnail'     : 'https://i.postimg.cc/HsmZT5St/Triskcraft-logo.png',  # Miniatura para el formulario
    'Emoji Yes'     : '<:PepeYes:887447915289776159>',  # Emoji "Yes" de Pepe
    'Emoji No'      : '<:PepeNo:887447914291560468>',  # Emoji "No" de Pepe
    'Channel ID'    : 1352825436043739237  # ID de canal para el formulario
}

tickets_config = {      
    'Category ID'   :1221848434198450177,  # ID de categoría para tickets
    'Ticket Moderator ID': 1355617895480164472   # ID del moderador de tickets
}
