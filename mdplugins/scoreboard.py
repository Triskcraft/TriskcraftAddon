import os
import discord
import math

from mcdis_rcon.utils import read_dat_files
from Classes.AeServer import AeServer

class mdplugin():
    def __init__(self, server: AeServer):
        self.server = server
        self.scoreboards_len = 30

    def format_value(self, value):
        return f'{value:,}'

    async def listener_on_message(self, message: discord.Message):
        if message.author.bot:
            return
        elif message.content.lower().strip() == '!!digs':
            scores = self.digs_scores()
            embed = self.digs_embed(scores)
            view = ScoreboardView(self, 'TriskCraft digs', scores)
            await message.channel.send(embed=embed, view=view)

    def digs_scores(self):
        path = os.path.join(self.server.path_files, 'server', 'world', 'data', 'scoreboard.dat')
        data = read_dat_files(path)

        scores = []
        total = 0
        for x in data['data']['PlayerScores']:
            if x['Objective'] == 'digs':
                score = int(x['Score'])
                if score > 0:  # Solo agregar si tiene más de 0
                    scores.append({"player": x['Name'], "score": score})
                    total += score

        scores.sort(key=lambda x: x['score'], reverse=True)
        scores.insert(0, {"player": 'Total', "score": total})
        return scores

    def digs_embed(self, scores: list, page: int = 1):
        scores.sort(key=lambda x: x['score'], reverse=True)

        total_score = scores[0]
        player_scores = scores[1:]  # excluye Total

        show_players = f'{total_score["player"]:>16}\n'
        show_index   = '  \n'  # Espacio para Total
        show_scores  = [self.format_value(total_score["score"])]

        start = self.scoreboards_len * (page - 1)
        end = min(start + self.scoreboards_len, len(player_scores))

        for i in range(start, end):
            show_index += f'{i + 1:>2}\n'
            show_players += f'{player_scores[i]["player"].capitalize():>16}\n'
            show_scores.append(self.format_value(player_scores[i]['score']))

        embed = discord.Embed(color=0x2f3136)\
            .set_footer(
                icon_url='https://cdn.discordapp.com/attachments/1246354182508642304/1338916354144731176/Triskcraft_logo.png?ex=6803d586&is=68028406&hm=599d5f6980470491a45a5b5d040758836f83bf6cb0dc80128a2fa9d263ee14ad&',
                text=f'TriskCraft digs [Top {self.scoreboards_len}]'
            )\
            .add_field(inline=True, name='‎ ', value=f'```\n{show_index}\n```')\
            .add_field(inline=True, name="**Player**", value=f'```\n{show_players}\n```')\
            .add_field(inline=True, name="**Score**", value='```yml\n' + "\n".join(show_scores) + '\n```')

        return embed


class ScoreboardView(discord.ui.View):
    def __init__(self, mdplugin: mdplugin, title: str, scores: list):
        super().__init__(timeout=300)
        self.mdplugin = mdplugin
        self.title = title
        self.scores = scores
        self.max_page = math.ceil((len(scores) - 1) / mdplugin.scoreboards_len)  # excluye Total
        self.page = 1

        self.add_item(PreviousPageButton())
        self.add_item(UpdateButton())
        self.add_item(NextPageButton())

    async def _update_page(self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=self.mdplugin.digs_embed(self.scores, self.page),
            view=self
        )

    async def _update_interface(self, interaction: discord.Interaction):
        if not interaction.response.is_done():
            await interaction.response.defer()

        self.scores = self.mdplugin.digs_scores()
        self.max_page = math.ceil((len(self.scores) - 1) / self.mdplugin.scoreboards_len)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=self.mdplugin.digs_embed(self.scores, self.page),
            view=self
        )


class UpdateButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='🔄', style=discord.ButtonStyle.gray, row=1)
        self.view: ScoreboardView

    async def callback(self, interaction: discord.Interaction):
        await self.view._update_interface(interaction)


class PreviousPageButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='<', style=discord.ButtonStyle.gray, row=1)
        self.view: ScoreboardView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = max(1, self.view.page - 1)
        await self.view._update_page(interaction)


class NextPageButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='>', style=discord.ButtonStyle.gray, row=1)
        self.view: ScoreboardView

    async def callback(self, interaction: discord.Interaction):
        self.view.page = min(self.view.max_page, self.view.page + 1)
        await self.view._update_page(interaction)
