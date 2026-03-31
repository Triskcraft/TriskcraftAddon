import discord
import asyncio
import shutil
import sys
import os

from mcdis_rcon.classes import McDisClient, Network

class mdaddon():
    def __init__(self, client: McDisClient):
        """Inicializa el addon con el cliente de McDisClient"""
        self.client = client
        self.persistent_tasks = []
        self.config_mdplugins = {
            'SMP':  ['manager.py', 'chatbridge.py', 'join_motd.py', 'calc.py','here.py', 'execute.py', 'reg-bkps.py', 'scoreboard.py','finder.py','terminal.py','tts_addon.py','scoreboards.py','build-event.py','bot.py','ow.py','dis-session.py'],
            'CMP':  ['manager.py', 'chatbridge.py', 'join_motd.py', 'calc.py','here.py', 'op.py', 'execute.py','online.py','finder.py','tts_addon.py','bot.py'],
            'Mirror':['manager.py', 'chatbridge.py', 'join_motd.py', 'calc.py','here.py', 'op.py', 'reg-updater.py', 'execute.py','finder.py','tts_addon.py','_maker.py','md-bkps.py','bot.py'],
            'SMP 1.12':['manager.py', 'chatbridge.py', 'join_motd.py', 'calc.py','here.py', 'op.py', 'reg-updater.py', 'execute.py','finder.py','tts_addon.py','_maker.py','md-bkps.py','bot.py'],
            'Bingo': ['manager.py', 'chatbridge.py', 'join_motd.py', 'calc.py','here.py', 'op.py', 'reg-updater.py', 'execute.py','finder.py','tts_addon.py','bot.py'],
            'Plugins': ['manager.py', 'chatbridge.py', 'here.py']
        }
        
        print('     -> Cargando AeExtensions')

        # Asegura que la ruta de los addons esté en sys.path
        if self.client.path_addons not in sys.path: 
            sys.path.insert(0, self.client.path_addons)

        # Cargar los complementos relacionados con el bot
        asyncio.create_task(self.load())

        # Actualiza las clases de los servidores
        self.update_server_classes()

        # Administra los plugins de MD
        self.manage_mdplugins()
        

    def manage_mdplugins(self) -> None:
        """Gestiona los plugins de md para cada proceso del cliente."""
        available_mdplugins = os.listdir(os.path.join(self.client.path_addons, 'mdplugins'))

        # Recorre los procesos del cliente
        for process in self.client.processes:
            if process.name not in self.config_mdplugins:
                continue
            
            # Elimina plugins antiguos que no estén en la lista configurada
            for plugin in os.listdir(process.path_plugins):
                plugin_path = os.path.join(process.path_plugins, plugin)
                if not os.path.isdir(plugin_path): 
                    os.remove(plugin_path)

            # Copia los nuevos plugins configurados
            for plugin in self.config_mdplugins[process.name]:
                if plugin not in available_mdplugins:
                    continue
                source = os.path.join(self.client.path_addons, 'mdplugins', plugin)
                dest = os.path.join(process.path_plugins, plugin)

                shutil.copy(source, dest)

            # Recarga los plugins del proceso
            process.load_plugins(reload=True)

    async def load(self) -> None:
        """Carga los cogs y tareas persistentes del bot."""
        # Cargar cogs: Commands, ContextMenus, Behaviours
        cogs = ['Commands', 'Behaviours']

        for cog in cogs:
            cog_path = os.path.join(self.client.path_addons, cog)
            os.makedirs(cog_path, exist_ok=True)
            scripts = [file.removesuffix('.py') for file in os.listdir(cog_path) if file.endswith('.py')]

            for script in scripts:
                extension = f"{cog}.{script}"
                
                # Descarga cualquier extensión cargada previamente
                if extension in self.client.extensions:
                    await self.client.unload_extension(extension)

                # Carga la nueva extensión
                await self.client.load_extension(extension)
        
        # Sincroniza el árbol de comandos
        await self.client.tree.sync()

        # Crear tareas persistentes para los banners
        

        from Banners.MembersInfo.Creator import members_creator, members_extras
        asyncio.create_task(members_extras(self.client))
        task = asyncio.create_task(members_creator(self.client))
        self.persistent_tasks.append(task)

        from Banners.DiscordInfo.Creator import discord_creator, discord_extras
        asyncio.create_task(discord_extras(self.client))
        task = asyncio.create_task(discord_creator(self.client))
        self.persistent_tasks.append(task)

        # Establecer el estado inicial del bot
        initial_status = discord.CustomActivity(name="triskcraft SMP")

        await self.client.change_presence(
            activity=initial_status,
            status=discord.Status.online
        )

    def update_server_classes(self) -> None:
        """Actualiza las clases de servidores en el cliente, asegurándose de que se instancian correctamente."""
        from Classes.AeServer import AeServer

        # Si ya son instancias de AeServer, no es necesario hacer nada
        if all(isinstance(x, AeServer) for x in self.client.servers): 
            return

        # Filtra los procesos para asegurarse de que sean de tipo Network
        self.client.processes = [x for x in self.client.processes if isinstance(x, Network)]
        self.client.servers = []

        # Crea nuevos servidores basados en la configuración
        for name, config in self.client.config['Processes']['Servers'].items():
            server = AeServer(name, self.client, config)
            self.client.processes.append(server)
            self.client.servers.append(server)
            print(f'        • {name} -> {server.__class__.__name__}')

    def unload(self) -> None:
        """Cancela las tareas persistentes del addon."""
        for task in self.persistent_tasks:
            task.cancel()
