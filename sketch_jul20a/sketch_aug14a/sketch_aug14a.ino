
const int solenoidPinZ = 4; // 솔레노이드 제어를 위한 디지털 핀 번호
const int solenoidPinC = 5;
const int solenoidPinLeft = 6;
const int solenoidPinRight = 7;

int receivedNumber; //파이썬에서 받은 4자리 정수
int command_1, command_2, command_3, command_4;

void setup() {
  pinMode(solenoidPinZ, OUTPUT); // 솔레노이드 핀을 출력으로 설정
  pinMode(solenoidPinC, OUTPUT);
  pinMode(solenoidPinLeft, OUTPUT);
  pinMode(solenoidPinRight, OUTPUT);
  
  digitalWrite(solenoidPinZ, HIGH); // 솔레노이드 초기 상태를 끄기로 설정
  digitalWrite(solenoidPinC, HIGH);
  digitalWrite(solenoidPinLeft, HIGH);
  digitalWrite(solenoidPinRight, HIGH);
  
  Serial.begin(9600); // 시리얼 통신 시작
}

void loop() {
  if (Serial.available() > 0) {
    //char command = Serial.read(); // 파이썬에서 받은 문자 읽기
    String data_received = Serial.readStringUntil('\n');  // CSV 문자열 읽기
    
    int values[4];
    char *token = strtok((char *)data_received.c_str(), ",");
    int index = 0;
    while (token != NULL && index < 4) {
      values[index] = atoi(token);
      token = strtok(NULL, ",");
      index++;
    }
    
    // 코드 중복을 줄이기 위해 솔레노이드를 배열로 관리
    int solenoidPins[4] = {solenoidPinZ, solenoidPinC, solenoidPinLeft, solenoidPinRight};
    int commands[4] = {command_1, command_2, command_3, command_4};

    for (int i = 0; i < 4; i++) {
      if (commands[i] == 0) {
        digitalWrite(solenoidPins[i], HIGH); // 솔레노이드 끄기
      } else if (commands[i] == 1) {
        digitalWrite(solenoidPins[i], LOW); // 솔레노이드 켜기
      } else if (commands[i] == 2) {
        digitalWrite(solenoidPins[i], LOW);
        int delayTime = generateGaussianRandom(92, 15);
        delayTime = constrain(delayTime, 62, 122);
        delay(delayTime);
        digitalWrite(solenoidPins[i], HIGH);
      }
    }
  }
}

int generateGaussianRandom(int mean, int stdDev) {
  float u1 = random(0, 32767) / 32767.0; // 0~1 사이의 난수 생성
  float u2 = random(0, 32767) / 32767.0;
  
  float z = sqrt(-2 * log(u1)) * cos(2 * PI * u2);
  
  return int(mean + stdDev * z);
}
