import subprocess
import asyncio
from Classes.AeServer import AeServer

class mdplugin():
    def __init__(self, server: AeServer):
        self.server = server
        self.script_path = '/home/ubuntu/Server/consola/terminal.py'  # Ruta del script
    async def on_player_command(self, player: str, message: str):
        if not player in self.server.admins:
            return
        
        elif self.server.is_command(message, 'mdhelp'):
            self.server.show_command(player, 'console'           , 'Comando para manejar la terminal en discord')    

    async def on_player_command(self, player: str, message: str):
        """Ejecuta el script cuando se usa !!console en Minecraft"""
        if self.server.is_command(message, 'console'):
            output = await self.run_terminal_script()
            # Ahora, si deseas que el mensaje sea enviado al jugador, puedes hacerlo aquí
            self.server.send_response(player, output)

    async def run_terminal_script(self):
        """Ejecuta el script terminal.py y devuelve su salida"""
        try:
            # Ejecutar el script de manera asíncrona
            process = await asyncio.create_subprocess_exec(
                'python3', self.script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            # Verificar la salida estándar (stdout) o de error (stderr)
            if stdout:
                return stdout.decode().strip()
            elif stderr:
                return f"Error: {stderr.decode().strip()}"
            return "Script ejecutado sin salida."
        except Exception as e:
            return f"Error inesperado: {str(e)}"
