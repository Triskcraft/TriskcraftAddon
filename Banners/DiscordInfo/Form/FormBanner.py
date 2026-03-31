from ..Modules import *

def form_banner_embed(client: commands.Bot):
    banner = discord.Embed(
            title = f'> ¡Bienvenido al Formulario!',
            colour = 0x2f3136,
            timestamp = datetime.now(),
            description = '¡Hola! Estás a punto de comenzar el proceso para postularte. Aquí te dejamos los pasos para que todo sea claro y sencillo:')\
        .add_field(name = '> Completa las preguntas', inline = False, value = 
            'Para comenzar, te pediremos que respondas a las preguntas del formulario. Las preguntas personales son obligatorias, mientras que para los roles, basta con seleccionar al menos uno.')\
        .add_field(name = '> Envía tu evidencia', inline = False, value = 
            'Una vez que hayas respondido, usa este canal para compartir pruebas de que puedes cumplir con los roles seleccionados. Lo más común es enviar imágenes de tu mundo, pero si tienes otro tipo de evidencia, también es válida.')\
        .add_field(name = '> Espera el proceso de votación', inline = False, value = 
            'Tu postulación será revisada y votada. Recibirás una respuesta en un plazo máximo de 48 horas. ¡Te deseamos mucha suerte!\n↳ Si tienes alguna duda, puedes dejarla en este canal.\n↳ Si deseas cancelar tu postulación, simplemente cierra el ticket.')\
        .set_footer(text = 'Sistema de Formularios \u200b', icon_url = client.user.display_avatar)\
        .set_thumbnail(url = config_form['Thumbnail'])
    return banner
