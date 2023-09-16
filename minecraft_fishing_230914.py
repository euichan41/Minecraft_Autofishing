import minecraft_screenCapture as window
import cv2
import time
#import win32gui
import interception
import numpy as np
import threading
import random

# 기본 설정
ESC_KEY = 27
FRAME_RATE = 144
SLEEP_TIME = 1 / FRAME_RATE
waitkey = 0


# 초기 상태 전역변수 설정
keystate = {"right": False, "left": False, "up": False, "down": False} # 키보드 상태 딕셔너리
x_coordinate_current_player = 0
y_coordinate_current_player = 0
x_coordinate_current_rune = 0
y_coordinate_current_rune = 0
last_time_rune = 0

# 키보드 장치 번호
#interception.auto_capture_devices(keyboard=True, mouse=True, verbose=True)
interception_instance = interception.Interception()
interception.set_devices(2, 10)
print("Keyboard device set to:", interception.get_keyboard())
print("Mouse device set to:", interception.get_mouse())


# 미니맵 좌표 상수
Minimap_w1 = 7
Minimap_h1 = 59

Minimap_w2 = 169
Minimap_h2 = 135


# 전역 변수로 current_position과 락을 선언
current_position = None
program_is_running = True
position_lock = threading.Lock()



# 텍스트 설정
text_MinimapPlayer = "Minimap_Player"
text_MinimapRune = "Minimap_Rune"

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
font_thickness = 1


# 윈도우 캡쳐 객체 생성
capture = window.WindowCapture("MapleStory", FRAME_RATE)


# 이미지 템플릿 로드
templit_MinimapPlayer = cv2.imread("resources_img/Player.bmp", cv2.IMREAD_UNCHANGED) #이미지를 불러옴
templit_MinimapRune = cv2.imread("resources_img/Rune.bmp", cv2.IMREAD_GRAYSCALE) #이미지를 불러옴


