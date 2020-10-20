from talkbot.tts.pyttsx3_tts import PYTTSX3TextToSpeech
from talkbot.text_to_speech import TextToSpeechQueue

from prompt_toolkit.completion import PathCompleter
from prompt_toolkit import prompt as prompt_toolkit_prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory


class CommandProcessor(object):
    def __init__(self):
        self.queue = TextToSpeechQueue()
        self.session = PromptSession(history=InMemoryHistory(),
                                     enable_history_search=True)

    def run(self):
        while True:
            resp = self.session.prompt("> ")
            self.queue.put(PYTTSX3TextToSpeech(resp))


if __name__ == "__main__":
    p = CommandProcessor()
    p.run()
