
#define LOplus 10
#define LOminus 11
#define output A0

void setup() {
  Serial.begin(9600); // set the baud rate
  pinMode(LOplus, INPUT);
  pinMode(LOminus, INPUT);
  pinMode(output, INPUT);
}

void loop() {
	// if any of the electrodes is off
  if ((digitalRead(LOplus) == 1) || (digitalRead(LOminus) == 1)) {
    Serial.println('!');
  }
  else {
    Serial.println(analogRead(output));
  }
  delay(1);
}
