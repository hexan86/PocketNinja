"""
Display TFT Bonnet Adafruit 1.3"
Put in /home/"user"/boot/ and change paths
Add BOOT Image in the same folder or adjust the path
Use /etc/rc.local to call a bash script that executes this Python code
(The reason is to facilitate singular modifications)

This code starts after boot, displays the DEFCON logo and then goes to the command interface

The Joystick alone:
UP = Airdump-NG WEP
LEFT = Airodump-NG ALL
RIGHT = MAC Changer
DOWN = Proxmark3 "auto" scan
CENTER = Airo-Kill/Screen Alive

A + Joystick
UP = Bettercap 0/24
LEFT = Nmap 0/24
RIGHT = Nmap 1/24
DOWN = Bettercap 1/24
CENTER = Screen-Kill

B + Joystick
UP = Upload
LEFT = Reboot
RIGHT = Reset
DOWN = Shutdown
"""


#IMPORT

import os
import time
import random
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import digitalio
from digitalio import DigitalInOut, Direction
import board
import adafruit_rgb_display.st7789 as st7789
# pylint: disable=unused-import


# CONFIGURATION

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000
# Setup SPI bus using hardware SPI:
spi = board.SPI()


# CREATE DISPLAY

# pylint: disable=line-too-long
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
# pylint: enable=line-too-long



# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT


# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True


def clearscreen():
    width = disp.width
    height = disp.height
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 255, 0))
    disp.image(image)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

