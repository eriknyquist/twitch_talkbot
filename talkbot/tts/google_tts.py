import io

from talkbot.text_to_speech import TextToSpeech, TextToSpeechQueue

from gtts import gTTS


class GoogleTextToSpeech(TextToSpeech):
    def __init__(self, *args, **kwargs):
        super(GoogleTextToSpeech, self).__init__(*args, **kwargs)

    def text_to_audio_fp(self, text):
        tts = gTTS(text=text, lang='it')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        tts.save("test.mp3")
        fp.seek(0)
        return fp


if __name__ == "__main__":
    q = TextToSpeechQueue()

    try:
        while True:
            text = input("> ").strip()
            if text:
                q.put(GoogleTextToSpeech(text))
    except KeyboardInterrupt:
        q.stop()
