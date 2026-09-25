import serial
import time

PORT = "/dev/ttyUSB0"
BAUDRATE = 115200

print(f"Membuka {PORT}...")

ser = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    timeout=1
)

print("ESP32 terhubung.")
print("Perintah: ON / OFF / BLINK / EXIT")

# Tunggu ESP32 reset setelah serial dibuka
time.sleep(2)

# Bersihkan pesan boot yang sudah masuk
ser.reset_input_buffer()

while True:
    command = input("> ").strip().upper()

    if command == "EXIT":
        break

    if command not in ["ON", "OFF", "BLINK"]:
        print("Perintah tidak dikenal.")
        continue

    ser.write((command + "\n").encode())
    ser.flush()

    time.sleep(0.2)

    while ser.in_waiting:
        response = ser.readline().decode("utf-8", errors="ignore").strip()
        if response:
            print(f"ESP32: {response}")

ser.close()
print("Serial ditutup.")
