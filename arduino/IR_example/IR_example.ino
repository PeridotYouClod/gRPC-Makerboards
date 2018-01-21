#include "IRremote.h"

//ir receiver setup
int IrReceiverPin = 11;
IRrecv irrecv(IrReceiverPin);
decode_results results;

void setup()
{
  Serial.begin(9600);

  irrecv.enableIRIn(); // Start the IrReceiverPin
}

void loop()
{
    int irVal = getIrValue();
    if(irVal != -1)
    {
      Serial.println(irVal + 1);
    }

    delay(100);//10 times a second seems like enough
}

//get the value from the ir sensor.
int getIrValue()
{
  int irVal = -1;
  if (irrecv.decode(&results)) // have we received an IR signal?
  {
    irVal = translateIR();
    irrecv.resume(); // receive the next value
  }
  return irVal;
}

// takes in the code from the remote and gives back a number
int translateIR()
{
  switch(results.value)
  {
    case 0xFF6897: return 0;
    case 0xFF30CF: return 1;
    case 0xFF18E7: return 2;
    case 0xFF7A85: return 3;
    case 0xFF10EF: return 4;
    case 0xFF38C7: return 5;
    case 0xFF5AA5: return 6;
    case 0xFF42BD: return 7;
    case 0xFF4AB5: return 8;
    case 0xFF52AD: return 9;
    case 0xFFE01F: return 10;
    case 0xFFA857: return 11;
    case 0xFF906F: return 12;
    case 0xFF9867: return 13;
    case 0xFFB04F: return 14;
    default:       return -1; //Serial.println(" other button   ");
  }
  //reset the device
  delay(25);
}
