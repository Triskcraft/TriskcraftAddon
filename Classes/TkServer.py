import os
import yaml
from datetime import datetime
from mcdis_rcon.classes import Server, McDisClient

ACTIVITY_FILE = os.path.join('.mdaddons', 'Config', 'activity_sessions.yml')

def now():
    return datetime.utcnow().isoformat()

class tkServer(Server):
    def __init__(self, name: str, client: McDisClient, config: dict):
        super().__init__(name, client, config)

        os.makedirs(os.path.dirname(os.path.join(self.path, ACTIVITY_FILE)), exist_ok=True)
        self.activity_path = os.path.join(self.path, ACTIVITY_FILE)
        self.sessions = {}  # jugador -> hora de entrada
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.activity_path):
            with open(self.activity_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    def save_data(self):
        with open(self.activity_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f, allow_unicode=True)

    async def on_player_join(self, player: str):
        now_time = now()
        self.sessions[player] = now_time
        self.data.setdefault(player, []).append({'join': now_time})
        self.save_data()

    async def on_player_left(self, player: str):
        now_time = now()
        if player in self.sessions:
            join_time = self.sessions.pop(player)
            for session in reversed(self.data.get(player, [])):
                if 'join' in session and 'leave' not in session:
                    session['leave'] = now_time
                    break
            self.save_data()

    def unload(self):
        self.save_data()
