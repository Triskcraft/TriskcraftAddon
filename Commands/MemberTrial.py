import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime
import os
import yaml

class CerrarCanalButton(discord.ui.View):
    def __init__(self, canal: discord.TextChannel):
        super().__init__(timeout=None)
        self.canal = canal

    @discord.ui.button(label="Cerrar canal", style=discord.ButtonStyle.danger, emoji="🔒")
    async def cerrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Canal cerrado manualmente.", ephemeral=True)
        if self.canal.permissions_for(self.canal.guild.me).manage_channels:
            try:
                await self.canal.delete()
            except discord.NotFound:
                pass
        else:
            await interaction.followup.send("No tengo permisos para cerrar el canal.", ephemeral=True)

class TestMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.staff_role_id = 1355617895480164472
        self.member_test_role_id = 1202775706912948264
        self.mano_de_obra_role_id = 1302501042444963912
        self.member_role_id = 1202775128006459453
        self.encuesta_channel_id = 1219447416604856392
        self.categoria_channel_id = 1255012913505112084
        self.encuestas = {}
        self.config_path = os.path.join(os.path.dirname(__file__), "..", "Config", "evaluaciones.yml")
        self.load_encuestas()

        for data in self.encuestas.values():
            bot.loop.create_task(self.reanudar_evaluacion(data))

    def load_encuestas(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                data = yaml.safe_load(f) or {}
                self.encuestas = data

    def save_encuestas(self):
        with open(self.config_path, "w") as f:
            yaml.safe_dump(self.encuestas, f)

    @app_commands.command(name="test", description="Inicia el período de prueba para un miembro.")
    @app_commands.describe(member="El miembro que comenzará el período de prueba.")
    async def test(self, interaction: discord.Interaction, member: discord.Member):
        if self.staff_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
            return

        member_test_role = interaction.guild.get_role(self.member_test_role_id)
        mano_de_obra_role = interaction.guild.get_role(self.mano_de_obra_role_id)
        if not member_test_role or not mano_de_obra_role:
            await interaction.response.send_message("Faltan roles requeridos.", ephemeral=True)
            return

        await member.add_roles(member_test_role, mano_de_obra_role)
        await interaction.response.send_message(
            f"{member.mention} ha iniciado su período de prueba y se le ha asignado el rol de Mano de Obra.",
            ephemeral=True
        )

        await asyncio.sleep(60 * 60 * 24 * 14)  # Simula 2 semanas

        encuesta_channel = self.bot.get_channel(self.encuesta_channel_id)
        if not encuesta_channel:
            return

        embed = discord.Embed(
            title="Evaluación de miembro de prueba",
            description=f"¿{member.mention} califica para ser miembro permanente?",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        mensaje = await encuesta_channel.send(content="@everyone", embed=embed)
        await mensaje.add_reaction("✅")
        await mensaje.add_reaction("❌")

        self.encuestas[str(mensaje.id)] = {
            "member_id": member.id,
            "mensaje_id": mensaje.id,
            "inicio": datetime.utcnow().isoformat()
        }
        self.save_encuestas()

        await self.reanudar_evaluacion(self.encuestas[str(mensaje.id)])

    async def reanudar_evaluacion(self, data):
        await asyncio.sleep(60 * 60 * 5)  # Simula 5 horas desde votación

        encuesta_channel = self.bot.get_channel(self.encuesta_channel_id)
        if not encuesta_channel:
            return

        mensaje_id = int(data["mensaje_id"])
        member_id = int(data["member_id"])
        mensaje = await encuesta_channel.fetch_message(mensaje_id)
        reacciones = {reaction.emoji: reaction.count for reaction in mensaje.reactions}

        guild = encuesta_channel.guild
        member = guild.get_member(member_id)

        categoria = guild.get_channel(self.categoria_channel_id)
        if not isinstance(categoria, discord.CategoryChannel):
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True),
            guild.get_role(self.staff_role_id): discord.PermissionOverwrite(read_messages=True)
        }

        canal_privado = await guild.create_text_channel(
            name=f"evaluacion-{member.name}",
            overwrites=overwrites,
            category=categoria
        )

        member_test_role = guild.get_role(self.member_test_role_id)
        member_role = guild.get_role(self.member_role_id)

        if reacciones.get("✅", 0) > reacciones.get("❌", 0):
            await member.remove_roles(member_test_role)
            if member_role:
                await member.add_roles(member_role)

            embed = discord.Embed(
                title="Resultado del Período de Prueba",
                description=f"🎉 Felicidades {member.mention}, has sido promovido a miembro permanente.",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="Resultado del Período de Prueba",
                description=f"{member.mention}, lamentablemente no calificaste como miembro permanente.",
                color=discord.Color.red()
            )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Triskcraft | Evaluaciones de Miembros")

        await canal_privado.send(
            content=f"{member.mention} <@&{self.staff_role_id}>",
            embed=embed,
            view=CerrarCanalButton(canal_privado)
        )

        await asyncio.sleep(60 * 60 * 24)  # Simula 24h
        if canal_privado and canal_privado.permissions_for(guild.me).manage_channels:
            try:
                await canal_privado.delete()
            except discord.NotFound:
                pass

        self.encuestas.pop(str(mensaje_id), None)
        self.save_encuestas()

async def setup(bot):
    await bot.add_cog(TestMember(bot))
