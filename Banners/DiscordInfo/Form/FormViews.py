from ..Modules import *
from .LogInteraction import *

class form_banner_views(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    @discord.ui.select(placeholder='Preguntas',
                       options=[discord.SelectOption(label='Personales', value=0),
                                discord.SelectOption(label='(Rol) Mano de Obra', value=1),
                                discord.SelectOption(label='(Rol) Redstoner', value=2),
                                discord.SelectOption(label='(Rol) Decorador', value=3)])
    async def role_form_selection(view, interaction: discord.Interaction, selection: discord.ui.Select):
        if interaction.user.id == view.owner_id:
            if int(selection.values[0]) == 0:
                if form_info_request(interaction.message.id, ['log_message_id']):
                    await interaction.response.send_message('✖ Ya respondiste estas preguntas.', ephemeral=True, delete_after=5)
                    return
                await interaction.response.send_modal(es_form_modal())
            elif int(selection.values[0]) == 1:
                if not form_info_request(interaction.message.id, ['log_message_id']):
                    await interaction.response.send_message('✖ Por favor, responde primero las preguntas personales.', ephemeral=True, delete_after=5)
                    return
                await interaction.response.send_modal(es_form_mano_de_obra_modal())
            elif int(selection.values[0]) == 2:
                if not form_info_request(interaction.message.id, ['log_message_id']):
                    await interaction.response.send_message('✖ Por favor, responde primero las preguntas personales.', ephemeral=True, delete_after=5)
                    return
                await interaction.response.send_modal(es_form_redstoner_modal())
            elif int(selection.values[0]) == 3:
                if not form_info_request(interaction.message.id, ['log_message_id']):
                    await interaction.response.send_message('✖ Por favor, responde primero las preguntas personales.', ephemeral=True, delete_after=5)
                    return
                await interaction.response.send_modal(es_form_decorador_modal())
        else:
            await interaction.response.send_message('✖ Solo puede interactuar con el formulario el creador del mismo.', ephemeral=True, delete_after=5)


class es_form_mano_de_obra_modal(discord.ui.Modal, title='Preguntas de Mano de Obra'):
    question_1 = discord.ui.TextInput(label='Experiencia en construcción/minería',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')
    question_2 = discord.ui.TextInput(label='Herramientas o técnicas que usas',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')
    question_3 = discord.ui.TextInput(label='¿Has trabajado en proyectos grandes?',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Describe tu experiencia.')
    question_4 = discord.ui.TextInput(label='Organización de recursos en proyectos',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')

    async def on_submit(modal, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        forms_channel = interaction.client.get_channel(config_form['Channel ID'])
        form = await forms_channel.fetch_message(form_info_request(interaction.message.id, ['log_message_id']))
        
        new_embed = form.embeds[0]\
            .add_field(inline=False, name='> Preguntas de Mano de Obra', value='')\
            .add_field(inline=False, name=modal.question_1.label, value=str(modal.question_1).strip()[:1024])\
            .add_field(inline=False, name=modal.question_2.label, value=str(modal.question_2).strip()[:1024])\
            .add_field(inline=False, name=modal.question_3.label, value=str(modal.question_3).strip()[:1024])\
            .add_field(inline=False, name=modal.question_4.label, value=str(modal.question_4).strip()[:1024])

        await form.edit(embeds=[new_embed])

        response = await interaction.followup.send('✔ Las respuestas fueron agregadas a tu formulario.\nNo olvides enviar tus evidencias adjuntando fotos en el ticket.')
        await response.delete(delay=60)


class es_form_redstoner_modal(discord.ui.Modal, title='Preguntas de Redstoner'):
    question_1 = discord.ui.TextInput(label='Experiencia previa en servidores',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')
    question_2 = discord.ui.TextInput(label='Tiempo jugando Minecraft',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')
    question_3 = discord.ui.TextInput(label='Conceptos de Redstone que conoces',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Menciona y explícalos.')
    question_4 = discord.ui.TextInput(label='Estructuras complejas que has creado',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Describe algunas.')

    async def on_submit(modal, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        forms_channel = interaction.client.get_channel(config_form['Channel ID'])
        form = await forms_channel.fetch_message(form_info_request(interaction.message.id, ['log_message_id']))
        
        new_embed = form.embeds[0]\
            .add_field(inline=False, name='> Preguntas de Redstoner', value='')\
            .add_field(inline=False, name=modal.question_1.label, value=str(modal.question_1).strip()[:1024])\
            .add_field(inline=False, name=modal.question_2.label, value=str(modal.question_2).strip()[:1024])\
            .add_field(inline=False, name=modal.question_3.label, value=str(modal.question_3).strip()[:1024])\
            .add_field(inline=False, name=modal.question_4.label, value=str(modal.question_4).strip()[:1024])

        await form.edit(embeds=[new_embed])

        response = await interaction.followup.send('✔ Las respuestas fueron agregadas a tu formulario.\nNo olvides enviar tus evidencias adjuntando fotos en el ticket.')
        await response.delete(delay=60)


class es_form_decorador_modal(discord.ui.Modal, title='Preguntas de Decorador'):
    question_1 = discord.ui.TextInput(label='Experiencia como Builder/Decorador',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')
    question_2 = discord.ui.TextInput(label='Herramientas que usas para construir',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Menciona y explícalas.')
    question_3 = discord.ui.TextInput(label='Proyecto más grande que has realizado',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Descríbelo.')
    question_4 = discord.ui.TextInput(label='¿Has estado en un Build Team?',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')

    async def on_submit(modal, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        forms_channel = interaction.client.get_channel(config_form['Channel ID'])
        form = await forms_channel.fetch_message(form_info_request(interaction.message.id, ['log_message_id']))
        
        new_embed = form.embeds[0]\
            .add_field(inline=False, name='> Preguntas de Decorador', value='')\
            .add_field(inline=False, name=modal.question_1.label, value=str(modal.question_1).strip()[:1024])\
            .add_field(inline=False, name=modal.question_2.label, value=str(modal.question_2).strip()[:1024])\
            .add_field(inline=False, name=modal.question_3.label, value=str(modal.question_3).strip()[:1024])\
            .add_field(inline=False, name=modal.question_4.label, value=str(modal.question_4).strip()[:1024])

        await form.edit(embeds=[new_embed])

        response = await interaction.followup.send('✔ Las respuestas fueron agregadas a tu formulario.\nNo olvides enviar tus evidencias adjuntando fotos en el ticket.')
        await response.delete(delay=60)


class es_form_modal(discord.ui.Modal, title='Formulario de ingreso'):
    question_1 = discord.ui.TextInput(label='Edad, país y nick de MC')
    question_2 = discord.ui.TextInput(label='¿Por qué deseas aplicar a TriskCraft?',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')
    question_3 = discord.ui.TextInput(label='¿Cuánto tiempo llevas jugando MC técnico?',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')
    question_4 = discord.ui.TextInput(label='¿Has estado en algún servidor técnico?',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')
    question_5 = discord.ui.TextInput(label='¿Qué crees que puedes aportar a TriskCraft?',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='Explícalo brevemente.')

    async def on_submit(modal, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        form_embed = discord.Embed(
                colour=0x2f3136,
                timestamp=datetime.now())\
            .set_footer(text='Sistema de Formularios \u200b', icon_url=interaction.client.user.display_avatar)\
            .add_field(inline=False, name=f'> Formulario {interaction.user.display_name}', value='')\
            .add_field(inline=False, name='Cuenta de discord', value=interaction.user.mention)\
            .add_field(inline=False, name=modal.question_1.label, value=str(modal.question_1).strip()[:1024])\
            .add_field(inline=False, name=modal.question_2.label, value=str(modal.question_2).strip()[:1024])\
            .add_field(inline=False, name=modal.question_3.label, value=str(modal.question_3).strip()[:1024])\
            .add_field(inline=False, name=modal.question_4.label, value=str(modal.question_4).strip()[:1024])\
            .add_field(inline=False, name=modal.question_5.label, value=str(modal.question_5).strip()[:1024])\
            .set_thumbnail(url=interaction.user.display_avatar)
        
        forms_channel = interaction.client.get_channel(config_form['Channel ID'])
        new_form = await forms_channel.send(embed=form_embed)
        try:
            await new_form.add_reaction(config_form['Emoji Yes'])
        except:
            await new_form.add_reaction('✅')
        
        try:
            await new_form.add_reaction(config_form['Emoji No'])
        except:
            await new_form.add_reaction('❌')
        
        form_info_update(interaction.message.id, {'log_message_id': new_form.id})
        
        response = await interaction.followup.send(f'✔ Las respuestas fueron agregadas a tu formulario.')
        await response.delete(delay=60)