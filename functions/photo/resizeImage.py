from PIL import Image
from pathlib import Path

from typeIdentify import typeIdentify


def resizeImage (photo):
    
    originalWidth, originalHeight = photo.size
    
    newHeight = (originalHeight / originalWidth) * 480
    
    photoResize = photo.resize((480, int(newHeight)))
    
    caminhoImagem = Path(__file__).parent.parent.parent/"src"/"upload"
    
    photoResize.save(caminhoImagem / photo.filename, typeIdentify(photo))