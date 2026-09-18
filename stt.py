import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

audio_file = "audio/test.wav"

print("Mengirim audio ke Groq...")

with open(audio_file, "rb") as file:
    transcription = client.audio.transcriptions.create(
        file=file,
        model="whisper-large-v3",
        language="id",
        response_format="text"
    )

print("\n=== HASIL STT ===")
print(transcription)