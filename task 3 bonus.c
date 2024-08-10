#include <Servo.h>

const int trigPinFront = 2;
const int echoPinFront = 3;
const int trigPinRight = 4;
const int echoPinRight = 5;
const int trigPinLeft = 6;
const int echoPinLeft = 7;
const int trigPinBack = A2;
const int echoPinBack = A3;
const int photoresistorPin = A0;
const int buzzerPin = 8;
const int servoPin = 9;
const int motorPin1 = 10;
const int motorPin2 = 11;
const int motorPin3 = 12;
const int motorPin4 = 13;

Servo defuseServo;
int x = 0, y = 0;
int direction = 0;

long readDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  long distance = duration * 0.034 / 2;
  return distance;
}

void moveForward() {
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, LOW);
  delay(1000);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin3, LOW);
  if (direction == 0) y++;
  else if (direction == 1) x++;
  else if (direction == 2) y--;
  else if (direction == 3) x--;
  Serial.print("Current Position: ");
  Serial.print(x);
  Serial.print(", ");
  Serial.println(y);
}

void yawRight() {
  digitalWrite(motorPin1, HIGH);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, HIGH);
  delay(1000);
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin4, LOW);
  direction = (direction + 1) % 4;
}

void yawLeft() {
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, HIGH);
  digitalWrite(motorPin3, HIGH);
  digitalWrite(motorPin4, LOW);
  delay(1000);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  direction = (direction + 3) % 4;
}

void setup() {
  Serial.begin(9600);
  pinMode(trigPinFront, OUTPUT);
  pinMode(echoPinFront, INPUT);
  pinMode(trigPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);
  pinMode(trigPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  pinMode(trigPinBack, OUTPUT);
  pinMode(echoPinBack, INPUT);
  pinMode(photoresistorPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  defuseServo.attach(servoPin);
  defuseServo.write(0);
}

void loop() {
  long distanceFront = readDistance(trigPinFront, echoPinFront);
  long distanceRight = readDistance(trigPinRight, echoPinRight);
  long distanceLeft = readDistance(trigPinLeft, echoPinLeft);
  long distanceBack = readDistance(trigPinBack, echoPinBack);
  
  int lightLevel = analogRead(photoresistorPin);
  int threshold = 500;
  if (lightLevel < threshold) {
    digitalWrite(buzzerPin, HIGH);
    Serial.println("Mine detected!");
    defuseServo.write(90);
    delay(1000);
    defuseServo.write(0);
    digitalWrite(buzzerPin, LOW);
    Serial.println("Mine defused!");
  }

  if (distanceFront < 20) {
    if (distanceRight > distanceLeft) {
      yawRight();
    } else {
      yawLeft();
    }
  } else {
    moveForward();
  }

  if (distanceBack < 20) {
    Serial.println("Obstacle detected at the back!");
  }

  delay(500);
}
