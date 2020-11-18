# this code demonstrates how system work together
# and implement a typical pandemic flow where
#
# 1) detect qr code ->
# 2) scan temperature ->
# 3) display on lcd ->
# 4) upload identity and temperature to cloud
#
# WIP, currently implemented 1-3

import board
import busio as io
import adafruit_mlx90614
import smbus
import time
import cv2

# set up camera object
cap = cv2.VideoCapture(0)

# the mlx90614 must be run at 100k [normal speed]
# i2c default mode is is 400k [full speed]
# the mlx90614 will not appear at the default 400k speed
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

# temperature results in celsius
#print("Ambent Temp: ", mlx.ambient_temperature)
#print("Object Temp: ", mlx.object_temperature)


# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(0) # Rev 2 Pi uses 1

def lcd_init():
    # Initialise display
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
    lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
    time.sleep(E_DELAY)

def lcd_string(message,line):
    # Send string to display

    message = message.ljust(LCD_WIDTH," ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

def main():

    # Initialise display
    lcd_init()

    #Initial state
    qr_done = 0
    data = ''
    previousdata = 'a'

    while True:

        # First, sample QR code, if there is QR code containing valid user info
        # then proceed to next step of temperature measurement

        lcd_string("",  LCD_LINE_1)
        lcd_string("Welcome, please ",  LCD_LINE_2)
        lcd_string("scan the QR code",  LCD_LINE_3)
        lcd_string("",  LCD_LINE_4)

        # QR code detection object
        detector = cv2.QRCodeDetector()

        if qr_done == 0:
            print(".")
            print("data: ", data, ". previous data: ", previousdata)
            while previousdata != data:
                # get the image
                _, img = cap.read()
                # get bounding box coords and data
                data, bbox, _ = detector.detectAndDecode(img)
                
                # if there is a bounding box, draw one, along with the data
                """if(bbox is not None):
                    for i in range(len(bbox)):
                        cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                                 0, 255), thickness=2)
                    cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 2)"""
                if data:
                    qr_done = 1
                    userdata = data
                    print("data found: ", data, "qr_done: ", qr_done)
                    previousdata = data
                    break
                # display the image preview
                #cv2.imshow("code detector", img)
                #if(cv2.waitKey(1) == ord("q")):
                #    break

        # Received valid QR code, sense temperature, and then clear data.
        else:
            print(",")
            # This is the lowest human body temperature possible.
            # you are nearly dead if below 34.
            while (round(mlx.object_temperature, 2) < 34):
                temp_string = str(round(mlx.object_temperature, 2))
                # Print temperature text
                lcd_string("Wait for a valid",  LCD_LINE_1)
                lcd_string("body temperature",  LCD_LINE_2)
                lcd_string("                ",  LCD_LINE_3)
                lcd_string("Current: " + temp_string + "C",LCD_LINE_4)
                print(temp_string)
                time.sleep(3)

            temp_string = str(round(mlx.object_temperature, 2))
            lcd_string("hi ",                   LCD_LINE_1)
            lcd_string(userdata,                LCD_LINE_2)
            lcd_string("Body temperature:",     LCD_LINE_3)
            lcd_string(temp_string + " Celsius",LCD_LINE_4)
            time.sleep(3)
            
            #clear previous data
            qr_done = 0
            data = ''
            userdata = ''

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        # free camera object and exit
        cv2.destroyAllWindows()
        cap.release()


