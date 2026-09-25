import serial
import time

PORT = "/dev/ttyUSB0"
BAUDRATE = 115200

ser = serial.Serial(PORT, BAUDRATE, timeout=1)

print("TERHUBUNG KE ESP32")
print("Ketik perintah:")
print("  halo")
print("  terima kasih")
print("  tolong nyalakan lampunya")
print("  bisa matikan lampunya?")
print("  buat lampunya kelap-kelip")
print("Ketik EXIT untuk keluar.\n")

time.sleep(2)
ser.reset_input_buffer()

while True:
    text = input("> ")

    if text.upper() == "EXIT":
        break

    ser.write((text + "\n").encode())
    ser.flush()

    time.sleep(0.5)

    while ser.in_waiting:
        data = ser.readline().decode(errors="ignore").strip()
        if data:
            print("ESP32:", data)

ser.close()
print("Serial ditutup.")
