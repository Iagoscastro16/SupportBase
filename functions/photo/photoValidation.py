from PIL import Image

def typeIdentify (photo):
    return photo.format

def blockedFormats(image_format):

    prohibitedFormats = {"mp4","mov","avi"}

    if image_format in prohibitedFormats:
        return {"success": False,
                "errorMessage": "Não é permitido o envio de outros tipos de arquivos, que não sejam fotos"}
    else:
        return {"success": True,
                "message": "Fomato aceito"}