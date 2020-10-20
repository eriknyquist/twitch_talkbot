import io

import pyttsx3

from talkbot.text_to_speech import TextToSpeech, TextToSpeechQueue


engine = pyttsx3.init()
#engine.setProperty('voice', 'en-gb')


class PYTTSX3TextToSpeech(TextToSpeech):
    def __init__(self, *args, **kwargs):
        super(PYTTSX3TextToSpeech, self).__init__(*args, **kwargs)

    def say(self, text=None):
        if text is None:
            text = self.text

        if text is None:
            raise RuntimeError("No speech text provided")

        engine.say(text)
        engine.runAndWait()

    def voices(self):
        return [v.id for v in engine.getProperty("voices")]

    def set_voice(self, voice_id):
        raise NotImplementedError()
