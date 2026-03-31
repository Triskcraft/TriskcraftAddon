from mcdis_rcon.utils import isAdmin
from discord.ext import commands
from mcdis_rcon.utils import read_dat_files

import discord

class DigsCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.app_commands.command(
            name            = 'digs',
            description     = 'Lista el scoreboard de digs'
    )
    async def send_command(self, interaction: discord.Interaction):
        if not isAdmin(interaction.user):
            await interaction.response.send_message(
                "Comando en construcción.", ephemeral=True, delete_after=1
            )
            return

        scores = self.digs_scores()
        # scoreboard size
        ss = len(str(len(scores)))
        # max player name lenght
        mpnl = 1
        # max score length
        msl = 1
        lines = []

        for x in range(0, len(scores)):
            name = scores[x]["player"]
            score = scores[x]["score"]

            if len(name) > mpnl:
                mpnl = len(name)

            if len(str(score)) > msl:
                msl = len(str(score))

        for i, entry in enumerate(scores):
            name = entry["player"]
            score = entry["score"]      
            line = f"{str(i).rjust(ss)} {name.rjust(mpnl)} {str(score).rjust(msl)}"
            if len("```" + "\n".join(lines + [line]) + "```") > 1024:
                break
            lines.append(line)

        embed = discord.Embed(color=0x2f3136)\
            .set_footer(
                icon_url='https://triskcraft.com/logo.webp',
                text=f'TriskCraft digs [Top {len(lines)-1}]'
            )\
            .add_field(name="**Players**", value="```\n" + "\n".join(lines) + "\n```")
            
        await interaction.response.send_message(embed=embed)

    def digs_scores(self):
        data = read_dat_files('/home/ubuntu/TriskCraftSMP/SMP/server/world/data/scoreboard.dat')

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

async def setup(client: commands.Bot):
    await client.add_cog(DigsCommand(client))
