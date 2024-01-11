import asyncio
import websockets
import pyaudio

CHUNK = 1024

async def send_audio():
    async with websockets.connect("ws://localhost:8765") as websocket:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=CHUNK)

        try:
            while True:
                data = stream.read(CHUNK)
                await websocket.send(data)
        except websockets.ConnectionClosed:
            print("Connection closed.")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

asyncio.run(send_audio())
