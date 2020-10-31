import io

import pyttsx3

from twitch_talkbot.text_to_speech import TextToSpeech, TextToSpeechQueue


# Gotta do this stupid wrapper class to work around pyttsx3 win10 bug
class TTSWrapper:
    engine = None
    rate = None
    def __init__(self, voice_id=None):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)

        if voice_id is not None:
            self.engine.setProperty("voice", voice_id)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

class PYTTSX3TextToSpeech(TextToSpeech):
    voice_id = None

    def __init__(self, *args, **kwargs):
        super(PYTTSX3TextToSpeech, self).__init__(*args, **kwargs)

    def say(self, text=None):
        if text is None:
            text = self.text

        if text is None:
            raise RuntimeError("No speech text provided")

        t = TTSWrapper(PYTTSX3TextToSpeech.voice_id)
        t.say(text)
        del(t)
        
    def voices(self):
        return [v.id for v in pyttsx3.init().getProperty("voices")]

    def set_voice(self, voice_id):
        PYTTSX3TextToSpeech.voice_id = voice_id
