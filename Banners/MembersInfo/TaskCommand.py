import discord
from discord import app_commands, Interaction
from discord.ext import commands
from discord.app_commands import Choice, describe

from .Creator import members_creator
from .Modules import *
from .TaskLog import *

GUILD_ID = 1202732116102877246  # ID de tu servidor de Discord (TriskCraft)

class TaskCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name='task',
        description='Administra los hilos de tareas',
        extras={'rank': 3}
    )
    @describe(name='Nombre del hilo de tareas')
    @describe(action='Acción que quieres hacer con el hilo')
    @app_commands.choices(action=[Choice(name=i, value=i) for i in ['Create', 'Close']])
    async def task_command(self, interaction: Interaction, action: Choice[str], name: str):
        if not isAdmin(interaction.user):
            await interaction.response.send_message('✖ No tienes permisos.', ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        channel = interaction.channel
        dummy = [thread for thread in channel.threads if thread.name.lower() == name.lower() and is_task(thread)]

        if action.value == 'Create':
            if dummy:
                await interaction.followup.send('✖ Ya existe una tarea con ese nombre.')
                return

            message = await channel.send('Hilo público creado.')
            thread = await message.create_thread(name=name.strip())
            await message.delete()

            new_log(thread)
            await members_creator(self.client, loop=False)

            await interaction.followup.send('✔ Tarea creada correctamente.')

        elif action.value == 'Close':
            if not dummy:
                await interaction.followup.send('✖ No existe una tarea con ese nombre.')
                return

            thread = dummy[0]
            await thread.delete()
            del_log(thread)
            await members_creator(self.client, loop=False)

            await interaction.followup.send('✔ Tarea cerrada correctamente.')

async def setup(client: commands.Bot):
    await client.add_cog(TaskCommand(client))
    await client.tree.sync(guild=discord.Object(id=GUILD_ID))  # Registro rápido en tu servidor
    print('[TaskCommand] Slash commands sincronizados en TriskCraft.')
