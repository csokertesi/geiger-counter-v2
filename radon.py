import RPi.GPIO as GPIO
import time
import os
from datetime import datetime as dt
from datetime import timedelta
from I2C_LCD_driver import *
import subprocess
import threading

l = lcd()

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)

alphabet = "abcdefghijklmnopqrstuvwxyz"
measurement_id = ""
for c in alphabet:
    if not os.path.isfile("mes-" + c + ".csv"):
        measurement_id = c
        break

count_14 = 0
count_15 = 0

measurement_time = 0
mes_period = 60
alert_value = 0.3

def alert():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    for i in range(50):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(0.1)

def beep_14(channel):
    global count_14
    count_14 += 1

def beep_15(channel):
    global count_15
    count_15 += 1

GPIO.add_event_detect(14, GPIO.RISING, callback=beep_14, bouncetime=200)
GPIO.add_event_detect(15, GPIO.RISING, callback=beep_15, bouncetime=200)

l.lcd_display_string(f"M:{measurement_id} P:{mes_period} E:{measurement_time}xP", 1)
l.lcd_display_string(f"K:.... B:....", 2)

try:
    while True:
        #now = dt.now()
        #next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)

        time.sleep(mes_period)
        measurement_time += mes_period

        count_14 /= mes_period
        count_15 /= mes_period

        with open("mes-" + measurement_id + ".csv", "a") as f:
            f.write(f"{measurement_time},{count_14},{count_15}\n")
            print(f"{measurement_time},{count_14},{count_15}")
            l.lcd_clear()

        if measurement_time // mes_period % 2 == 1:
            l.lcd_display_string(f"M:{measurement_id} P:{mes_period} E:{measurement_time//mes_period}xP", 1)
            l.lcd_display_string(f"K:{count_14:.2f} B:{count_15:.2f}", 2)
        else:
            cpu_temp_degC = subprocess.check_output("vcgencmd measure_temp", shell=True)
            cpu_temp_degC = cpu_temp_degC.decode("utf-8")
            cpu_temp_degC = cpu_temp_degC[5:9]

            device_ip = subprocess.check_output("hostname -I", shell=True)
            device_ip = device_ip.decode("utf-8")
            device_ip = device_ip[:13]

            l.lcd_display_string(f"{cpu_temp_degC} C", 1)
            l.lcd_display_string(f"{device_ip}", 2)

        if count_15 >= alert_value:
            t = threading.Thread(target=alert)
            t.start()

        count_14 = 0
        count_15 = 0

except KeyboardInterrupt:
    print("Stop")
finally:
    GPIO.cleanup()
