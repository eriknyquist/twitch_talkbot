from twitch_talkbot.command_processor import CommandProcessor

from prompt_toolkit.completion import PathCompleter
from prompt_toolkit import prompt as prompt_toolkit_prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory


class Talkbot(object):
    def __init__(self, config, twitch_clientid, twitch_auth_token, bot_nick):
        self.config = config
        self.twitch_clientid = twitch_clientid
        self.twitch_auth_token = twitch_auth_token
        self.bot_nick = bot_nick

        self.processor = CommandProcessor()
        self.session = PromptSession(history=InMemoryHistory(),
                                     enable_history_search=True)

    def run(self):
        while True:
            text = self.session.prompt("> ")
            text = text.strip()

            if text:
                resp = self.processor.process_input(text)
                if resp:
                    print(resp)
