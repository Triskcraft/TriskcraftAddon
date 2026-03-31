import subprocess
from discord.ext import commands
import discord

def translate_with_shell(text: str, target_lang: str = "es") -> str:
    result = subprocess.run(
        ["trans", "-brief", f":{target_lang}", text],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() if result.stdout else "✖ No se pudo traducir."

class translate_to_spanish(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        @client.tree.context_menu(name='Translate to Spanish')
        async def translate_to_spanish(interaction: discord.Interaction, message: discord.Message):
            await interaction.response.defer(ephemeral=True)

            if message.content.strip():
                translation = translate_with_shell(message.content)
                emb_translation = discord.Embed(
                    colour=discord.Colour(0x2f3136),
                    description=f'{message.author.mention}: {translation}'
                )
                await interaction.followup.send(embed=emb_translation)
            else:
                await interaction.followup.send('✖ No hay nada para traducir.')

async def setup(client: commands.Bot):
    await client.add_cog(translate_to_spanish(client))
