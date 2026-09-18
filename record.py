import sounddevice as sd
import soundfile as sf
import numpy as np

DURATION = 5
SAMPLE_RATE = 16000
OUTPUT = "audio/test.wav"

print("Mulai merekam...")
print("Silakan bicara selama 5 detik...")

try:
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    # Cek apakah benar-benar ada suara
    volume = np.max(np.abs(audio))

    if volume < 0.01:
        print("⚠️ Volume suara sangat kecil atau tidak ada suara.")

    sf.write(OUTPUT, audio, SAMPLE_RATE)

    print(f"Selesai. File tersimpan di: {OUTPUT}")

except Exception as e:
    print(f"❌ Gagal merekam: {e}")
    raise