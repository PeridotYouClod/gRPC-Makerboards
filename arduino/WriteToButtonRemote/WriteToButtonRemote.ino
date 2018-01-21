/*
 * We are going to be using serial for both sending and recieving messages
 * This means we need to define a few opcodes to make sure the proper data transformations occure when asked for
 * and we dont go into an infinite self spamming loop
 */

String possibleSerial;
char incomingByte;

int rfOnButton, rfOffButton, buttonPressDelay;

bool debug;

void setup() {
  debug = false;
  
  Serial.begin(9600);
  rfOffButton = 2;
  rfOnButton = 3;
  buttonPressDelay = 500;
  
  pinMode(rfOnButton, OUTPUT);
  pinMode(rfOffButton, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = (char)(Serial.read());
    possibleSerial += incomingByte;
  }
  if(possibleSerial.length()) {
    debugPrint(possibleSerial);
  //  switch for checking each of our opcodes
    switch(possibleSerial.toInt()) {
  // 3 bits for address of button, 1 bit for state
      case 101:  // turn on the radio button
        debugPrint("turning on the rf button");
        digitalWrite(rfOnButton, HIGH);
        delay(buttonPressDelay);
        digitalWrite(rfOnButton, LOW);
        break;
      case 100:  // turn off the radio button
        debugPrint("turning off the rf button");
        digitalWrite(rfOffButton, HIGH);
        delay(buttonPressDelay);
        digitalWrite(rfOffButton, LOW);
        break;
      default:
        debugPrint("bad data sent " + possibleSerial);
    }
  }


//  cleanup for next possible data input check
  possibleSerial = "";
  delay(50);
}

void debugPrint(String message) {
  if(debug){
    Serial.println(message);
  }
}

