#include <Servo.h>
#define ROTARION_RANGE 180


Servo myservoH_, myservoVlr_, myservoVfb_;

Servo myServos[3] = {myservoH_, myservoVlr_, myservoVfb_};
int currentAngles[3] = {90, 108, 90}; // 三个舵机, 头水平, 头俯仰, 脸蛋

const int initDelayTime = 30; //舵机初始化延时时间
const int moveDelayTime = 10; //舵机运动延时时间 最快为4，最慢是10
const int moveDelayMin = 4;
const int moveDelayMax = 100;
const int powerDelay = 1000; //运动完成后延时断电
const float pParament = 4.0; //PID control >0
const int trigPin = 8;
const int servoZeroPin = 9;
const int resolution = 1;
const float weight_smooth = 0.1;
const float tolerance = 0.00001;
const float accelerate_limit = 0.5;

byte incomingByte[2];
unsigned char sign1 = 0;
int i = 0;
float new_path[ROTARION_RANGE];
int flexible[ROTARION_RANGE];


//float x[180];
//float y[180];
//int currentangleH=90;//三个舵机 头水平
//int currentangleVlr=90;//三个舵机 头俯仰
//int currentangleVfb=90;//三个舵机 脸蛋



// float ComputeParament(float parament, int targetAngle, int k, int currentAngle){
//
//   int scala = abs(currentAngle - targetAngle);
//   if (targetAngle >= k){
//     parament = 1- (targetAngle - k) / scala;
//   } else {
//     parament = 1- (k - targetAngle) / scala;
//   }
//   if (parament < 0.5) parament = 1 - parament;
//   parament -= 1.0;
//   parament *= pParament;
//   parament += 1.0;
//
//   if (parament < (float)moveDelayMin /moveDelayTime ) parament = moveDelayMin/moveDelayTime;
//   if (parament > (float)moveDelayMax /moveDelayTime) parament = moveDelayMax/moveDelayTime;
//   return parament;
// }

void PathInitialize(){
  for( int i = 0; i < ROTARION_RANGE; i++){
    new_path[i] = 0;
    flexible[i] = 0;
  }
}

void Smooth(){
  float error = tolerance;
  float aux;
  while (error >= tolerance){
    error = 0;
    for (int i = 0; i < ROTARION_RANGE; i++){
      if (flexible[i] == 1){
        aux = new_path[i];
        new_path[i] += (weight_smooth * (new_path[i - 1] + new_path[i + 1] - 2 * new_path[i]) + (weight_smooth / 2) * (2 * new_path[i - 1] - new_path[i - 2] - new_path[i]) + (weight_smooth / 2) * (2 * new_path[i + 1] - new_path[i + 2] - new_path[i]));
        error += abs(new_path[i] - aux);
      }
    }
  }
}

void ComputeParameter(int targetAngle, int currentAngle){
  PathInitialize();
  int scale = abs(currentAngle - targetAngle);
  for (int i = 0; i < scale; i++){
    new_path[i] = 1;
  }
  for (int i = 2; i < scale - 2; i++){
    flexible[i] = 1;
  }
  int mid_index = (int)(scale / 2);
  float mid_value = 1 - (float)mid_index * accelerate_limit / moveDelayTime;
  if (mid_value < (float)moveDelayMin / moveDelayTime){
    mid_value = (float)moveDelayMin / moveDelayTime;
  }
  new_path[mid_index] = mid_value;
  flexible[mid_index] = 0;
  Smooth;
}

void servoRun(int targetAngle, int servoNum){
  float parament;
  setTrig(HIGH);//HIGH
  myServos[servoNum].attach(servoNum + servoZeroPin,900,2100);
  // if( (targetAngle-currentAngles[servoNum] )>0){
  //   for(int k=currentAngles[servoNum]; k <= targetAngle; ){
  //     k += resolution;
  //     //k += (int)(pParament * ( targetAngle - k));
  //     myServos[servoNum].write(k);
  //     parament = ComputeParament(parament, targetAngle, k, currentAngles[servoNum]);
  //     delay((int)(parament * moveDelayTime));
  //   }
  // } else {
  //   for(int k=currentAngles[servoNum];k >= targetAngle;){
  //     k -= resolution;
  //     //k += (int)(pParament * ( targetAngle - k));
  //     myServos[servoNum].write(k);
  //     parament = ComputeParament(parament, targetAngle, k, currentAngles[servoNum]);
  //     delay((int)(parament * moveDelayTime));
  //   }
  // }
  // //myServos[servoNum].detach();
  ComputeParameter(targetAngle, currentAngles[servoNum]);
  if( (targetAngle-currentAngles[servoNum] )>0){
    for(int k=currentAngles[servoNum]; k <= targetAngle; ){
        k++;
        myServos[servoNum].write(k);
        delay((int)(moveDelayTime * new_path[k - 1 - currentAngles[servoNum]]));
    }
  } else{
    for(int k=currentAngles[servoNum]; k >= targetAngle; ){
        k--;
        myServos[servoNum].write(k);
        delay((int)(moveDelayTime * new_path[currentAngles[servoNum] - k + 1]));
    }
  }

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

