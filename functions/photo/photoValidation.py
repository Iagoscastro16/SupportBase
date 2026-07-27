from PIL import Image, UnidentifiedImageError

def type_identify (photo):
    return photo.format

def corruption_data(photo):
    try:
        with Image.open(photo) as img:
            img.verify()

        with Image.open(photo) as img:
            img.load()

        return {"success": True,
                "message": "A imagem não está corrompida"}
# Imagem perfeita, sem corrupção
    except(UnidentifiedImageError,OSError,SyntaxError):
        # Imagem corrompida ou inválida
        return {"success": False,
                "errorMessage": "A imagem possui corrupção"} 


def formats(image_format):

    accepted_format = {"JPEG", "PNG", "WEBP"}

    if image_format in accepted_format:
        return {"success": True,
                "message": "Fomato aceito"}
    else:
        return {"success": False,
                        "errorMessage": "Não é permitido o envio de outros tipos de arquivos, que não sejam fotos"}