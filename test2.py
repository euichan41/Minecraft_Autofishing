import threading
import time
import interception
import numpy as np

# 상수
current_position = 0

interception_instance = interception.Interception()


# 키보드 장치 번호
#interception.auto_capture_devices(keyboard=True, mouse=True, verbose=True)
interception.set_devices(2, 10)
print("Keyboard device set to:", interception.get_keyboard())
print("Mouse device set to:", interception.get_mouse())

# 정규분포 생성 함수
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
    interception.key_down(key, keydown_time)
    interception.key_up(key)


def action_1():
    interception.Interception.send_key("right")

def action_2():
    keycode = interception.KEYBOARD_MAPPING["right"]
    keystroke = interception.KeyStroke(keycode, interception.KeyState.KEY_DOWN, 0)
    interception_instance.send_key(stroke=keystroke)
    time.sleep(3)
    keycode = interception.KEYBOARD_MAPPING["right"]
    keystroke = interception.KeyStroke(keycode, interception.KeyState.KEY_UP, 0)
    interception_instance.send_key(stroke=keystroke)
    time.sleep(3)

def action_3(key):
    keycode = interception.KEYBOARD_MAPPING[key]
    keystroke = interception.KeyStroke(keycode, interception.KeyState.KEY_DOWN, 0)
    interception.Interception.send_key(stroke=keystroke)
    time.sleep(3)

def action_4():
    keycode = interception.KEYBOARD_MAPPING["right"]
    keystroke = interception.KeyStroke(keycode, interception.KeyState.KEY_DOWN, 0)
    states = interception_instance.receive(2)
    print(states)

def action_5(): # action_2에서 업그레이드
    keycode = interception.KEYBOARD_MAPPING["right"]
    keystroke = interception.KeyStroke(keycode, interception.KeyState.KEY_DOWN, 0)
    interception_instance.send_key(stroke=keystroke)
    



def keyinput_loop():
    while True:
        if current_position == 0:
            interception.Interception.send_key()
        else:
            pass

p1=threading.Thread(target=action_2)
#p2=threading.Thread(target=keyinput_loop)


# 그러나 아래 함수 호출 순서를 바꾸지는 않았음
p1.start()

#p2.start()