def tftcontrol():
    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for color.
    width = disp.width
    height = disp.height
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Clear display.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 255))
    disp.image(image)

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    udlr_fill = "#00FF00"
    udlr_outline = "#00FFFF"
    button_fill = "#FF00FF"
    button_outline = "#FFFFFF"

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font_size = 13
    font2_sze = 30
    fnt = ImageFont.truetype(font_path, font_size)
    fnt2 = ImageFont.truetype(font_path, font2_sze)


    # Try to call bash scripts, coded as scripts that pass commands to screen sessions

    def up():  # UP Pressed
        up_fill = udlr_fill
        os.system("sudo /home/kali/boot/scrnup.sh") # Call bash script Screen, to call bash script commands.sh, to execute airodump for WEP recording + variable time/date
        clearscreen()
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/aimg.jpg")
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        tftcontrol()

    def left():  # LEFT Pressed
        left_fill = udlr_fill
        os.system("sudo /home/kali/boot/scrnleft.sh") # Call bash script for NET recording + variable time/date
        clearscreen()
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/aimg.jpg")
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        tftcontrol()

    def right():  # RIGHT Pressed
        right_fill = udlr_fill
        os.system("sudo /home/kali/boot/imgs/right.sh")
        clearscreen()
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/right.jpg")
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        tftcontrol()

    def down():  # DOWN Pressed
        down_fill = udlr_fill
        clearscreen()
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(50, 50, 50))
        disp.image(image)
        image = Image.open("/home/kali/boot/imgs/down.jpg")
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        os.system("sudo /home/kali/boot/down.sh")

        tftcontrol()

    def center(): # CENTER Pressed
        center_fill = button_fill
        os.system("sudo /home/kali/boot/center.sh")

    def aempty(): # A Pressed
        A_fill = button_fill # Do nothing, to prevent interfering with other commands

    def aup(): # A + UP
        A_fill = button_fill
        up_fill = udlr_fill
        os.system("sudo /home/kali/boot/scrnAup.sh") # bettercap 192.168.0.0
        clearscreen()
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/AUD.jpg")
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        tftcontrol()

    def aleft(): # A + LEFT
        A_fill = button_fill
        left_fill = udlr_fill
        os.system("sudo /home/kali/boot/scrnAleft.sh") # nmap 192.168.0.0/24
        clearscreen()
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/ALR.jpg")
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        tftcontrol()

    def aright(): # A + RIGHT
        A_fill = button_fill
        right_fill = udlr_fill
        os.system("sudo /home/kali/boot/scrnAright.sh") # nmap 192.168.1.0/24
        clearscreen()
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/nmap.jpg")
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        tftcontrol()

    def adown(): # A + DOWN
        A_fill = button_fill
        down_fill = udlr_fill
        os.system("sudo /home/kali/boot/scrnAdown.sh") # bettercap 192.168.1.0
        clearscreen()
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/AUD.jpg")
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        tftcontrol()

    def acenter(): # A + CENTER
        A_fill = button_fill
        center_fill = button_fill
        os.system("sudo /home/kali/boot/acenter.sh")


    def bempty(): # B Pressed
        B_fill = button_fill # Do nothing, to prevent interfering with other commands


    def bcenter():  # B + CENTER Pressed
        clearscreen()
        #disp.fill(0)


        # Troubles printing text, temp use of img


        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/Help.jpg")

        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))

        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)

        time.sleep(10)

        tftcontrol()

    def bup():  # B + UP
        B_fill = button_fill
        up_fill = udlr_fill
        #Upload?

    def bdown():  # B + DOWN
        down_fill = udlr_fill
        clearscreen()
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/Power.jpg")

        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))

        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        os.system("off")

    def bleft():  # B + LEFT
        left_fill = udlr_fill
        clearscreen()
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        if disp.rotation % 180 == 90:
            height = disp.width  # we swap height/width to rotate it to landscape!
            width = disp.height
        else:
            width = disp.width  # we swap height/width to rotate it to landscape!
            height = disp.height
        image = Image.new("RGB", (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image)

        image = Image.open("/home/kali/boot/imgs/Power.jpg")

        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))

        # Display image.
        disp.image(image)
        time.sleep(0.5)
        disp.image(image)
        time.sleep(5)

        os.system("sudo shutdown -r now")


    def commander():
        while True:
            up_fill = 0
            if not button_U.value:  # up pressed
                up_fill = udlr_fill
                up()
            draw.polygon(
                [(40, 40), (60, 4), (80, 40)], outline=udlr_outline, fill=up_fill
            )  # Up Arrow

            left_fill = 0
            if not button_L.value:  # left pressed
                left_fill = udlr_fill
                left()
            draw.polygon(
                [(0, 60), (36, 42), (36, 81)], outline=udlr_outline, fill=left_fill
            )  # Left Arrow

            right_fill = 0
            if not button_R.value:  # right pressed
                right_fill = udlr_fill
                right()
            draw.polygon(
                [(120, 60), (84, 42), (84, 82)], outline=udlr_outline, fill=right_fill
            )  # Right Arrow

            down_fill = 0
            if not button_D.value:  # down pressed
                down_fill = udlr_fill
                down()
            draw.polygon(
                [(60, 120), (80, 84), (40, 84)], outline=udlr_outline, fill=down_fill
            )  # Down Arrow

            center_fill = 0
            if not button_C.value:  # center pressed
                center_fill = button_fill
            draw.rectangle((40, 44, 80, 80), outline=button_outline, fill=center_fill)  # Center Block

            A_fill = 0
            if not button_A.value:  # A pressed
                A_fill = button_fill
                if not button_U.value: # A + UP
                    up_fill = udlr_fill
                    aup()
                elif not button_L.value: # A + LEFT
                    left_fill = udlr_fill
                    aleft()
                elif not button_R.value: # A + RIGHT
                    right_fill = udlr_fill
                    aright()
                elif not button_D.value: # A + DOWN
                    down_fill = udlr_fill
                    adown()
                elif not button_C.value: # A + CENTER
                    center_fill = button_fill
                    acenter()
                else:
                    A_fill = button_fill
                    aempty()
            draw.ellipse((140, 80, 180, 120), outline=button_outline, fill=A_fill)  # A button

            B_fill = 0
            if not button_B.value:  # B pressed
                B_fill = button_fill
                if not button_U.value:  # B + UP = Upload?
                    up_fill = udlr_fill
                    bup()
                elif not button_L.value:  # B + LEFT = Reboot
                    left_fill = udlr_fill
                    time.sleep(1)
                    clearscreen()
                    bleft()
                elif not button_R.value:  # B + RIGHT = Reset
                    right_fill = udlr_fill
                    os.system("sudo /home/kali/boot/reset-tft.sh")  # bash to kill this prog and restart it
                elif not button_D.value:  # B + DOWN = Shutdown
                    down_fill = udlr_fill
                    bdown()
                elif not button_C.value: # B + CENTER = Command list
                    center_fill = button_fill
                    clearscreen()
                    bcenter()
                else:
                    B_fill = button_fill
                    bempty()
                B_fill = button_fill
            draw.text((140, 5), "#6 + C - Help", font=fnt)
            draw.ellipse((190, 40, 230, 80), outline=button_outline, fill=B_fill)  # B button

            # make a random color and print text
            rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
            draw.text((15, 180), "POCKET NINJA", font=fnt2, fill=rcolor)

            # Display the Image
            disp.image(image)

            time.sleep(0.01)

    commander()


def bootlogo():
    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width  # we swap height/width to rotate it to landscape!
        height = disp.height
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)

    image = Image.open("/home/kali/boot/imgs/bootimg.jpg")

    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # Display image.
    disp.image(image)
    time.sleep(0.5)
    disp.image(image)
    time.sleep(5)

    tftcontrol()



bootlogo()
