from twitch_talkbot.tts.pyttsx3_tts import PYTTSX3TextToSpeech
from twitch_talkbot.text_to_speech import TextToSpeechQueue

COMMAND_PREFIX = "!"


class CommandProcessor(object):
    def __init__(self, tts_class=PYTTSX3TextToSpeech):
        self.queue = TextToSpeechQueue()
        self.tts_class = tts_class

    def process_input(self, text):
        text = text.strip()

        if text.startswith(COMMAND_PREFIX):
            # Pass to command processor
            return self.process_command(text)

        # Not a command, speak this text
        self.queue.put(self.tts_class(text))
        return None
