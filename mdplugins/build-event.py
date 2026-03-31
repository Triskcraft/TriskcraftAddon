import os
import re

from Classes.AeServer import AeServer

class mdplugin():
    def __init__(self, server: AeServer):
        self.server = server
        self.current_target = {}  # player -> { 'name': str, 'mode': str }
        self.positions = {}       # player -> [pos1, pos2]

    async def on_player_command(self, player: str, message: str):
        try:
            msg = message.strip()


            if self.server.is_command(msg, 'mdhelp'):
                self.server.show_command(player, 'be help', 'Opciones de BuildEvents.')

            elif self.server.is_command(msg, 'be help'):
                self.server.show_command(player, 'be <nombre> <both/break/place>', 'Comenzar creación de evento.')
                self.server.show_command(player, 'be add', 'Añadir un punto (marca posición).')
                self.server.show_command(player, 'be clear', 'Limpiar puntos actuales.')
                self.server.show_command(player, 'be list', 'Mostrar puntos marcados.')

            elif msg.startswith('!!be '):
                parts = msg.split()
                if len(parts) >= 3 and parts[1] not in ('add', 'clear', 'list'):
                    name = parts[1]
                    mode = parts[2].lower()

                    if mode not in ('both', 'break', 'place'):
                        self.server.send_response(player, '✖ Modos válidos: both, break, place.')
                        return

                    self.current_target[player] = {'name': name, 'mode': mode}
                    self.positions[player] = []
                    self.server.send_response(player, f"✔ Evento **{name}** ({mode}) listo. Usa `!!be add` para marcar 2 posiciones.")

                elif len(parts) == 2 and parts[1] == 'add':
                    await self.add_position(player)

                elif len(parts) == 2 and parts[1] == 'clear':
                    self.clear_points(player)

                elif len(parts) == 2 and parts[1] == 'list':
                    self.list_points(player)

        except Exception:
            pass

    async def add_position(self, player: str):
        if player not in self.current_target:
            self.server.send_response(player, "✖ Primero debes usar `!!be <nombre> <both/break/place>`.")
            return

        self.server.execute(f'data get entity {player}')

    async def listener_events(self, log: str):
        if 'has the following entity data:' not in log:
            return

        match = re.search(r"(.*?) has the following entity data: (.*)", log)
        if not match:
            return

        player = match.group(1).strip().split(' ')[-1]
        data = match.group(2)

        if player not in self.current_target:
            return

        raw_pos = data[data.find(', Pos:'):]
        raw_pos = raw_pos[raw_pos.find('[') + 1: raw_pos.find(']')].split(',')

        try:
            x = round(float(raw_pos[0].strip().rstrip('d')))
            y = round(float(raw_pos[1].strip().rstrip('d')))
            z = round(float(raw_pos[2].strip().rstrip('d')))
        except Exception:
            self.server.send_response(player, "✖ Error obteniendo tus coordenadas. Intenta de nuevo.")
            return

        self.positions.setdefault(player, []).append((x, y, z))

        if len(self.positions[player]) == 1:
            self.server.send_response(player, "✔ Primera posición guardada. Usa `!!be add` otra vez para marcar la segunda posición.")
        elif len(self.positions[player]) == 2:
            await self.save_event(player)

    async def save_event(self, player: str):
        if player not in self.current_target or len(self.positions.get(player, [])) < 2:
            self.server.send_response(player, "✖ Faltan posiciones.")
            return

        name = self.current_target[player]['name']
        mode = self.current_target[player]['mode']

        pos1 = self.positions[player][0]
        pos2 = self.positions[player][1]

        # Ordenar coordenadas horizontalmente
        x1 = min(pos1[0], pos2[0])
        z1 = min(pos1[2], pos2[2])

        x2 = max(pos1[0], pos2[0])
        z2 = max(pos1[2], pos2[2])

        # Forzar altura de -64 a 320
        y1 = -64
        y2 = 320

        # Comando completo
        command = f'buildevents add {name} {x1} {y1} {z1} {x2} {y2} {z2} {mode}'

        # Ejecutar en el servidor
        self.server.execute(command)

        self.server.send_response(player, f"✔ Se ejecutó `/buildevents add {name} {x1} {y1} {z1} {x2} {y2} {z2} {mode}`")

        # Limpiar registros
        del self.current_target[player]
        del self.positions[player]

    def clear_points(self, player: str):
        if player in self.positions:
            del self.positions[player]
        if player in self.current_target:
            del self.current_target[player]

        self.server.send_response(player, "✔ Puntos actuales limpiados.")

    def list_points(self, player: str):
        if player not in self.positions or not self.positions[player]:
            self.server.send_response(player, "No tienes puntos guardados.")
            return

        points = self.positions[player]
        messages = []
        for idx, p in enumerate(points, start=1):
            messages.append(f"{idx} • X:{p[0]} Y:{p[1]} Z:{p[2]}")

        if messages:
            self.server.send_response(player, messages)
        else:
            self.server.send_response(player, "No tienes puntos guardados.")
