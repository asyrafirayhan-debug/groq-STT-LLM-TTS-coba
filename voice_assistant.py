
import os
import sys
import subprocess
import asyncio
import edge_tts

from dotenv import load_dotenv
from groq import Groq


# =========================
# LOAD GROQ API KEY
# =========================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================
# TEXT TO SPEECH
# =========================

async def speak(text):
    communicate = edge_tts.Communicate(
        text,
        "id-ID-ArdiNeural"
    )

    await communicate.save(
        "audio/response.mp3"
    )


# =========================
# VOICE ASSISTANT
# =========================

print("=== GROQ VOICE ASSISTANT ===")
print("Tekan Ctrl+C untuk berhenti.\n")


while True:

    try:

        # -------------------------
        # 1. RECORDING
        # -------------------------

        print("🎤 Silakan bicara selama 5 detik...")

        subprocess.run(
            [sys.executable, "record.py"],
            check=True
        )


        # -------------------------
        # 2. SPEECH TO TEXT
        # -------------------------

        print("📝 Mengubah suara menjadi teks...")

        result = subprocess.run(
            [sys.executable, "stt.py"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )


        # Kalau STT gagal
        if result.returncode != 0:

            print("❌ STT gagal:")
            print(result.stderr)

            continue


        output = result.stdout


        # Ambil teks setelah
        # === HASIL STT ===

        if "=== HASIL STT ===" in output:

            text = output.split(
                "=== HASIL STT ===",
                1
            )[1].strip()

        else:

            text = output.strip()


        print("\n=== TEKS KAMU ===")
        print(text)


        # -------------------------
        # 3. CEK SUARA
        # -------------------------

        if not text or text == ".":

            print(
                "⚠️ Suara tidak terdeteksi. "
                "Coba lagi.\n"
            )

            continue


        # -------------------------
        # 4. GROQ
        # -------------------------

        print(
            "\n🤖 Mengirim pertanyaan ke Groq..."
        )


        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[

                {
                    "role": "system",

                    "content": (
                        "Kamu adalah asisten AI "
                        "suara yang ramah, jelas, "
                        "dan membantu. "
                        "Jawablah dalam bahasa Indonesia. "
                        "Jawaban harus singkat dan "
                        "mudah didengar ketika dibacakan "
                        "oleh suara."
                    )
                },

                {
                    "role": "user",
                    "content": text
                }

            ]
        )


        answer = response.choices[0].message.content


        # -------------------------
        # 5. PRINT ANSWER
        # -------------------------

        print(
            "\n=== JAWABAN GROQ ==="
        )

        print(answer)

        print()


        # -------------------------
        # 6. TEXT TO SPEECH
        # -------------------------

        print(
            "🔊 Membacakan jawaban..."
        )


        asyncio.run(
            speak(answer)
        )


        # -------------------------
        # 7. PLAY AUDIO
        # -------------------------

        os.system(
            'start "" "audio\\response.mp3"'
        )


        print(
            "\n✅ Selesai. "
            "Silakan bicara lagi.\n"
        )


    # =========================
    # CTRL + C
    # =========================

    except KeyboardInterrupt:

        print(
            "\nProgram dihentikan."
        )

        break


    # =========================
    # OTHER ERROR
    # =========================

    except Exception as e:

        print(
            f"\n❌ Terjadi error: {e}\n"
        )