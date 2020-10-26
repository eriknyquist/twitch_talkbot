import multiprocessing
from twitchio.ext import commands

from twitch_talkbot.command_processor import CommandProcessor

from prompt_toolkit.completion import PathCompleter
from prompt_toolkit import prompt as prompt_toolkit_prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

class TwitchBot(commands.Bot):
    def __init__(self, config, *args, **kwargs):
        super(TwitchBot, self).__init__(*args, **kwargs)
        self.config = config

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print('Ready')

    async def event_message(self, message):
        if message.author.name.lower() != self.config.twitch_bot_account.lower():
            # We only care about mesages from ourself
            return

        await message.channel.send(message.content)

class Talkbot(object):
    def __init__(self, config):
        self.config = config

        self.bot = TwitchBot(config,
                irc_token=config.twitch_auth_token,
                client_id=config.twitch_client_id,
                nick=config.twitch_bot_account,
                prefix='%',
                initial_channels=['#%s' % config.twitch_bot_account]
        )

        self.processor = CommandProcessor()
        self.session = PromptSession(history=InMemoryHistory(),
                                     enable_history_search=True)

        self.bot_thread = multiprocessing.Process(target=self.bot.run)
        self.bot_thread.daemon = True

    def run(self):
        #self.bot_thread.start()
        self.bot.run()

        while True:
            text = self.session.prompt("> ")
            text = text.strip()

            if text:
                resp = self.processor.process_input(text)
                if resp:
                    print(resp)
