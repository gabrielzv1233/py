import asyncio
from aiohttp import web
import pyaudio
import io
import wave

CHUNK = 110250
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 110250

audio = pyaudio.PyAudio()

default_input_device_index = audio.get_default_input_device_info()['index']
default_input_device_name = audio.get_device_info_by_index(default_input_device_index)['name']
print(f"Using default input device: {default_input_device_name}")

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=default_input_device_index,
                    frames_per_buffer=CHUNK)

def pcm_to_wav(pcm_data, sample_rate=RATE, channels=CHANNELS, bit_depth=16):
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(bit_depth // 8)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_data)
    return wav_io.getvalue()

async def handle(request):
    return """<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Audio Streaming</title>
</head>
<body>
    <h1>WebSocket Audio Streaming</h1>
    <button id="start">Start Audio</button>
    <script>
        let ws;
        let audioContext;
        let bufferQueue = [];
        let isPlaying = false;
        let lastPacketTime = Date.now();

        document.getElementById('start').addEventListener('click', async () => {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            } else if (audioContext.state === 'suspended') {
                await audioContext.resume();
            }

            if (!ws || ws.readyState !== WebSocket.OPEN) {
                ws = new WebSocket('ws://localhost:5000/ws');
                ws.binaryType = 'arraybuffer';

                ws.onopen = () => {
                    console.log('WebSocket connection opened');
                };

                ws.onmessage = async (event) => {
                    const currentTime = Date.now();
                    const timeDiff = currentTime - lastPacketTime;
                    console.log(`Received audio packet. Size: ${event.data.byteLength} bytes. Time since last packet: ${timeDiff} ms`);
                    lastPacketTime = currentTime;

                    // Convert ArrayBuffer to Uint8Array
                    const audioData = new Uint8Array(event.data);

                    // Push the data into the buffer queue
                    bufferQueue.push(audioData.buffer);

                    // Process the buffer queue
                    if (!isPlaying && bufferQueue.length > 0) {
                        isPlaying = true;
                        processBuffer();
                    }
                };

                ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };

                ws.onclose = (event) => {
                    console.log('WebSocket connection closed', event);
                    if (isPlaying) {
                        isPlaying = false;
                    }
                };
            }
        });

        async function processBuffer() {
            if (bufferQueue.length === 0) {
                isPlaying = false;
                return;
            }

            const audioData = bufferQueue.shift();
            try {
                const audioBuffer = await audioContext.decodeAudioData(audioData);
                const source = audioContext.createBufferSource();
                source.buffer = audioBuffer;
                source.connect(audioContext.destination);
                source.start();

                source.onended = () => {
                    if (bufferQueue.length > 0) {
                        setTimeout(processBuffer, 0);
                    } else {
                        isPlaying = false;
                    }
                };
            } catch (error) {
                console.error('Audio decoding error:', error);
                setTimeout(processBuffer, 0);
            }
        }
    </script>
</body>
</html>
"""

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    try:
        while True:
            audio_data = stream.read(CHUNK, exception_on_overflow=False)
            wav_data = pcm_to_wav(audio_data)
            await ws.send_bytes(wav_data)
    except Exception as e:
        print(f'WebSocket connection closed with exception {e}')
    finally:
        print('WebSocket connection closed')
        stream.stop_stream()
        stream.close()
        audio.terminate()

    return ws

async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/ws', websocket_handler)
    return app

async def main():
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    print("Server started at http://0.0.0.0:5000")
    await site.start()
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
