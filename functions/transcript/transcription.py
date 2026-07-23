# Importação do fast_whisper, escolhi ele por ser mais leve que o modelo original.
from faster_whisper import WhisperModel

# Model como variavel global, para que não precise ser sempre recarregado quando a pessoa roda, ela carrega uma vez na memoria e fica lá, só esperando o transcribe chamar.

model = None

def chooseModel(modelSize):
    
    global model
    
    model = WhisperModel(modelSize, device="cpu",compute_type="int8")

# Função que faz a transcrição(tem a probabilidade da lingua, para quando tiver alguma interferencia ou parecido, ideal para detectar ruidos e etc.

def transcribe(audio):
    segments, info = model.transcribe(audio, language="pt")
    
    text = "".join(segment.text for segment in segments)
    
    return {
        "text":text,
        "language":info.language,
        "language_probability":info.language_probability
    }