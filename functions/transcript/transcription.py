from faster_whisper import WhisperModel

model = None

def chooseModel(modelSize):
    
    global model
    
    model = WhisperModel(modelSize, device="cpu",compute_type="int8")
    
def transcribe(audio):
    segments, info = model.transcribe(audio, language="pt")
    
    text = "".join(segment.text for segment in segments)
    
    return {
        "text":text,
        "language":info.language,
        "language_probability":info.language_probability
    }