import time
import os
import threading
import queue

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

pygame.mixer.pre_init(frequency=24000, size=-16, channels=2, buffer=4096)
pygame.mixer.init()


STOP_EVENT_POLL_SECS = 0.1
AUDIO_PLAYING_POLL_SECS = 0.1


class TextToSpeech(object):
    def __init__(self, text=None):
        self.audio_playing = threading.Event()
        self.thread = None
        self.text = text
        self.fp = None

    def play_audio_and_wait(self):
        pygame.mixer.music.stop()
        time.sleep(0.2)

        pygame.mixer.music.load(self.fp)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.2)

        self.fp.close()
        self.fp = None

        self.audio_playing.clear()

    def text_to_audio_fp(self, text):
        raise NotImplementedError()

    def prepare_audio(self, text=None):
        if text is None:
            text = self.text

        if text is None:
            raise ValueError("No text provided for speech synthesis")

        self.fp = self.text_to_audio_fp(text)
        return self

    def speak_prepared_audio(self):
        if self.fp is None:
            raise RuntimeError("No prepared audio to play")

        self.audio_playing.set()
        self.thread = threading.Thread(target=self.play_audio_and_wait)
        self.thread.daemon = True
        self.thread.start()

    def say(self, text=None):
        self.prepare_audio(text)
        self.speak_prepared_audio()

    def saying(self):
        return self.audio_playing.is_set()


class TextToSpeechQueue(object):
    def __init__(self, initial_items=[]):
        self.stop_event = threading.Event()
        self.queue = queue.Queue()
        self.prepare_thread = None
        self.wait_thread = threading.Thread(target=self._play_audio_queue)
        self.wait_thread.daemon = True
        self.wait_thread.start()

        for i in initial_items:
            self.queue.put(i)

    def _play_audio_queue(self):
        while True:
            time.sleep(STOP_EVENT_POLL_SECS)

            if self.stop_event.is_set():
                self.stop_event.clear()
                return

            try:
                tts = self.queue.get(block=False)
            except queue.Empty:
                continue

            tts.speak_prepared_audio()
            while tts.saying():
                time.sleep(AUDIO_PLAYING_POLL_SECS)

    def stop(self):
        if self.wait_thread is None:
            return

        self.stop_event.set()
        self.wait_thread.join()
        self.wait_thread = None

    def put(self, tts):
        self.prepare_thread = threading.Thread(target=self._prepare_audio, args=(tts,))
        self.prepare_thread.daemon = True
        self.prepare_thread.start()

    def _prepare_audio(self, tts):
        tts.prepare_audio()
        self.queue.put(tts)
