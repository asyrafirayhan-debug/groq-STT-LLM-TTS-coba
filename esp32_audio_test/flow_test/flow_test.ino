	String inputText = "";

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);

  Serial.println();
  Serial.println("======================================");
  Serial.println(" ESP32 VOICE FLOW SIMULATOR");
  Serial.println("======================================");
  Serial.println("Contoh:");
  Serial.println("  tolong nyalakan lampunya");
  Serial.println("  bisa matikan lampu?");
  Serial.println("  buat lampunya kelap-kelip");
  Serial.println("  halo");
  Serial.println();
}

String detectCommand(String text) {

  text.toLowerCase();
  text.trim();

  // BLINK
  if (
    text.indexOf("kelap") >= 0 ||
    text.indexOf("kedip") >= 0 ||
    text.indexOf("berkedip") >= 0 ||
    text.indexOf("blink") >= 0
  ) {
    return "BLINK";
  }

  // ON
  if (
    text.indexOf("nyalakan") >= 0 ||
    text.indexOf("nyala") >= 0 ||
    text.indexOf("hidupkan") >= 0 ||
    text.indexOf("hidup") >= 0
  ) {
    return "ON";
  }

  // OFF
  if (
    text.indexOf("matikan") >= 0 ||
    text.indexOf("mati") >= 0 ||
    text.indexOf("padamkan") >= 0 ||
    text.indexOf("padam") >= 0
  ) {
    return "OFF";
  }

  // GREETING
  if (
    text.indexOf("halo") >= 0 ||
    text.indexOf("hai") >= 0 ||
    text.indexOf("hi") >= 0
  ) {
    return "GREETING";
  }

  // THANKS
  if (
    text.indexOf("terima kasih") >= 0 ||
    text.indexOf("makasih") >= 0 ||
    text.indexOf("thanks") >= 0
  ) {
    return "THANKS";
  }

  return "UNKNOWN";
}

  


void executeCommand(String command) {

  if (command == "ON") {

    digitalWrite(2, HIGH);

    Serial.println("ACTION  : GPIO 2 HIGH");
    Serial.println("RESPONSE: Baik, lampu sudah dinyalakan.");
  }

  else if (command == "OFF") {

    digitalWrite(2, LOW);

    Serial.println("ACTION  : GPIO 2 LOW");
    Serial.println("RESPONSE: Baik, lampu sudah dimatikan.");
  }

  else if (command == "BLINK") {

    Serial.println("ACTION  : BLINK");

    for (int i = 0; i < 5; i++) {

      digitalWrite(2, HIGH);
      delay(300);

      digitalWrite(2, LOW);
      delay(300);
    }

    Serial.println("RESPONSE: Baik, lampu dibuat berkedip.");
  }

  else {

    Serial.println("ACTION  : NONE");
    Serial.println("RESPONSE: Maaf, saya belum memahami perintah tersebut.");
  }
}


void processInput(String text) {

  text.trim();

  if (text.length() == 0) {
    return;
  }

  Serial.println();
  Serial.println("--------------------------------------");

  Serial.print("INPUT   : ");
  Serial.println(text);

  String command = detectCommand(text);

  Serial.print("INTENT  : ");
  Serial.println(command);

  executeCommand(command);

  Serial.println("--------------------------------------");
  Serial.println("Silakan bicara/masukkan teks lagi.");
}


void loop() {

  while (Serial.available()) {

    char c = Serial.read();

    if (c == '\n' || c == '\r') {

      if (inputText.length() > 0) {

        processInput(inputText);

        inputText = "";
      }

    } else {

      inputText += c;
    }
  }
}
