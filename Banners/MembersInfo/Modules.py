import pandas as pd
import numpy as np
import discord
import asyncio
import traceback
import os
import sys

from mcdis_rcon.utils import isAdmin, thread
from mcdis_rcon.classes import McDisClient

from discord.app_commands import describe, choices, Choice
from discord.ext import commands
from datetime import datetime

tasks_log = os.path.join(os.path.dirname(__file__), 'TasksLog.csv')

config = {      
    'Thumbnail'         : 'https://i.postimg.cc/HsmZT5St/Triskcraft-logo.png',
    'Emoji Server'      : '<1349865708196204596>',
    'Foundation Date'   : '21/10/2024',
    'IP Server'         : 'mc.triskcraft.com',
    'Seed'              : '-1412583731547517931',
    'Channel ID'        : 1353433284545089587, 
    'Discord Invite'    : 'https://discord.com/invite/VJQJRZehTG',
    'Link YouTube'      : 'https://www.youtube.com/@Triskcraft',
    'Link Twitter'      : 'https://x.com/TriskcraftSMP',
    'Link Twitch'       : 'https://www.twitch.tv/thevugx_',
}
