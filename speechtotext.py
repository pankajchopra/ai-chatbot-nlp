import json
import sounddevice as sd

from vosk import Model, KaldiRecognizer
import sys
import queue

onetime_token = "eyJhbGciOiJFUzI1NiIsImtpZCI6ImtleTEiLCJ0eXAiOiJKV1QifQ.eyJyZWdpb24iOiJlYXN0dXMiLCJzdWJzY3JpcHRpb24taWQiOiJiNDUyMzY0NWZlOGE0OTE5ODE4NTRjNjI1OTI2M2NlNCIsInByb2R1Y3QtaWQiOiJTcGVlY2hTZXJ2aWNlcy5TMCIsImNvZ25pdGl2ZS1zZXJ2aWNlcy1lbmRwb2ludCI6Imh0dHBzOi8vYXBpLmNvZ25pdGl2ZS5taWNyb3NvZnQuY29tL2ludGVybmFsL3YxLjAvIiwiYXp1cmUtcmVzb3VyY2UtaWQiOiIvc3Vic2NyaXB0aW9ucy8xNGRjMWNmMi1iYzcxLTRmYjMtODdkNS0yMDhhNjczMWY2Y2MvcmVzb3VyY2VHcm91cHMvb3BlbmFpL3Byb3ZpZGVycy9NaWNyb3NvZnQuQ29nbml0aXZlU2VydmljZXMvYWNjb3VudHMvY3ljbG90cm9uc3BlZWNoIiwic2NvcGUiOiJzcGVlY2hzZXJ2aWNlcyIsImF1ZCI6InVybjptcy5zcGVlY2hzZXJ2aWNlcy5lYXN0dXMiLCJleHAiOjE3MDUwMzA3MzMsImlzcyI6InVybjptcy5jb2duaXRpdmVzZXJ2aWNlcyJ9.xpFQsJygsYvGlQqzB8NwAUjTjL_-yjB7jD4n2bmV_KwbbewepNbeasICCYT6I3RCvDwrii2hblGy-yjZB3xMVQ"
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
