#include <BluetoothSerial.h>
#include <Stepper.h>

BluetoothSerial SerialBT; 
const int steps_per_rev = 2048;  

#define IN1 26
#define IN2 25
#define IN3 33
#define IN4 32

Stepper motor(steps_per_rev, IN1, IN3, IN2, IN4);
void setup() {
  motor.setSpeed(15);
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT");  
}

void loop() {
  
  if(SerialBT.available()){Serial.println("");}
  while(SerialBT.available())
  {
    char btdata=SerialBT.read();
    if (btdata=='1'){
          for(int i=0;i<4;i++){
            motor.step(steps_per_rev);
            if (SerialBT.available()){break;}
          }
    }
    if (btdata=='2'){
      for(int i=0;i<3;i++){
            motor.step(-steps_per_rev);
            if (SerialBT.available()){break;}
          }  
      }
    if (btdata=='3'){
       Serial.println("stop");  
    }
    Serial.print(btdata);
  }  
  delay(500);
}
