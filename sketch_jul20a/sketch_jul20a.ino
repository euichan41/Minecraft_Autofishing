#include <cvzone.h>

SerialData serialData(1, 1); //(numOfValsRec,digitsPerValRec)
int valsRec[1]; // array of int with size numOfValsRec 

void setup() {
  pinMode(13, OUTPUT);
  serialData.begin();
}

void loop() {

  serialData.Get(valsRec);
  digitalWrite(13, valsRec[0]);
  digitalWrite(12, valsRec[1]);
  delay(10);
}
