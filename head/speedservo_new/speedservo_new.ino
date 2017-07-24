#include <Servo.h>
#define ROTATION_RANGE 180
#define DATA_LENGTH 6
#define DEBUG

Servo myservoH_, myservoVlr_, myservoVfb_;

Servo myServos[3] = {myservoH_, myservoVlr_, myservoVfb_};
int currentAngles[3] = {90, 108, 90}; // 三个舵机, 头水平, 头俯仰, 脸蛋 yaw, pitch, roll
const int trigPin = 2, servoZeroPin = 9, powerDelay =  800;

byte buf[DATA_LENGTH];
unsigned char sign1 = 0;
int read_index = 0;
int stop_flag = 0;
int temp_angles[3];

void servo_run_all(int yaw, int pitch, int roll){
  setTrig(HIGH);
  temp_angles[0] = yaw;
  temp_angles[1] = pitch;
  temp_angles[2] = roll;
  for (int i = 0; i < 3; i++){
    myServos[i].write(temp_angles[i]);
  }
}

void setTrig(int trigState){
  digitalWrite(trigPin, trigState);
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++){
    myServos[i].attach(i + servoZeroPin, 900, 2100);
  }
  pinMode(trigPin,OUTPUT);
  servo_run_all(currentAngles[0],currentAngles[1],currentAngles[2]);
  delay(powerDelay);
  setTrig(LOW);//LOW
}

void loop() {
  if (Serial.available() > 0){
    //读入数据
    byte one_byte;
    one_byte = Serial.read();
    if (one_byte == 0xAA && read_index == 0){
      read_index = 1;
    }
    #ifdef DEBUG
    Serial.write(one_byte);
    #endif
    if (read_index > 0 && read_index <= DATA_LENGTH){
      buf[read_index - 1] = one_byte;
      read_index++;
    } else if (read_index > DATA_LENGTH){
      read_index = 0;
    } else{
      //pass
    }
    if (one_byte == 0x55 && read_index == DATA_LENGTH + 1){
      int yaw = (unsigned int)buf[1];
      int pitch = (unsigned int)buf[2];
      int roll = (unsigned int)buf[3];
      servo_run_all(yaw, pitch, roll);
      if ((unsigned int)buf[4] == 1){
        delay(powerDelay);
        setTrig(LOW);
      }
      #ifdef DEBUG
      Serial.write(buf[1]);
      Serial.write(buf[2]);
      Serial.write(buf[3]);
      Serial.write(buf[4]);
      Serial.write(read_index);
      #endif
      read_index = 0;
      currentAngles[0] = yaw;
      currentAngles[1] = pitch;
      currentAngles[2] = roll;
    }
  }
}
