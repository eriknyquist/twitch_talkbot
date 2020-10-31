Twitch Talkbot
==============

A twitch bot for streamers who can't / don't want to speak. Uses the standard TTS
engine for your OS to convert text you type into audible speech. Talkbot will
see everything you type in the twitch chat, and will speak it. Additionally,
you may type text into the prompt you get when you run Talkbot locally on your PC,
and this text will be spoken too, and also simultaneously sent to the twitch chat
as if you typed it in there.

Setup instructions
==================

First-time setup
----------------

You only need to do this stuff once.

#. Install `Python 3.7 <https://www.python.org/downloads/release/python-379/>`_

#. Open a Command Prompt or a terminal and type the following command to install
   twitch_talkbot:

   ::

       python -m pip install twitch_talkbot

#. Once the installation command completes, type the following command to
   run Talkbot:

   ::

       python -m twitch_talkbot

#. Since you do not have a configuration file yet, running the above command
   should result in the following output:

   ::

       Unable to find config file. Created default in 'xxxx.json', please
       enter appropriate values and re-run.

   Open the default configuraton file that was created for you at ``xxxx.json``,
   and ensure the following parameters are set:

   #. ``"twitch_auth_token"``: ensure this is set to the OAuth token for the
      twitch account you want the bot to use
      (e.g. ``"twitch_auth_token": "oauth:blahblahblahblahblah"``).
      `Generate an OAuth token here <https://twitchapps.com/tmi/>`_ (you will need
      to log in to the twitch account you plan to use).

   #. ``"twitch_bot_account"``: Ensure this is set to the name of the twitch account
      you want to the bot to log in with (e.g. ``"twitch_bot_account": "endremia"``).

   #. ``"twitch_client_id"``: Ensure this is set to the client ID for your
      registered application (e.g. ``"twitch_client_id": "blahblahblahblah"``).
      `Register a new application here <https://dev.twitch.tv/console/apps/create>`_
      (Set "OAuth redirect URLs" to ``http://localhost``).

That's it, you're done, and hopefully you never have to do those things again.


Running the bot
---------------

Every time you want to start twitch_talkbot, open a Command Prompt or terminal and
type the following command:

::

    python -m twitch_talkbot

Now, the bot is running and you can type commands or text to speak into the
command prompt window, or into the twitch chat window.
