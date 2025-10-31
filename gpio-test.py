from gpiozero import LED
from time import sleep

red = LED(23)

while True:
    print("On")
    red.on()
    sleep(5)
    print("Off")
    red.off()
    sleep(5)
   


