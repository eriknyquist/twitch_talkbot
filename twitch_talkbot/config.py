import json


TWITCH_CLIENTID_KEY = "twitch_client_id"
TWITCH_CLIENTID_DEFAULT = ""

TWITCH_AUTH_TOKEN_KEY = "twitch_auth_token"
TWITCH_AUTH_TOKEN_DEFAULT = ""

TWITCH_BOT_ACCOUNT_KEY = "twitch_bot_account"
TWITCH_BOT_ACCOUNT_DEFAULT = ""

COMMANDS_KEY = "commands"
COMMANDS_DEFAULT = {}


def load_cfg_default(attrs, key, default):
    if key in attrs:
        return attrs[key]

    return default

class BotConfig(object):
    @classmethod
    def from_file(cls, filename):
        return BotConfig(filename)

    def __init__(self, filename=None):
        self.filename = filename

        if filename is None:
            # No filename passed- use default values
            self.twitch_client_id = TWITCH_CLIENTID_DEFAULT
            self.twitch_auth_token = TWITCH_AUTH_TOKEN_DEFAULT
            self.twitch_bot_account = TWITCH_BOT_ACCOUNT_DEFAULT
            self.commands = COMMANDS_DEFAULT
        else:
            # Load provided config file
            self.load_from_file(filename)

    def load_from_file(self, filename):
        with open(filename, 'r') as fh:
            attrs = json.load(fh)

        self.twitch_client_id = load_cfg_default(attrs, TWITCH_CLIENTID_KEY, TWITCH_CLIENTID_DEFAULT)
        self.twitch_auth_token = load_cfg_default(attrs, TWITCH_AUTH_TOKEN_KEY, TWITCH_AUTH_TOKEN_DEFAULT)
        self.twitch_bot_account = load_cfg_default(attrs, TWITCH_BOT_ACCOUNT_KEY, TWITCH_BOT_ACCOUNT_DEFAULT)
        self.commands = load_cfg_default(attrs, COMMANDS_KEY, COMMANDS_DEFAULT)

        return self

    def save_to_file(self, filename=None):
        if filename is None:
            filename = self.filename

        with open(filename, 'w') as fh:
            json.dump({
                TWITCH_CLIENTID_KEY: self.twitch_client_id,
                TWITCH_AUTH_TOKEN_KEY: self.twitch_auth_token,
                TWITCH_BOT_ACCOUNT_KEY: self.twitch_bot_account,
                COMMANDS_KEY: self.commands
            }, fh, indent=4)
