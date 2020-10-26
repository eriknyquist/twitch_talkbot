import asyncio

from twitch_talkbot.tts.pyttsx3_tts import PYTTSX3TextToSpeech
from twitch_talkbot.text_to_speech import TextToSpeechQueue

COMMAND_PREFIX = "!"

CMD_HELP_HELP = """{0} [command]

Shows helpful information about the given command. Replace [command] with the
command you want help with."""

CMD_CMD_HELP = """{0} [command_name] [arg1] [arg2] ...

Allows you to add a new command (triggered by '!command_name') that sends a
particular message to TTS and also to the twitch chat. After the [command_name],
there may be optionally one or more strings representing the names of positional
arguments for the command, which must be provided to the command in the same
order given here.

You will be prompted for the content of the message to be triggered by the command,
within which you can reference the positional arguments by putting their names in
between curly braces, e.g. {{arg1}}."""


class Command(object):
    def __init__(self, word, handler, helptext):
        self.word = word
        self.handler = handler
        self.helptext = helptext

    def help(self):
        return self.helptext.format(COMMAND_PREFIX + self.word)


class CommandProcessor(object):
    def __init__(self, config, bot, command_list, tts_class=PYTTSX3TextToSpeech):
        self.queue = TextToSpeechQueue()
        self.tts_class = tts_class
        self.config = config
        self.bot = bot
        self.cmds = {x.word: x for x in command_list}

    def help(self):
        return "Available commands:\n%s" % "\n".join(self.cmds.keys())

    def handle_custom_command(self, cmd, args):
        fields = self.config.commands[cmd]
        resp = fields[0]
        argnames = fields[1:]
        expected_args = len(argnames)

        if len(args) < expected_args:
            if expected_args > 1:
                argstring = "%d arguments" % expected_args
            else:
                argstring = "%d argument" % expected_args

            if len(args) == 0:
                provstring = "none were provided"
            elif len(args) == 1:
                provstring = "only 1 was provided"
            else:
                provstring = "only %d were provided" % len(args)

            return ("Command '%s' requires %s, but %s" % (cmd, argstring, provstring))

        kwargs = {argnames[i]: args[i] for i in range(len(argnames))}
        message = resp.format(**kwargs)

        # SPeak the message
        self.queue.put(self.tts_class(message))

        # and send it to twitch chat
        self.bot.send_message(message)

    def process_command(self, text):
        text = text.strip()
        words = text.lstrip(COMMAND_PREFIX).split()
        command = words[0].lower()

        if command in self.cmds:
            return self.cmds[command].handler(self, self.config, self.bot, words[1:])
        elif command in self.config.commands:
            return self.handle_custom_command(command, words[1:])

        return "Sorry, I don't recognize the command '%s'" % command

    def process_commandline_input(self, text):
        text = text.strip()

        if text.startswith(COMMAND_PREFIX):
            # Pass to command processor
            resp = self.process_command(text)
            if resp:
                print("\n" + resp + "\n")

            return

        # Not a command, speak this text
        self.queue.put(self.tts_class(text))

        # .. and, send to twitch chat
        self.bot.send_message(text)

        return None

    def process_twitch_chat_input(self, text):
        text = text.strip()

        if text.startswith(COMMAND_PREFIX):
            # Pass to command processor
            resp = self.process_command(text)
            if resp:
                print("\n" + resp + "\n")

            return

        # Not a command, speak this text
        self.queue.put(self.tts_class(text))


def cmd_cmd(proc, config, bot, args):
    if len(args) == 0:
        return "Please provide at least a command name"

    name = args[0]
    cmdargs = args[1:]

    if (name in proc.cmds) or (name in config.commands):
        return "Sorry, but there is already a command called '%s'!" % name

    if cmdargs:
        argstring = "arguments: %s" % ", ".join(cmdargs)
    else:
        argstring = "no arguments"

    print(">> Adding new command '%s' with %s" % (name, argstring))

    while True:
        f = asyncio.run_coroutine_threadsafe(
                proc.bot.session.prompt_async(">> Please enter message for '%s': " % name),
                proc.bot.event_loop
        )

        # Get message text
        resp = f.result().strip()

        # Build format token fict to verify format tokens
        kwargs = {x: None for x in cmdargs}
        try:
            _ = resp.format(**kwargs)
        except KeyError:
            print(">> Invalid format token provided! try again...")
            continue

        config.commands[name] = [resp] + cmdargs
        break

    config.save_to_file()
    return "New command '%s' added successfully!" % name

def cmd_help(proc, config, bot, args):
    if len(args) == 0:
        return proc.help()

    cmd = args[0].strip()
    if cmd.startswith(COMMAND_PREFIX):
        cmd = cmd.lstrip(COMMAND_PREFIX)

    if cmd not in proc.cmds:
        return "No command '%s' to get help for" % cmd

    return proc.cmds[cmd].help()


twitch_talkbot_command_list = [
    Command("help", cmd_help, CMD_HELP_HELP),
    Command("cmd", cmd_cmd, CMD_CMD_HELP)
]
