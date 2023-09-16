import serial
import time
import sys
import csv

# 아두이노와의 시리얼 통신을 위한 포트 설정
arduino_port = "COM4"  # 포트는 해당 환경에 맞게 변경

# 시리얼 통신 시작
ser = serial.Serial(arduino_port, 9600, timeout=1)
time.sleep(2)  # 아두이노가 초기화되는 동안 대기
integer_list_1 = [0,0,0,0]
integer_list_2 = [1,0,0,0]
integer_list_3 = [0,1,0,0]
integer_list_4 = [0,0,1,0]
integer_list_5 = [0,0,0,1]
integer_list_6 = [0,1,1,0]
integer_list_7 = [0,1,0,1]

integer_list = [integer_list_1, integer_list_2, integer_list_3, integer_list_4, integer_list_5, integer_list_6, integer_list_7]
command_list = [1,2,3,4,5,6,7]



try:
    while True:
        command = sys.stdin.readline().strip()
        command = int(command)
        #command = list(map(int, sys.stdin.readline().rstrip().split())) # 명령 입력, 공백 기준으로 분리된 정수를 리스트로 저장
        if command in command_list:
            selected_integer_list = integer_list[command - 1]
            data_csv = ','.join(map(str, selected_integer_list)) + '\n'
            ser.write(data_csv.encode())  # 아두이노로 명령 전송
        elif command == 'q':
            break
        else:
            print("Invalid command...")
except KeyboardInterrupt:
    pass

# 시리얼 통신 종료
ser.close()