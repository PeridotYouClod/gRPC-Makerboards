#include <NewPing.h>

#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
unsigned int last_distance = 0;

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup() {
  Serial.begin(9600); // Open serial monitor at 115200 baud to see ping results.
}

void loop() {
  delay(300);
  unsigned int ping = sonar.ping(); // Send ping, get ping time in microseconds (uS).
  unsigned int distsance = ping / US_ROUNDTRIP_CM;
  if(distsance != last_distance) {
    Serial.print("Ping: ");
    Serial.print(distance); // Convert ping time to distance and print result (0 = outside set distance range, no ping echo)
    Serial.println("cm");
    last_distance = distance;
  }
}
