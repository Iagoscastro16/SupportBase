#1. importando a biblioteca pillow, que serve para podermos mexer com imagens
from PIL import Image
#2. importando a função que identifica o formato da imagem
from photoValidation import typeIdentify
#3. importando a função que cuida dos caminhos dos arquivos, é a nova forma padrão de armazenar caminhos no python
from pathlib import Path

# O pillow trabalha de formas parecidas, porém com nomes diferentes para o tratamento de cada tipo de arquivo

def decreaseQuality (photo):

# No caso do Jpeg e webp, eles são arquivos que são caracterizados como "lossy", ou seja, arquivo que perdem qualidade , utilizando o "quality"(pillow permite escolher de 1 até 95), já o optimize é para o pillow reorganizar a imagem de uma forma que diminua o tamanho sem mexer na resolução

    caminhoImagem = Path(__file__).parent.parent.parent/"src"/"upload"
    tipo = typeIdentify(photo)

    if tipo == "JPEG" or tipo == "WEBP":
        photo.save(caminhoImagem / photo.filename, optimize=True, quality=70)

# png é caracterizado como "lossless", ou seja, um tipo de arquivo que não perde qualidade, então aqui a forma de diminuir seu peso é "comprimindo" a imagem

    elif tipo == "PNG":
        photo.save(caminhoImagem / photo.filename, compress_level=7, optimize=True)
        
    return photo
