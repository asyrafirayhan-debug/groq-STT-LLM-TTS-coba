void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "ON") {
      Serial.println("LED_ON");
    }
    else if (command == "OFF") {
      Serial.println("LED_OFF");
    }
    else {
      Serial.print("RECEIVED: ");
      Serial.println(command);
    }
  }
}
void setup() {
  pinMode(2, OUTPUT);
  Serial.begin(115200);

  Serial.println("ESP32 READY");
}

void loop() {
  // Blink LED
  digitalWrite(2, HIGH);
  delay(1000);

  digitalWrite(2, LOW);
  delay(1000);

  // Cek perintah dari komputer
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "ON") {
      digitalWrite(2, HIGH);
      Serial.println("LED_ON");
    }
    else if (command == "OFF") {
      digitalWrite(2, LOW);
      Serial.println("LED_OFF");
    }
    else {
      Serial.print("RECEIVED: ");
      Serial.println(command);
    }
  }
}
