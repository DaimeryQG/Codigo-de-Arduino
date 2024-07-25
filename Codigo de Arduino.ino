#include <Wire.h>
#include <Servo.h>
#define ENA 7 
#define IN1 6
#define IN2 5
#define ENB 1
#define IN3 2
#define IN4 3

int velocidad = 0; // Inicializa la velocidad a 200
unsigned char comando;
Servo myservo;
const int trigPin = A1;
const int echoPin = A0;
bool scanning = false;


void setup() {
  myservo.attach(A2);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600); // Inicializa la comunicación serial
  delay(1000);
}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();
    Serial.println(comando);
    switch (comando) {
      case 'E':
        motorAdelante();
        break;
      case 'A':
        motorApagar();
        break;
      case 'V':
        ajustarVelocidad();
        break;
      case 'I':
        motorIzquierda();
        break;
      case 'D':
        motorDerecha();
        break;
      case 'R':
        motorAtras();
        break;
      case 'S':
        motorDetener();
        break;
      case 'H':
        if (!scanning) {
          motorDetener();
          scanning = true;
          moveAndCheckDistance(90);
          moveAndCheckDistance(160);
          moveAndCheckDistance(90);
          moveAndCheckDistance(20);
          moveAndCheckDistance(90);
          scanning = false;
        }
        break;
      case 'J':
        motorDetener();
        scanning = false;
        break;
      default:
        break;
    }
  }
}

float checkdistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  float duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2.0; // Speed of sound is 343 m/s or 0.034 cm/microsecond

  return distance;
}

void moveAndCheckDistance(int angle) {
  myservo.write(angle);
  delay(3000);
  float distance = checkdistance();
  Serial.print("Distance at ");
  Serial.print(angle);
  Serial.print(" degrees: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Envía la distancia a través del puerto serial
  Serial.print("D ");  // Marca para indicar que es una distancia
  Serial.println(distance);
}

void motorAdelante() {
  // Enciende el motor hacia adelante
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  actualizarVelocidad();
  Serial.println("Motor encendido hacia adelante");
}

void motorAtras() {
  // Enciende el motor hacia atrás
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  actualizarVelocidad();
  Serial.println("Motor encendido hacia atrás");
}

void motorDerecha() {
  // Enciende el motor hacia la derecha
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  actualizarVelocidad();
  Serial.println("Motor encendido hacia la derecha");
}

void motorIzquierda() {
  // Enciende el motor hacia la izquierda
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  actualizarVelocidad();
  Serial.println("Motor encendido hacia la izquierda");
}

void motorDetener() {
  // Detiene el motor
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, HIGH);
  actualizarVelocidad();
  Serial.println("Motor Detenido");
}

void motorApagar() {
  // Apaga el motor
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  actualizarVelocidad();
  Serial.println("Motor apagado");
}

void ajustarVelocidad() {
  // Lee y ajusta la velocidad del motor
  velocidad = Serial.parseInt();
  if( velocidad < 0){
    velocidad = 0;
  } else if (velocidad > 255) {
    velocidad = 255;
  }
  // velocidad = constrain(velocidad, 0, 255); // Asegura que la velocidad esté en el rango correcto
  actualizarVelocidad();
  Serial.print("Velocidad cambiada a ");
  Serial.println(velocidad);
}

void actualizarVelocidad() {
  analogWrite(ENA, velocidad);
  analogWrite(ENB, velocidad);
}