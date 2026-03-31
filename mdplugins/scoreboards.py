import os
import yaml
import json
from Classes.AeServer import AeServer

class mdplugin():
    def __init__(self, server: AeServer):
        self.server = server
        self.scores_dir = os.path.join(self.server.path_commands, "scores")
        os.makedirs(self.scores_dir, exist_ok=True)

    def get_scoreboards(self):
        return [f.replace('.yml', '') for f in os.listdir(self.scores_dir) if f.endswith('.yml')]

    async def on_player_command(self, player: str, message: str):
        try:
            msg = message.strip()

            if msg == "!!mdhelp":
                self.server.show_command(player, 'score help', 'Opciones para administrar scoreboards.')
                
                for command, description in help_lines:
                    self.server.show_command(player, command, description)
                return
            if msg=="!!score help":
                self.server.show_command(player, 'score', 'Opciones para administrar scoreboards.')

                help_lines = [
                    ('score list', 'Lista todos los scoreboards registrados.'),
                    ('score <nombre>', 'Crea o activa un scoreboard.'),
                    ('score del <nombre>', 'Elimina un scoreboard registrado.'),  
                ]

                for command, description in help_lines:
                    self.server.show_command(player, command, description)
                return


            if msg == "!!score list":
                scores = self.get_scoreboards()
                if not scores:
                    self.server.send_response(player, "No hay scoreboards registrados.")
                    return

                self.server.execute(f'tellraw {player} {json.dumps({"text": "Scoreboards registrados:", "color": "gray"})}')

                for score in sorted(scores):
                    line = {
                        "text": "• ",
                        "color": "gray",
                        "extra": [{
                            "text": score,
                            "color": "gray",
                            "hoverEvent": {
                                "action": "show_text",
                                "value": f"score: {score}"
                            },
                            "clickEvent": {
                                "action": "suggest_command",
                                "value": f"!!{score}"
                            }
                        }]
                    }
                    self.server.execute(f'tellraw {player} {json.dumps(line, ensure_ascii=False)}')
                return

            if msg.startswith("!!score "):
                parts = msg[8:].strip().split()

                # Comando de eliminar
                if len(parts) >= 2 and parts[0] == "del":
                    score_name = parts[1]

                    score_file = os.path.join(self.scores_dir, f"{score_name}.yml")
                    if os.path.exists(score_file):
                        os.remove(score_file)
                        self.server.send_response(player, f"✔ Archivo del scoreboard eliminado: {score_name}")
                    else:
                        self.server.send_response(player, f"✖ No existe archivo registrado para {score_name}")

                    # También eliminar el objetivo en el servidor
                    self.server.execute(f"scoreboard objectives remove {score_name}")
                    self.server.send_response(player, f"✔ Scoreboard removido del servidor: {score_name}")
                    return

                # Crear o activar scoreboard
                score_name = parts[0]
                if not score_name:
                    self.server.send_response(player, "Uso: !!score <nombre> o !!score list")
                    return

                score_file = os.path.join(self.scores_dir, f"{score_name}.yml")
                if not os.path.exists(score_file):
                    with open(score_file, "w", encoding='utf-8') as f:
                        yaml.dump({
                            "description": f"Scoreboard {score_name}",
                            "comandos": [f"scoreboard objectives setdisplay sidebar {score_name}"]
                        }, f)
                    self.server.send_response(player, f"✔ Scoreboard creado: {score_name}")

                self.server.execute(f"scoreboard objectives setdisplay sidebar {score_name}")
                self.server.send_response(player, f"✔ Scoreboard activado: {score_name}")
                return

            if msg.startswith("!!"):
                score_name = msg[2:]
                score_file = os.path.join(self.scores_dir, f"{score_name}.yml")

                if os.path.exists(score_file):
                    self.server.execute(f"scoreboard objectives setdisplay sidebar {score_name}")
                    self.server.send_response(player, f"✔ Scoreboard activado: {score_name}")
                return

        except Exception:
            pass
