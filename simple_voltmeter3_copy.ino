//const int analogInPin = A0;  // Analog input pin on Arduino
//const int refPin = A0;  // Analog input pin on Arduino

void setup() {
    Serial.begin(9600);
}

void loop() {
  long sum =0;
  for (int i = 0; i < 128; i++) {
    sum+=analogRead(A0);
    sum+=analogRead(A1);
    sum+=analogRead(A2);
    sum+=analogRead(A3);
    sum+=analogRead(A4);
    sum+=analogRead(A5);
    sum+=analogRead(A6);
  }
    //float voltage = sensorValue * (5.0 / 1023.0);  // Convert analog reading to voltage
    Serial.println(sum);
   // delay(40);  // Adjust the delay as needed
}