const int LED_PIN = 2;

unsigned long previousMillis = 0;
const unsigned long blinkInterval = 1000;

bool blinkState = false;
bool manualMode = false;

String command = "";

void setup() {
  pinMode(LED_PIN, OUTPUT);

  Serial.begin(115200);
  delay(500);

  Serial.println("ESP32 READY");
  Serial.println("Commands: ON, OFF, BLINK");
}

void loop() {
  // =========================
  // BLINK NON-BLOCKING
  // =========================
  if (!manualMode) {
    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= blinkInterval) {
      previousMillis = currentMillis;

      blinkState = !blinkState;
      digitalWrite(LED_PIN, blinkState);
    }
  }

  // =========================
  // SERIAL COMMAND
  // =========================
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n' || c == '\r') {
      if (command.length() > 0) {

        command.trim();
        command.toUpperCase();

        if (command == "ON") {
          manualMode = true;
          digitalWrite(LED_PIN, HIGH);
          Serial.println("LED_ON");
        }

        else if (command == "OFF") {
          manualMode = true;
          digitalWrite(LED_PIN, LOW);
          Serial.println("LED_OFF");
        }

        else if (command == "BLINK") {
          manualMode = false;
          Serial.println("BLINK_MODE");
        }

        else {
          Serial.print("RECEIVED: ");
          Serial.println(command);
        }

        command = "";
      }
    }

    else {
      command += c;
    }
  }
}
