import asyncio
import edge_tts

TEXT = "Halo Raihan. Ini adalah pengujian suara dari voice assistant."

async def main():
    communicate = edge_tts.Communicate(
        TEXT,
        "id-ID-ArdiNeural"
    )

    await communicate.save("audio/response.mp3")

    print("TTS selesai.")
    print("File tersimpan di: audio/response.mp3")

asyncio.run(main())