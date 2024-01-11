import asyncio
import websockets
import azure.cognitiveservices.speech as speechsdk

# Azure Speech to Text configuration
speech_config = speechsdk.SpeechConfig(subscription="your_subscription_key", region="your_region")
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=False)  # Use WebSocket for audio input

# Speech recognizer for WebSocket stream
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

async def recognize_audio(websocket):
    async for message in websocket:
        audio_data = speechsdk.audio.AudioDataStream(buffer=message)
        result = speech_recognizer.recognize_once_async().get()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            await websocket.send(result.text)
        elif result.reason == speechsdk.ResultReason.NoMatch:
            await websocket.send("No speech detected.")
        else:
            await websocket.send("Error: " + result.reason)

start_server = websockets.serve(recognize_audio, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
