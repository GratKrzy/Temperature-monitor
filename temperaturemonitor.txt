#include <PCF8563.h>
#include <SPI.h>
#include <SD.h>
#include "dht.h"
#include <math.h>

dht DHT22;

float temperatureCalculation(int reading){
  const int beta = 3950;
  const float temperature0 = 298;
  const float resistance0 = 10000;
  const float resistance2 = 10000;
  float resistance;
  if(reading == 0){
    resistance = 2000000;
  } else {
    resistance = resistance2*(1023.0/reading - 1);
  }
  if (resistance < 10){
    resistance = 10;
  }
  float temperature;
  temperature = temperature0 * beta / (beta + temperature0 * log(resistance/resistance0));
  temperature = temperature - 273;
  return temperature;
}

float photoresistorCalculation(int reading){
  const float resistance2 = 5000;
  float resistance;
  if(reading == 0){
    resistance = 2000000;
  } else {
    resistance = resistance2*(1023.0/reading - 1);
  }
  return resistance;
}

void setNextAlarm(){
  UBYTE timebuffer[10];
  PCF8563_Get_Time(timebuffer);
  int alarmMinutes = (int)timebuffer[1];
  int alarmHours = (int)timebuffer[2];
  if (alarmMinutes < 30){
    alarmMinutes = 30;
  } else {
    alarmMinutes = 0;
    alarmHours ++;
    if (alarmHours>23){
      alarmHours = 0;
    }
  }
  Serial.println(alarmHours);
  Serial.println(alarmMinutes);
  
  PCF8563_Set_Alarm(alarmHours,alarmMinutes);
}

void setup() {

  Serial.begin(115200);
  PCF8563_Init();

  DHT22.read(3);
  pinMode(4,OUTPUT);

  while(!SD.begin(10)){
    Serial.println("SD error!");
    digitalWrite(4,HIGH);
    delay(1000);
  }
  digitalWrite(4,LOW);

  PCF8563_Alarm_Enable();
  setNextAlarm();

}



void loop() {

  int flag = PCF8563_Get_Flag();
  if(flag==1||flag == 3){
    PCF8563_Cleare_AF_Flag();

    UBYTE timebuffer[10];
    PCF8563_Get_Time(timebuffer);
    PCF8563_Get_Days(&timebuffer[3]);

    int photoresistor = analogRead(A0);
    int thermistor1 = analogRead(A1);
    int thermistor2 = analogRead(A2);
    int thermistor3 = analogRead(A3);
    int window = digitalRead(2);

    while(!SD.begin(10)){
      Serial.println("SD error!");
      digitalWrite(4,HIGH);
      delay(1000);
    }
    digitalWrite(4,LOW);

    File dataFile = SD.open("Datalog.txt", FILE_WRITE);
    
    if (dataFile){
      dataFile.print(timebuffer[3]);
      dataFile.print("-");
      dataFile.print(timebuffer[4]);
      dataFile.print("-");
      dataFile.print(timebuffer[6]);
      dataFile.print(timebuffer[5]);
      dataFile.print(" ");
      dataFile.print(timebuffer[2]);
      dataFile.print(":");
      dataFile.print(timebuffer[1]);
      dataFile.print(";");

      dataFile.print((float)DHT22.humidity, 2);
      dataFile.print(";");
      dataFile.print((float)DHT22.temperature, 2);
      dataFile.print(";");

      dataFile.print(photoresistor);
      dataFile.print(";");
      dataFile.print(photoresistorCalculation(photoresistor));
      dataFile.print(";");

      dataFile.print(thermistor1);
      dataFile.print(";");
      dataFile.print(temperatureCalculation(thermistor1));
      dataFile.print(";");

      dataFile.print(thermistor2);
      dataFile.print(";");
      dataFile.print(temperatureCalculation(thermistor2));
      dataFile.print(";");

      dataFile.print(thermistor3);
      dataFile.print(";");
      dataFile.print(temperatureCalculation(thermistor3));
      dataFile.print(";");

      if (window == 0) {
        dataFile.print("open");
      } else {
        dataFile.print("closed");
      }

      dataFile.print("\n");
      dataFile.close();
      Serial.println("File save success");
    } else{
      Serial.println("File save error!");
    }

    setNextAlarm();
  }
  delay(60000);
}
