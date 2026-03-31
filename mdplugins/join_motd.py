import os
from datetime import datetime

from mcdis_rcon.utils import hover_and_run, extras, read_file, write_in_file
from Classes.AeServer import AeServer

class mdplugin():
    def __init__(self, server: AeServer):
        self.server = server
        self.foundation_date = '2024-10-21'
        self.path_motd = os.path.join(self.server.path_plugins, 'join_motd', 'join_messages.txt')

        os.makedirs(os.path.join(self.server.path_plugins, 'join_motd'), exist_ok=True)
        if not os.path.exists(self.path_motd):
            write_in_file(self.path_motd, '')

    async def on_player_join(self, player: str):
        self.show_motd(player)

    async def on_player_command(self, player: str, message: str):
        if self.server.is_command(message, 'mdhelp'):
            self.server.show_command(player, 'motd help', 'Muestra comandos para join-motd')
            self.server.show_command(player, 'join-motd', 'Muestra banner de join-motd')

        if self.server.is_command(message, 'motd help'):
            self.server.show_command(player, 'add-motd <tarea>', 'Añade un mensaje al motd.')
            self.server.show_command(player, 'del-motd <index>', 'Elimina un mensaje del motd.')
            

        if self.server.is_command(message, 'join-motd'):
            self.show_motd(player)
            
   
                                    

        elif not player in self.server.admins:
            return

        elif self.server.is_command(message, 'add-motd'):
            motd = message.removeprefix(f'{self.server.prefix}add-motd').strip()
            self.add_motd(motd)
            self.show_motd(player)
            self.server.send_response(player, '✔ Motd añadido.')

        elif self.server.is_command(message, 'del-motd'):
            index = message.removeprefix(f'{self.server.prefix}del-motd').strip()

            if not index.isnumeric():
                self.server.send_response(player, '✖ El índice debe ser numérico.')
                return

            index = int(index)

            if index > len(self.get_motd()) or index < 1:
                self.server.send_response(player, '✖ No existe un motd con ese índice.')
                return

            self.del_motd(index)
            self.show_motd(player)
            self.server.send_response(player, '✔ Motd eliminado.')

    def show_motd(self, player: str):
        join_messages = self.join_message()

        for message in join_messages:
            message = message.replace('\n', '')
            self.server.execute(f'tellraw {player} {message}')

    def join_message(self):
        years = int(((datetime.today() - datetime.strptime(self.foundation_date, "%Y-%m-%d")).days) // 365.25)
        days = int((datetime.today() - datetime.strptime(self.foundation_date, "%Y-%m-%d")).days % 365.25)

        if years == 0:
            active_days = f'Tiempo activo: {days} días'
        elif days == 0:
            active_days = f'Tiempo activo: {years} años'
        else:
            active_days = f'Tiempo activo: {years} años {days} días'

        join_messages = [
            '{"text" : "§a§lTriskcraft  Server", "color": "green"}',
            '{"text" : "--------------------------"}',
            '{"text" : "Accede a los servidores: ", "color": "white"}\n',
            extras([
                hover_and_run('§l[SMP] ', color='gray', command='/server SMP', hover='/server SMP'),
                hover_and_run('§l[CMP] ', color='gray', command='/server CMP', hover='/server CMP'),
                hover_and_run('§l[MMP] ', color='gray', command='/server Mirror', hover='/server Mirror'),
                hover_and_run('§l[PMP] ', color='gray', command='/server Plugins', hover='/server Plugins'),
                hover_and_run('§l[BNG] ', color='gray', command='/server bingo', hover='/server bingo')
            ], text='', color='white'),
            f'{{"text" : "{active_days}", "color": "white"}}',
            '{"text" : "--------------------------"}',
            '{"text" : "Comandos: §7!!mdhelp        !!task", "color" : "gray"}',
        ]

        extra_messages = self.get_motd()

        if extra_messages:
            join_messages.append('{"text" : "--------------------------"}')
            for i, msg in enumerate(extra_messages):
                join_messages.append(f'{{"text" : "§8[{i + 1}] §r{msg}"}}')

        return join_messages

    def get_motd(self):
        messages = read_file(self.path_motd).strip().split('\n')
        messages = [msg for msg in messages if msg.strip()]
        return messages

    def add_motd(self, message: str):
        content = read_file(self.path_motd).strip().split('\n')
        write_in_file(self.path_motd, '\n'.join(content + [message]))

    def del_motd(self, index: int):
        content = self.get_motd()
        content.pop(index - 1)
        write_in_file(self.path_motd, '\n'.join(content))
