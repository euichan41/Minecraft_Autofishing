import interception
import numpy as np
import time
import threading


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

# 스레드 생성 및 실행
right_thread = threading.Thread(target=key_keydown("right", 3))
c_thread = threading.Thread(target=key_press("c"))

right_thread.start()

c_thread.start()

# 스레드가 실행을 마칠 때까지 대기
right_thread.join()
c_thread.join()

"""
for i in range (0,3):
    interception.inputs.press("c", 3, 0.5)
    interception.key_down("x", 2)
    interception.key_up("x", 1)
"""
    #interception.KEY_PRESS_DELAY = 0.1
    #interception.key_down("b", 1)c
    #print(interception.KeyState.KEY_DOWN)

# interception.auto_capture_devices(keyboard=True, mouse=True, verbose=True) # 자동으로 장치를 캡처

# interception.inputs.press("a", 3, 0.5) # a를 0.5초 간격으로 3번 누르기
# interception.key_down("b", 1) 