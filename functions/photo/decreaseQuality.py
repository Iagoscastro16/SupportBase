#1. importando a biblioteca pillow, que serve para podermos mexer com imagens
from PIL import Image
#2. importando a função que identifica o formato da imagem
from typeIdentify import typeIdentify
#3. importando a função que 
from pathlib import Path

def decreaseQuality (photo):
    
    if typeIdentify(photo) == "JPEG" or typeIdentify(photo) == "WEBP":
        caminhoImagem = Path(__file__).parent.parent.parent/"src"/"upload"
        photo.save(caminhoImagem / photo.filename, optimize=True, quality=70)
        
    
    elif typeIdentify(photo) == "PNG":
        caminhoImagem = Path(__file__).parent.parent.parent/"src"/"upload"
        photo.save(caminhoImagem / photo.filename, compress_level=7, optimize=True)
        
    return photo
