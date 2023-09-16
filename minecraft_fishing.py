import minecraft_screenCapture as window
import cv2
import time
#import win32gui
import interception
import numpy as np

# 기본 설정
ESC_KEY = 27
FRAME_RATE = 144
SLEEP_TIME = 1 / FRAME_RATE


# 키보드 마우스 장치 번호
#interception.auto_capture_devices(keyboard=True, mouse=True, verbose=True)
interception.set_devices(2, 10)
print("Keyboard device set to:", interception.get_keyboard())
print("Mouse device set to:", interception.get_mouse())


# 미니맵 좌표 상수
Minimap_w1 = 7
Minimap_h1 = 59

Minimap_w2 = 169
Minimap_h2 = 135

x_coordinate_target = 60
y_coordinate_target = 13

current_position = 8


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
    normal_values = np.clip(normal_values, 49, 137)
    
    # 값을 1000으로 나눔
    normal_values = normal_values / 1000
    
    # 소숫점 셋째자리까지 표기
    normal_values = np.round(normal_values, 3)
    
    return normal_values[0]


# 키 입력 함수
def key_press(key):
    key_delay = generate_normal_distribution(92,17)
    interception.key_down(key, key_delay) # 92ms의 평균과 17ms의 표준편차를 가진 정규분포로 랜덤한 입력시간 동안 키를 누름
    interception.key_up(key) # 키를 뗌
    print(f"key {key} pressed:", key_delay)

def key_keydown(key, keydown_time):
    interception.key_down(key, keydown_time) # keydown_time동안 키를 눌렀다 뗌
    interception.key_up(key)


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
    start_time = time.time()
    
    while True:
        loop_start_time = time.time()
        frame = capture.screenshot()
        #frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 화면을 그레이스케일로 변환
        frame_Minimap = frame[Minimap_h1:Minimap_h2, Minimap_w1:Minimap_w2] #미니맵 영역만 가져옴
        frame_Minimap_gray = cv2.cvtColor(frame_Minimap, cv2.COLOR_BGR2GRAY) #미니맵 영역을 그레이스케일로 변환
        
        # 이미지 매칭 수행 (Minimap_Character)
        text_x_player, text_y_player, x_coordinate_current_player, y_coordinate_current_player = findImage_Minimap(frame_Minimap, frame, templit_MinimapPlayer)
        cv2.putText(frame, f"{text_MinimapPlayer} (x:{x_coordinate_current_player}, y:{y_coordinate_current_player})", (text_x_player, text_y_player), font, font_scale, (0, 255, 0), font_thickness)
        
        # 룬이 미니맵에 있을 경우 이미지 매칭 수행 (Minimap_Rune)
        text_x_rune, text_y_rune, x_coordinate_current_rune, y_coordinate_current_rune = findImage_Minimap(frame_Minimap_gray, frame, templit_MinimapRune)
        if x_coordinate_current_rune != None and y_coordinate_current_rune != None and x_coordinate_current_player != None and y_coordinate_current_player != None:
            cv2.putText(frame, f"{text_MinimapRune} (x:{x_coordinate_current_rune}, y:{y_coordinate_current_rune})", (text_x_rune, text_y_rune), font, font_scale, (0, 255, 255), font_thickness)
            x_coordinate_target, y_coordinate_target = x_coordinate_current_rune, y_coordinate_current_rune
            x_coordinate_error = x_coordinate_target - x_coordinate_current_player
            y_coordinate_error = y_coordinate_target - y_coordinate_current_player
            
            if x_coordinate_error > 5:
                text_playerAction_x = "Move Right"
            elif x_coordinate_error < -5:
                text_playerAction_x = "Move Left"
            else:
                text_playerAction_x = "X Stop"
                
            if y_coordinate_error > 2:
                text_playerAction_y = "Move Up"
            elif y_coordinate_error < -2:
                text_playerAction_y = "Move Down"
            else:
                text_playerAction_y = "Y Stop"
            cv2.putText(frame, f"{text_playerAction_x}, {text_playerAction_y} (x:{x_coordinate_error}, y:{y_coordinate_error})", (text_x_player, text_y_player + 10), font, font_scale, (0, 128, 255), font_thickness)
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
                    currenet_position = 2
                elif 100 <= x_coordinate_current_player <= 138:
                    current_position = 3
                else:
                    current_position = 8
            elif 26 <= y_coordinate_current_player < 39:
                if 5 <= x_coordinate_current_player <= 43:
                    current_position = 4
                elif 51 <= x_coordinate_current_player <= 82:
                    current_position = 5
                elif 90 <= x_coordinate_current_player <= 142:
                    current_position = 6
                else:
                    current_position = 8
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
            break
        
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("minecraft_fishing.py executed as main file!!!")
    main_loop()
    print("minecraft_fishing.py quit!!!")