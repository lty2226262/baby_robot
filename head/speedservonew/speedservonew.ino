#include <Servo.h>


Servo myservoH_, myservoVlr_, myservoVfb_;

Servo myServos[3] = {myservoH_, myservoVlr_, myservoVfb_};
int currentAngles[3] = {90, 108, 90}; // 三个舵机, 头水平, 头俯仰, 脸蛋

const int initDelayTime = 30; //舵机初始化延时时间
const int moveDelayTime = 10; //舵机运动延时时间 最快为4，最慢是100
const int powerDelay = 1000; //运动完成后延时断电
const float pParament = 4.0; //PID control >0
const int trigPin = 8;
const int servoZeroPin = 9;
byte incomingByte[2];
unsigned char sign1=0;
int i = 0;
const int resolution = 1;
//float x[180];
//float y[180];
//int currentangleH=90;//三个舵机 头水平
//int currentangleVlr=90;//三个舵机 头俯仰
//int currentangleVfb=90;//三个舵机 脸蛋



float ComputeParament(float parament, int targetAngle, int k, int currentAngle){
  
  int scala = abs(currentAngle - targetAngle);
  if (targetAngle >= k){
    parament = 1- (targetAngle - k) / scala;
  } else {
    parament = 1- (k - targetAngle) / scala;
  }
  if (parament < 0.5) parament = 1 - parament;
  parament -= 1.0;
  parament *= pParament;
  parament += 1.0;
  
  if (parament < (float)4/moveDelayTime ) parament = 4/moveDelayTime;
  if (parament > (float)100/moveDelayTime) parament = 100/moveDelayTime;
  return parament;
}

void servoRun(int targetAngle, int servoNum){
  float parament;
  setTrig(HIGH);//HIGH
  myServos[servoNum].attach(servoNum + servoZeroPin,900,2100);
  if( (targetAngle-currentAngles[servoNum] )>0){
    for(int k=currentAngles[servoNum]; k <= targetAngle; ){
      k += resolution;
      //k += (int)(pParament * ( targetAngle - k));
      myServos[servoNum].write(k);
      parament = ComputeParament(parament, targetAngle, k, currentAngles[servoNum]);
      delay((int)(parament * moveDelayTime));
    }
  } else {
    for(int k=currentAngles[servoNum];k >= targetAngle;){
      k -= resolution;
      //k += (int)(pParament * ( targetAngle - k));
      myServos[servoNum].write(k);
      parament = ComputeParament(parament, targetAngle, k, currentAngles[servoNum]);
      delay((int)(parament * moveDelayTime));
    }
  }
  //myServos[servoNum].detach();
  delay(powerDelay);
  setTrig(LOW);//LOW
}

void setTrig(int trigState){
  digitalWrite(trigPin, trigState);
  delay(moveDelayTime);
}

void setup() {
  Serial.begin(9600);
  pinMode(trigPin,OUTPUT);
  setTrig(LOW);//LOW
  for (int i = 0; i < 3;i++){
    
    servoRun(currentAngles[i],i);
    delay(initDelayTime);
  }
}

void loop() {
  if (Serial.available() > 0) {
    // 读取传入的数据:
    incomingByte[i] = Serial.read();
    i++;
    if(i==2)
    {
      i=0;
      sign1=1;
    }

    if(sign1==1)
    {
      int angle = (unsigned int)incomingByte[1];
      Serial.write(incomingByte[0]);
      Serial.write(incomingByte[1]);
      sign1=0;
      if(incomingByte[0]==0x01)
      {
        servoRun( angle, 0);
        currentAngles[0] = angle;
      }
      if(incomingByte[0]==0x02)
      {
        servoRun( angle, 1);
        currentAngles[1] = angle;
      }
      if(incomingByte[0]==0x03)
      {
        servoRun( angle, 2);
        currentAngles[2] = angle;
      }
    }
  }
}
