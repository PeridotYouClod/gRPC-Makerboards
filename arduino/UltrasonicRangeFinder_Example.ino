#include <Ultrasonic.h>

//ultrasonic range finder setup
int triggerPin =  10;
int echoPin = 9;
int maxDistance = 375;
Ultrasonic sonar(triggerPin, echoPin);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
    int sonarVal = sonar.Ranging(CM);

    Serial.flush();
    Serial.println(sonarVal);

    delay(100);//10 times a second seems like enough
}
