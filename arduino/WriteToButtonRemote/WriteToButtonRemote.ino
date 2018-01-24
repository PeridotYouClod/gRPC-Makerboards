/*
 * We are going to be using serial for both sending and recieving messages
 * This means we need to define a few opcodes to make sure the proper data transformations occure when asked for
 * and we dont go into an infinite self spamming loop
 */

String possibleSerial;
char incomingByte;
bool debug;

// Set up pins
int RF_ON_1 = 2;
int RF_OFF_1 = 3;

int RF_ON_2 = 4;
int RF_OFF_2 = 5;

int RF_ON_3 = 6;
int RF_OFF_3 = 7;

int RF_ON_4 = 8;
int RF_OFF_4 = 9;

int RF_ON_5 = 10;
int RF_OFF_5 = 11;

// Length of time to hold down button
int BUTTON_PRESS_DELAY = 500;

void setup() {
  debug = false;
  
  Serial.begin(9600);
  
  pinMode(RF_ON_1, OUTPUT);
  pinMode(RF_OFF_1, OUTPUT);
  
  pinMode(RF_ON_2, OUTPUT);
  pinMode(RF_OFF_2, OUTPUT);
  
  pinMode(RF_ON_3, OUTPUT);
  pinMode(RF_OFF_3, OUTPUT);
  
  pinMode(RF_ON_4, OUTPUT);
  pinMode(RF_OFF_4, OUTPUT);
  
  pinMode(RF_ON_5, OUTPUT);
  pinMode(RF_OFF_5, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = (char)(Serial.read());
    possibleSerial += incomingByte;
    delay(10);
  }
  if(possibleSerial.length()) {
    debugPrint(possibleSerial);
  //  switch for checking each of our opcodes
    switch(possibleSerial.toInt()) {
  // 3 bits for address of button, 1 bit for state
      case 100: pressButton(RF_OFF_1); break;
      case 101: pressButton(RF_ON_1); break;
      case 200: pressButton(RF_OFF_2); break;
      case 201: pressButton(RF_ON_2); break;
      case 300: pressButton(RF_OFF_3); break;
      case 301: pressButton(RF_ON_3); break;
      case 400: pressButton(RF_OFF_4); break;
      case 401: pressButton(RF_ON_4); break;
      case 500: pressButton(RF_OFF_5); break;
      case 501: pressButton(RF_ON_5); break;
      default:
        debugPrint("bad data sent " + possibleSerial);
    }
  }

  // cleanup for next possible data input check
  possibleSerial = "";
  delay(50);
}

void pressButton(int button) {
  digitalWrite(button, HIGH);
  delay(BUTTON_PRESS_DELAY);
  digitalWrite(button, LOW);
}

void debugPrint(String message) {
  if(debug){
    Serial.println(message);
  }
}

