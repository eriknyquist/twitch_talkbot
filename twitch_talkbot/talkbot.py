import asyncio
import threading
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

        self.event_loop = asyncio.get_event_loop()
        self.event_thread = threading.Thread(target=self.event_loop.run_forever)
        self.event_thread.daemon = True

    def run(self):
        self.event_thread.start()
        asyncio.run_coroutine_threadsafe(self.bot.start(), self.event_loop)

        while True:
            f = asyncio.run_coroutine_threadsafe(self.session.prompt_async("> "), self.event_loop)
            text = f.result()
            text = text.strip()

            if text:
                resp = self.processor.process_input(text)
                if resp:
                    print(resp)
