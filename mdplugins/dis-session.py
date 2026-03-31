from mcdis_rcon.utils import hover, extras, mc_uuid
from Classes.AeServer import AeServer
import requests
import psycopg
from psycopg import errors

# DSN de PostgreSQL (recomendado moverlo a variables de entorno)
# Formato: "host=... dbname=... user=... password=... port=..."
PG_DSN = "host=localhost dbname=triskcraftdb user=postgres password=N0m3h4k33n! port=5432"


class mdplugin():
    def __init__(self, server: AeServer):
        self.server = server

    @staticmethod
    def online_uuid_to_name(uuid: str) -> str:
        try:
            response = requests.get(
                f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}",
                timeout=5
            )
            if response.status_code == 200:
                return response.json().get("name", "unknown")
            return "unknown"
        except Exception:
            return "unknown"

    async def on_player_command(self, player: str, message: str):
        if self.server.is_command(message, "mdhelp"):
            self.server.show_command(
                player,
                "dis-session",
                "Conectas tu usuario de discord a la sesion actual de minecraft"
            )
            return

        if not self.server.is_command(message, "dis-session"):
            return

        code = message.removeprefix(f"{self.server.prefix}dis-session").strip()
        if not len(code):
            return self.server.send_response(player, "Debes introducir el codigo")

        try:
            # Conexión a PostgreSQL
            with psycopg.connect(PG_DSN) as conn:
                with conn.cursor() as cur:
                    # 1) Buscar el código
                    cur.execute(
                        "SELECT discord_id, discord_nickname FROM link_codes WHERE code = %s",
                        (code,)
                    )
                    res = cur.fetchone()

                    if res is None:
                        return self.server.send_response(
                            player,
                            "Codigo incorrecto, genera uno en discord."
                        )

                    mc_id = mc_uuid(player)
                    discord_id = res[0]
                    discord_nickname = res[1]
                    
                    # 2) Buscar y editar el usuario anterior del si existe o crear uno si no
                    cur.execute("""
                        INSERT INTO minecraft_users (uuid, nickname, discord_user_id)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (uuid)
                        DO UPDATE SET nickname = EXCLUDED.nickname,
                                    discord_user_id = EXCLUDED.discord_user_id
                    """, (mc_id, player, discord_id))

                    # 3) Consumir el código (borrarlo)
                    cur.execute("DELETE FROM link_codes WHERE code = %s", (code,))

                # conn hace COMMIT automático al salir del with si no hubo error

            self.server.send_response(player, f"Enlazado con {discord_nickname}")

        except errors.UniqueViolation:
            # Ej: discord_id ya estaba en uso o mc_id ya enlazado (según constraints)
            self.server.send_response(player, "ya esta enlazado con otro jugador")

        except Exception as e:
            # Error inesperado
            self.server.send_response(player, "Error interno al enlazar. Intenta de nuevo.")
            print(f"Error en dis-session plugin: {e}")