def generate_normal_distribution(mean, std_dev):
    # 평균(mean)과 표준편차(std_dev)를 사용하여 정규 분포 생성
    normal_values = np.random.normal(mean, std_dev, 1)  # 1개의 랜덤 값 생성 (원하는 개수로 조절 가능)
    
    # 값 범위를 50에서 150 사이로 제한
    normal_values = np.clip(normal_values, mean // 1.25, mean * 1.25)
    
    # 값을 1000으로 나눔
    normal_values = normal_values / 1000
    
    # 소숫점 셋째자리까지 표기
    normal_values = np.round(normal_values, 3)
    
    return normal_values[0]


# 키 입력 함수
#def key_press(key):
#    key_delay = generate_normal_distribution(92,17)
#    interception.key_down(key, key_delay) # 92ms의 평균과 17ms의 표준편차를 가진 정규분포로 랜덤한 입력시간 동안 키를 누름
#    interception.key_up(key) # 키를 뗌
#    print(f"key {key} pressed:", key_delay)

#def key_keydown(key, keydown_time):
#    interception.key_down(key, keydown_time) # keydown_time동안 키를 눌렀다 뗌
#    interception.key_up(key)


# 키 입력 함수
def key_press():
    global current_time, last_time_rune
    global current_position
    global program_is_running
    global x_coordinate_current_player, y_coordinate_current_player
    global x_coordinate_current_rune, y_coordinate_current_rune
    global keystate
    while program_is_running:
        with position_lock:
            #if last_time_rune < (current_time - 900) and x_coordinate_current_rune != 0 and y_coordinate_current_rune != 0:
            #    x_coordinate_error = x_coordinate_current_rune - x_coordinate_current_player
            #    y_coordinate_error = y_coordinate_current_rune - y_coordinate_current_player
            #    if x_coordinate_error < 0:
            if current_position == 0:
                key_keydown("right")
                if y_coordinate_current_player == 0:
                    if x_coordinate_current_player >= 100:
                        if x_coordinate_current_player >= 117:
                            if x_coordinate_current_player >= 142:
                                key_keyup("right")
                                key_keydown("down")
                                time.sleep(generate_normal_distribution(880,40))
                                key_keyup("down")
                            else:
                                key_keyup("right")
                                key_keypress("shift", 245)
                                time.sleep(generate_normal_distribution(500,40)) # Position 0: x좌표 117 이상이면 shift 누르기
                        else:
                            key_keypress("c", 85)
                            time.sleep(generate_normal_distribution(45,5))
                            key_keypress("x", 105)
                            time.sleep(generate_normal_distribution(500,40))
                    else:
                        key_keypress("c", 53)
                        time.sleep(generate_normal_distribution(45,5))
                        key_keypress("c", 45)
                        time.sleep(generate_normal_distribution(44,3))
                        key_keypress("x", 105)
                        time.sleep(generate_normal_distribution(200,40)) # Position 0: 더블점프 후 퀀터
                elif x_coordinate_current_player == 24 and 1 <= y_coordinate_current_player <= 12:
                    key_keydown("right")
                    time.sleep(generate_normal_distribution(40,5))
                    key_keypress("c", 65)
                    time.sleep(generate_normal_distribution(48,5))
                    if random.random() < 0.5:
                        key_keypress("x", 95)
                    else:
                        key_keypress("z", 205) # 50% 확률로 x 또는 z키 누르기
                    time.sleep(generate_normal_distribution(300,40)) # Position 1: 줄1에 매달렸을 때 우점프
                    key_keyup("right")
                elif x_coordinate_current_player == 67 and 1<= y_coordinate_current_player <= 12:
                    key_keydown("right")
                    time.sleep(generate_normal_distribution(42,5))
                    key_keypress("c", 65)
                    time.sleep(generate_normal_distribution(46,5))
                    if random.random() < 0.5:
                        key_keypress("x", 90)
                    else:
                        key_keypress("z", 205) # 50% 확률로 x 또는 z키 누르기
                    time.sleep(generate_normal_distribution(290,40)) # Position 1: 줄2에 매달렸을 때 우점프
                    key_keyup("right")
                else:
                    time.sleep(0.05)
            elif current_position == 1:
                time.sleep(0.1)
                key_keyup("left")
                key_keyup("right")
                key_keypress("right", 80)
                if y_coordinate_current_player == 13:
                    key_keydown("down")
                    time.sleep(generate_normal_distribution(50,10))
                    key_keypress("c", 86)
                    time.sleep(generate_normal_distribution(51,4))
                    key_keypress("x", 102)
                    time.sleep(generate_normal_distribution(100,17))
                    key_keyup("down")
                    time.sleep(generate_normal_distribution(110,15))
            elif current_position == 2:
                time.sleep(0.1)
                key_keyup("left")
                key_keyup("right")
                time.sleep(0.1)
                key_keypress("right", 88)
                if y_coordinate_current_player == 13:
                    key_keydown("down")
                    time.sleep(generate_normal_distribution(48,12))
                    key_keypress("c", 90)
                    time.sleep(generate_normal_distribution(51,4))
                    if random.random() < 0.38:
                        key_keypress("x", 96)
                    else:
                        key_keypress("z", 187) # 50% 확률로 x 또는 z키 누르기
                    time.sleep(generate_normal_distribution(110,5))
                    key_keyup("down")
                    time.sleep(generate_normal_distribution(115,19))
            elif current_position == 3:
                time.sleep(0.1)
                key_keyup("left")
                key_keyup("right")
                if y_coordinate_current_player == 13:
                    key_keydown("down")
                    time.sleep(generate_normal_distribution(49,13))
                    key_keypress("c", 90)
                    time.sleep(generate_normal_distribution(44,5))
                    if random.random() < 0.35:
                        key_keypress("x", 82)
                    else:
                        key_keypress("z", 174) # 50% 확률로 x 또는 z키 누르기
                    time.sleep(generate_normal_distribution(105,8))
                    key_keyup("down")
                    time.sleep(generate_normal_distribution(113,12))
            elif current_position == 4 or current_position == 5 or current_position == 6:
                key_keydown("left")
                if y_coordinate_current_player == 26:
                    if x_coordinate_current_player <= 44:
                        if x_coordinate_current_player <= 32:
                            key_keyup("left")
                            time.sleep(generate_normal_distribution(42,3))
                            key_keydown("down")
                            time.sleep(generate_normal_distribution(49,13))
                            key_keypress("c", 90)
                            time.sleep(generate_normal_distribution(44,5))
                            key_keypress("x", 85)
                            time.sleep(generate_normal_distribution(105,8))
                            key_keyup("down")
                            time.sleep(generate_normal_distribution(113,12))
                        else:
                            key_keypress("c", 85)
                            time.sleep(generate_normal_distribution(30,12))
                            key_keypress("x", 105)
                            time.sleep(generate_normal_distribution(500,40))
                    else:
                        key_keypress("c", 53)
                        time.sleep(generate_normal_distribution(44, 5))
                        key_keypress("c", 51)
                        time.sleep(generate_normal_distribution(42,6))
                        key_keypress("x", 105)
                        time.sleep(generate_normal_distribution(190,20))
                else:
                    time.sleep(0.05)
            else:
                key_keyup("right")
                key_keyup("left")
                time.sleep(0.1)
        time.sleep(SLEEP_TIME)


def key_keypress(key,delay):
    std_dev = random.randint(8,12)
    key_delay = generate_normal_distribution(delay,std_dev)
    interception.key_down(key, key_delay) 
    interception.key_up(key)

def key_keydown(key):
    global keystate
    if key in keystate and keystate[key] == False:
        keycode = interception.KEYBOARD_MAPPING[key]
        keystroke = interception.KeyStroke(keycode, interception.KeyState.KEY_DOWN, 0)
        interception_instance.send_key(stroke=keystroke)
        keystate[key] = True
    else:
        pass

def key_keyup(key):
    global keystate
    if key in keystate and keystate[key] == True:
        keycode = interception.KEYBOARD_MAPPING[key]
        keystroke = interception.KeyStroke(keycode, interception.KeyState.KEY_UP, 0)
        interception_instance.send_key(stroke=keystroke)
        keystate[key] = False
    else:
        pass


# 미니맵 이미지 매칭 함수
def findImage_Minimap(frame_Minimap, frame, templit):
    # 이미지 매칭 수행 (Minimap_Character)
    result = cv2.matchTemplate(frame_Minimap, templit, cv2.TM_SQDIFF_NORMED)
    
    # 매칭 결과에서 가장 좋은 매칭값과 좌표 구하기
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    x, y = minLoc
    h, w = templit.shape[:2]
    
    # 매칭이 될 경우에만 실행
    if minVal < 0.3:
        # 매칭된 영역을 사각형으로 표시
        x, y = x + Minimap_w1, y + Minimap_h1
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        
        # 매칭된 영역에 텍스트 표시
        text_x = x + w
        text_y = y + h + 15
        x_coordinate_current = x - 10
        y_coordinate_current = -y + 111
        #cv2.putText(frame, f"{text} (x:{x_coordinate_current}, y:{y_coordinate_current})", (text_x, text_y), font, font_scale, (0, 0, 255), font_thickness)
        return text_x, text_y, x_coordinate_current, y_coordinate_current
    else:
        return None, None, None, None



def main_loop():
    global program_is_running
    global current_time
    global current_position
    global x_coordinate_current_player, y_coordinate_current_player
    global x_coordinate_current_rune, y_coordinate_current_rune
    start_time = time.time()
    
    while True:
        loop_start_time = time.time()
        frame = capture.screenshot()
        frame_Minimap = frame[Minimap_h1:Minimap_h2, Minimap_w1:Minimap_w2] #미니맵 영역만 가져옴
        frame_Minimap_gray = cv2.cvtColor(frame_Minimap, cv2.COLOR_BGR2GRAY) #미니맵 영역을 그레이스케일로 변환
        
        # 이미지 매칭 수행 (Minimap_Character)
        text_x_player, text_y_player, x_coordinate_current_player, y_coordinate_current_player = findImage_Minimap(frame_Minimap, frame, templit_MinimapPlayer)
        cv2.putText(frame, f"{text_MinimapPlayer} (x:{x_coordinate_current_player}, y:{y_coordinate_current_player})", (text_x_player, text_y_player), font, font_scale, (0, 255, 0), font_thickness)
        
        # 룬이 미니맵에 있을 경우 이미지 매칭 수행 (Minimap_Rune)
        text_x_rune, text_y_rune, x_coordinate_current_rune, y_coordinate_current_rune = findImage_Minimap(frame_Minimap_gray, frame, templit_MinimapRune)
        if x_coordinate_current_rune != None and y_coordinate_current_rune != None and x_coordinate_current_player != None and y_coordinate_current_player != None:
            cv2.putText(frame, f"{text_MinimapRune} (x:{x_coordinate_current_rune}, y:{y_coordinate_current_rune})", (text_x_rune, text_y_rune), font, font_scale, (0, 255, 255), font_thickness)
        else:
            pass
        
        # 현재 캐릭터의 위치를 파악
        if x_coordinate_current_player != None and y_coordinate_current_player != None:
            current_position = 8
            if 0 <= y_coordinate_current_player < 13:
                current_position = 0
            elif 13 <= y_coordinate_current_player < 26:
                if 10 <= x_coordinate_current_player <= 35:
                    current_position = 1
                elif 41 <= x_coordinate_current_player <= 93:
                    current_position = 2
                elif 100 <= x_coordinate_current_player <= 138:
                    current_position = 3
                else:
                    current_position = 8
            elif 26 <= y_coordinate_current_player < 39:
                if 0 <= x_coordinate_current_player <= 43:
                    current_position = 4
                elif 43 <= x_coordinate_current_player <= 90:
                    current_position = 5
                elif 90 <= x_coordinate_current_player <= 148:
                    current_position = 6
                else:
                    current_position = 8
                #if 5 <= x_coordinate_current_player <= 43:
                #    current_position = 4
                #elif 51 <= x_coordinate_current_player <= 82:
                #    current_position = 5
                #elif 90 <= x_coordinate_current_player <= 142:
                #    current_position = 6
                #else:
                #    current_position = 8
            elif 39 <= y_coordinate_current_player < 52:
                if 19 <= x_coordinate_current_player <= 71:
                    current_position = 7
                else:
                    current_position = 8
            else:
                current_position = 8
            
            cv2.putText(frame, f"Current Section: [{current_position}]", (10, 200), font, font_scale, (0, 255, 255), font_thickness)
        
        
        # 창에 시간 출력
        current_time = time.time() - start_time
        cv2.putText(frame, f"Current Time: {current_time:.2f}", (10, 220), font, font_scale, (255, 255, 255), font_thickness)
        
        
        # 창에 이미지 출력
        cv2.imshow("frame_window_Netflix", frame)
        
        delta = time.time() - loop_start_time
        if delta < SLEEP_TIME:
            time.sleep(SLEEP_TIME - delta)
        waitkey = cv2.waitKey(1) & 0xFF
        if waitkey == ESC_KEY:
            with position_lock:
                program_is_running = False
            break
        
    cv2.destroyAllWindows()









if __name__ == "__main__":
    print("minecraft_fishing.py executed as main file!!!")
    
    key_press_thread = threading.Thread(target=key_press)
    key_press_thread.start()
    
    main_loop()
    key_press_thread.join()  # main_loop가 종료되면 key_press 스레드가 종료될 때까지 기다림
    
    print("minecraft_fishing.py quit!!!")