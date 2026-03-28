import whisper
model = None
def chooseModel(modelSize):
    global model
    
    model = whisper.load_model(modelSize)
    
    
    
def transcribe(audio):
    return model.transcribe(audio,language = "pt")