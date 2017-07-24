#include <Servo.h> //包含舵机库

Servo myservo; //创建一个舵机控制类
int pos = 0; //定义一个变量存储舵机转动角度

void setup()
{
myservo.attach(9, 900, 2100);
Serial.begin(9600);
}

void loop()
{
  for (;pos < 180; pos += 10){
    myservo.write(pos); //舵机转动到相应角度
    Serial.print(pos);
    delay(1000); //延时一段时间让舵机转动到对应位置
    
  }
  pos -= 10;
  
  for (;pos > 0; pos -= 5){
    myservo.write(pos); //舵机转动到相应角度
    Serial.print(pos);
    delay(1000); //延时一段时间让舵机转动到对应位置
  }
  pos += 5;
}

