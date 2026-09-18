import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# Riwayat percakapan
messages = [
    {
        "role": "system",
        "content": (
            "Kamu adalah Groq Assistant, asisten AI yang ramah, "
            "jelas, dan membantu. Jawablah dalam bahasa Indonesia "
            "kecuali pengguna meminta bahasa lain."
        )
    }
]

print("=== GROQ ASSISTANT ===")
print("Ketik 'keluar' untuk berhenti.\n")

while True:
    pertanyaan = input("Kamu: ")

    if pertanyaan.lower() == "keluar":
        print("Program selesai.")
        break

    # Masukkan pertanyaan pengguna ke riwayat
    messages.append({
        "role": "user",
        "content": pertanyaan
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    jawaban = response.choices[0].message.content

    # Masukkan jawaban AI ke riwayat
    messages.append({
        "role": "assistant",
        "content": jawaban
    })

    print("Groq:", jawaban)
    print()