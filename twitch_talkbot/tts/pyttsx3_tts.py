import io

import pyttsx3

from twitch_talkbot.text_to_speech import TextToSpeech, TextToSpeechQueue


# Gotta do this stupid wrapper class to work around pyttsx3 win10 bug
class TTSWrapper:
    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

class PYTTSX3TextToSpeech(TextToSpeech):
    def __init__(self, *args, **kwargs):
        super(PYTTSX3TextToSpeech, self).__init__(*args, **kwargs)

    def say(self, text=None):
        if text is None:
            text = self.text

        if text is None:
            raise RuntimeError("No speech text provided")

        t = TTSWrapper()
        t.say(text)
        del(t)
        
    def voices(self):
        return [v.id for v in engine.getProperty("voices")]

    def set_voice(self, voice_id):
        raise NotImplementedError()
