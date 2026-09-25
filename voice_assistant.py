import os
import sys
import subprocess
import asyncio
import time
import serial
import edge_tts

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# KONFIGURASI ESP32
# ============================================================

ESP32_PORT = "/dev/ttyUSB0"
ESP32_BAUDRATE = 115200


# ============================================================
# LOAD GROQ API KEY
# ============================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# HUBUNGKAN KE ESP32
# ============================================================

try:
    esp32 = serial.Serial(
        port=ESP32_PORT,
        baudrate=ESP32_BAUDRATE,
        timeout=1
    )

    # ESP32 biasanya restart ketika serial dibuka
    time.sleep(2)

    # Bersihkan pesan startup ESP32
    esp32.reset_input_buffer()

    print("🔌 ESP32 terhubung.")
    print(f"   Port: {ESP32_PORT}")
    print(f"   Baudrate: {ESP32_BAUDRATE}\n")

except Exception as e:

    esp32 = None

    print("⚠️ ESP32 tidak terhubung.")
    print(f"   Error: {e}\n")


# ============================================================
# KONTROL ESP32
# ============================================================

def control_esp32(command):

    if esp32 is None:
        return False, "ESP32 tidak terhubung."

    try:

        # Kirim perintah ke ESP32
        esp32.write(
            (command + "\n").encode()
        )

        esp32.flush()

        # Tunggu ESP32 memberikan respon
        time.sleep(0.2)

        responses = []

        while esp32.in_waiting:

            response = esp32.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if response:
                responses.append(response)

        return True, responses

    except Exception as e:

        return False, str(e)


# ============================================================
# DETEKSI PERINTAH LAMPU
# ============================================================

def detect_command(text):

    text = text.lower().strip()

    # --------------------------------------------------------
    # LAMPU ON
    # --------------------------------------------------------

    on_commands = [
        "nyalakan lampu",
        "hidupkan lampu",
        "lampu nyala",
        "lampu hidup",
        "nyalakan lampunya",
        "hidupkan lampunya",
        "tolong nyalakan lampu",
        "tolong hidupkan lampu"
    ]

    for command in on_commands:

        if command in text:
            return "ON"


    # --------------------------------------------------------
    # LAMPU OFF
    # --------------------------------------------------------

    off_commands = [
        "matikan lampu",
        "padamkan lampu",
        "lampu mati",
        "matikan lampunya",
        "padamkan lampunya",
        "tolong matikan lampu",
        "tolong padamkan lampu"
    ]

    for command in off_commands:

        if command in text:
            return "OFF"


    # --------------------------------------------------------
    # LAMPU BLINK
    # --------------------------------------------------------

    blink_commands = [
        "kedipkan lampu",
        "buat lampu berkedip",
        "buat lampunya berkedip",
        "lampu berkedip",
        "lampu kedip",
        "nyalakan mode kedip",
        "aktifkan mode kedip",
        "tolong kedipkan lampu"

        # Variasi kelap-kelip
        "buat lampu kelap-kelip",
        "buat lampunya kelap-kelip",
        "lampu kelap-kelip",
        "lampu kelap kelip",
        "kelap-kelipkan lampu",
        "kelap kelipkan lampu",
        "buat lampu berkedip-kedip",
        "buat lampunya berkedip-kedip"
    ]

    for command in blink_commands:

        if command in text:
            return "BLINK"


    # Tidak ada perintah perangkat
    return None


# ============================================================
# TEXT TO SPEECH
# ============================================================

async def speak(text):

    communicate = edge_tts.Communicate(
        text,
        "id-ID-ArdiNeural"
    )

    await communicate.save(
        "audio/response.mp3"
    )


# ============================================================
# VOICE ASSISTANT
# ============================================================

print("======================================")
print("       GROQ VOICE ASSISTANT")
print("======================================")
print("Kontrol:")
print("  - Nyalakan lampu")
print("  - Matikan lampu")
print("  - Kedipkan lampu")
print()
print("Tekan Ctrl+C untuk berhenti.")
print("======================================\n")


while True:

    try:

        # ====================================================
        # 1. RECORDING
        # ====================================================

        print("🎤 Silakan bicara selama 5 detik...")

        subprocess.run(
            [sys.executable, "record.py"],
            check=True
        )


        # ====================================================
        # 2. SPEECH TO TEXT
        # ====================================================

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


        # ====================================================
        # AMBIL HASIL STT
        # ====================================================

        if "=== HASIL STT ===" in output:

            text = output.split(
                "=== HASIL STT ===",
                1
            )[1].strip()

        else:

            text = output.strip()


        print("\n=== TEKS KAMU ===")
        print(text)


        # ====================================================
        # 3. CEK SUARA
        # ====================================================

        if not text or text == ".":

            print(
                "⚠️ Suara tidak terdeteksi. "
                "Coba lagi.\n"
            )

            continue


        # ====================================================
        # 4. DETEKSI PERINTAH ESP32
        # ====================================================

        command = detect_command(text)


        # ====================================================
        # JIKA PERINTAH ESP32 DITEMUKAN
        # ====================================================

        if command is not None:

            print("\n💡 Perintah ESP32 terdeteksi:")
            print(f"   {command}")


            # ------------------------------------------------
            # KIRIM PERINTAH KE ESP32
            # ------------------------------------------------

            success, response = control_esp32(command)


            if success:

                print("📡 Respon ESP32:")

                if response:

                    for line in response:
                        print(f"   {line}")

                else:

                    print("   Tidak ada respon.")


                # --------------------------------------------
                # JAWABAN SUARA
                # --------------------------------------------

                if command == "ON":

                    answer = (
                        "Baik, lampu sudah dinyalakan."
                    )

                elif command == "OFF":

                    answer = (
                        "Baik, lampu sudah dimatikan."
                    )

                elif command == "BLINK":

                    answer = (
                        "Baik, lampu sekarang berkedip."
                    )

                else:

                    answer = (
                        "Perintah berhasil dijalankan."
                    )


            else:

                print(
                    f"❌ Gagal mengontrol ESP32: {response}"
                )

                answer = (
                    "ESP32 belum terhubung, "
                    "jadi saya belum bisa mengontrol lampu."
                )


        # ====================================================
        # 5. JIKA BUKAN PERINTAH ESP32 → GROQ
        # ====================================================

        else:

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


            answer = (
                response
                .choices[0]
                .message
                .content
            )


        # ====================================================
        # 6. PRINT ANSWER
        # ====================================================

        print(
            "\n=== JAWABAN ==="
        )

        print(answer)

        print()


        # ====================================================
        # 7. TEXT TO SPEECH
        # ====================================================

        print(
            "🔊 Membacakan jawaban..."
        )


        asyncio.run(
            speak(answer)
        )


        # ====================================================
        # 8. PLAY AUDIO
        # ====================================================

        subprocess.run([
    "powershell.exe",
    "-Command",
    "Start-Process",
    r"audio\response.mp3"
])


        print(
            "\n✅ Selesai. "
            "Silakan bicara lagi.\n"
        )


    # ========================================================
    # CTRL + C
    # ========================================================

    except KeyboardInterrupt:

        print(
            "\n\n🛑 Program dihentikan."
        )

        break


    # ========================================================
    # ERROR LAIN
    # ========================================================

    except Exception as e:

        print(
            f"\n❌ Terjadi error: {e}\n"
        )


# ============================================================
# TUTUP SERIAL ESP32
# ============================================================

if esp32 is not None:

    try:

        esp32.close()

        print("🔌 Koneksi ESP32 ditutup.")

    except Exception:
        pass