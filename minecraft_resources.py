import cv2
from cvzone.SerialModule import SerialObject
from time import sleep

arduino = SerialObject("COM3") # Change the port accordingly

imgledon = cv2.imread()

while True:
    arduino.sendData([1]) # Send 1 to Arduino
    print("Sent 1")
    sleep(2)
    
    arduino.sendData([0]) # Send 0 to Arduino
    print("Sent 0")
    sleep(1)
    