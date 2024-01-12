from googletrans import Translator

translator = Translator()

def language(Input):
    return translator.detect(Input).lang
    
def translate(Input, TransToLang = "en"):
    return translator.translate(Input, dest = TransToLang).text

