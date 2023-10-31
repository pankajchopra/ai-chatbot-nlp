import json
import sounddevice as sd

from vosk import Model, KaldiRecognizer
import sys
import queue

class SpeechToText:

    def __init__(self):
        self.q = queue.Queue()
        self.device_info = sd.query_devices(sd.default.device[0], 'input')
        self.samplerate = int(self.device_info['default_samplerate'])
        self.model = Model('model')
        self.recognizer = KaldiRecognizer(self.model, self.samplerate)
        self.recognizer.SetWords(False)

    def record_call_back(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def speech_to_text_run(self):
        with sd.RawInputStream(dtype='int16',
                           channels=1,

                           callback=self.recordCallback):
            while True:
                data = self.q.get()        
                if self.recognizer.AcceptWaveform(data):
                    recognizerResult = self.recognizer.Result()
                    # convert the recognizerResult string into a dictionary  
                    resultDict = json.loads(recognizerResult)
                    if not resultDict.get("text", "") == "":
                        return recognizerResult
                    else:
                        return '{\n  "text" : "Sorry, I could not understand what you were saying"\n}'
