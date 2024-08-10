const int trigPin = 9;
const int echoPin = 10;
const int thresholdDistance = 200;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  long duration, distance;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  if (distance <= thresholdDistance) {
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
    Serial.println("Object detected!");
  }

  delay(700);
}
