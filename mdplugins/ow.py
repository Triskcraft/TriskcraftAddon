from mcdis_rcon.utils import hover, extras, hover
from Classes.AeServer import AeServer

class mdplugin():
    def __init__(self, server: AeServer):
        self.server = server

    async def on_player_command(self, player: str, message: str):

        if self.server.is_command(message, 'vic'):
            self.server.execute(f'view inv {player}')
        
        elif self.server.is_command(message, 'mdhelp'):
            self.server.show_command(player, f"Vic", "Comando reservado solo para Owners.")