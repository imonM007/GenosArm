#include <Servo.h>

Servo servo0;

Servo servo1;

Servo servo2;

Servo servo3;

int sensorvalue0;

int sensorvalue1;

int sensorvalue2;

int sensorvalue3;


void setup()

{

  Serial.begin(9600); 

  pinMode(A0,INPUT);

  pinMode(5,OUTPUT);

  servo0.attach(5);

  

  pinMode(A1,INPUT);

  pinMode(6,OUTPUT);

  servo1.attach(6);

  

  pinMode(A2,INPUT);

  pinMode(7,OUTPUT);

  servo2.attach(7);

  

  pinMode(A3,INPUT);

  pinMode(8,OUTPUT);

  servo3.attach(8);

}


void loop()

{

  sensorvalue0 = analogRead(A0);

  sensorvalue0 = map(sensorvalue0, 0, 1023, 0, 120);  // left servo

  servo0.write(sensorvalue0);

 // Serial.println (sensorvalue0);

  

  sensorvalue1 = analogRead(A1);

  sensorvalue1 = map(sensorvalue1, 0, 1023, 70, 150);  // right servo

  servo1.write(sensorvalue1);

 //  Serial.println (sensorvalue1);


  sensorvalue2 = analogRead(A2);

  sensorvalue2 = map(sensorvalue2, 0, 1023, 20, 160); // center servo

  servo2.write(sensorvalue2);

  //Serial.println (sensorvalue2);


  sensorvalue3 = analogRead(A3);

  sensorvalue3 = map(sensorvalue3, 0, 1023, 130, 145);  // jaw servo

  servo3.write(sensorvalue3);

//  Serial.println (sensorvalue3);

 

}