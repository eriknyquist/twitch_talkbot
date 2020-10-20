import time
import os
import threading
import queue

STOP_EVENT_POLL_SECS = 0.1
AUDIO_PLAYING_POLL_SECS = 0.1


class TextToSpeech(object):
    def __init__(self, text=None):
        self.text = text

    def voices(self):
        raise NotImplementedError()

    def set_voice(self, voice_id):
        raise NotImplementedError()

    def say(self, text=None):
        raise NotImplementedError()


class TextToSpeechQueue(object):
    def __init__(self, initial_items=[]):
        self.stop_event = threading.Event()
        self.queue = queue.Queue()
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

            tts.say()

    def stop(self):
        if self.wait_thread is None:
            return

        self.stop_event.set()
        self.wait_thread.join()
        self.wait_thread = None

    def put(self, text):
        self.queue.put(text)
