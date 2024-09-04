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

void setup() {
  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();
  int sensorValue;
  
  //Serial.println(key);

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
            break;
          case '5':
            currentState = TS;
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
          currentState = START;
          break;
        }
        Serial.print("tau:");
        Serial.println(key);
      }
      break;
      
    case TS:
      if (key != NO_KEY) {
        if (key == '#') {
          currentState = START;
          break;
        }
        Serial.print("ts:");
        Serial.println(key);
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
  }
}
