#include <Keypad.h>

const uint8_t ROWS = 4;
const uint8_t COLS = 4;
char keys[ROWS][COLS] = {
  { '1', '2', '3', 'A' },
  { '4', '5', '6', 'B' },
  { '7', '8', '9', 'C' },
  { '*', '0', '#', 'D' }
};

uint8_t colPins[COLS] = { 5, 4, 3, 2 };
uint8_t rowPins[ROWS] = { 9, 8, 7, 6 };

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// Definir estados do automato
enum State {
  START,
  KP,
  KI,
  KD,
  TAU,
  TS,
  CONTROL_DIGITAL,
  CONTROL_CONTINUOUS,
  PLOT,
  CONTROL_TYPE
};

State currentState = START;
String tau = ""; // String para armazenar o valor de tau
String ts = ""; // String para armazenar o valor de ts

void setup() {
  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();
  int sensorValue;
  
  switch (currentState) {
    case START:
      if (key != NO_KEY) {
        switch (key) {
          case '1':
            currentState = KP;
            break;
          case '2':
            currentState = KI;
            break;
          case '3':
            currentState = KD;
            break;
          case '4':
            currentState = TAU;
            tau = ""; // Limpa o valor de tau ao iniciar a entrada
            break;
          case '5':
            currentState = TS;
            ts = ""; // Limpa o valor de ts ao iniciar a entrada
            break;
          case 'A':
            currentState = CONTROL_DIGITAL;
            break;
          case 'B':
            currentState = CONTROL_CONTINUOUS;
            break;
          case '0':
            currentState = PLOT;
            break;
          case 'C':
            currentState = CONTROL_TYPE;
            break;
        }
      }
      break;
      
    case KP:
      if (key != NO_KEY) {
        if (key == '#') {
          currentState = START;
          break;
        }
      }
      sensorValue = analogRead(A0);
      Serial.print("kp:");
      Serial.println(sensorValue);
      break;

    case KI:
      if (key != NO_KEY) {
        if (key == '#') {
          currentState = START;
          break;
        }
      }
      sensorValue = analogRead(A0);
      Serial.print("ki:");
      Serial.println(sensorValue);
      break;

    case KD:
      if (key != NO_KEY) {
        if (key == '#') {
          currentState = START;
          break;
        }
      }
      sensorValue = analogRead(A0);
      Serial.print("kd:");
      Serial.println(sensorValue);
      break;

    case TAU:
      if (key != NO_KEY) {
        if (key == '#') {
          Serial.print("Valor final de tau:");
          Serial.println(tau);
          currentState = START;
          break;
        }
        if (key >= '0' && key <= '9') {
          tau += key;
          Serial.print("tau:");
          Serial.println(tau);
        }
      }
      break;
      
    case TS:
      if (key != NO_KEY) {
        if (key == '#') {
          Serial.print("Valor final de ts:");
          Serial.println(ts);
          currentState = START;
          break;
        }
        if (key >= '0' && key <= '9') {
          ts += key;
          Serial.print("ts:");
          Serial.println(ts);
        }
        if (key == '*'){
          ts += '.';
          Serial.print("ts:");
          Serial.println(ts);
        }
      }
      break;
    
    case CONTROL_DIGITAL:
      Serial.println("control:Digital");
      currentState = START;
      break;
    
    case CONTROL_CONTINUOUS:
      Serial.println("control:Continuous");
      currentState = START;
      break;
    
    case PLOT:
      Serial.println("plot:true");
      currentState = START;
      break;
    
    case CONTROL_TYPE:
      switch (key){
        case 'A':
          Serial.println("control_type:p");
          break;
        case 'B':
          Serial.println("control_type:pi");
          break;
        case 'C':
          Serial.println("control_type:pd");
          break;
        case 'D':
          Serial.println("control_type:pid");
          break;
        case '#':
          currentState = START;
          break;
      }
      break;
  }
}
