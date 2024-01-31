import smbus
import time

# I2C bus and device address
bus = smbus.SMBus(1)
address = 0x27

# LCD configuration
lcd_width = 16
lcd_lines = 2

# Command definitions
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Write 4 bits to the LCD
def lcd_write_4bits(value):
    bus.write_byte(address, value << 4)
    lcd_strobe()

# Strobes the enable pin
def lcd_strobe():
    bus.write_byte(address, 0x04 | 0x08)
    time.sleep(0.0005)
    bus.write_byte(address, 0x00 & ~0x08)
    time.sleep(0.002)

# Write a command to the LCD
def lcd_write_cmd(cmd):
    lcd_write_4bits(cmd >> 4)
    lcd_write_4bits(cmd & 0x0F)
    time.sleep(0.002)

def lcd_clear():
    lcd_write_cmd(0x01)  # Command to clear the display
    time.sleep(0.002)


# Initialize the LCD
def lcd_init():
    # Wait for the device to initialize
    time.sleep(0.020)

    # Set the LCD to 4-bit mode
    lcd_write_cmd(0x03 << 4)
    time.sleep(0.005)

    # Set the LCD to 4-bit mode (again)
    lcd_write_cmd(0x03 << 4)
    time.sleep(0.0005)

    # Set the LCD to 4-bit mode (again)
    lcd_write_cmd(0x03 << 4)
    time.sleep(0.0005)

    # Set the LCD to 4-bit mode
    lcd_write_cmd(0x02 << 4)

    # Set the display parameters
    lcd_write_cmd(LCD_FUNCTIONSET | LCD_4BITMODE | LCD_2LINE | LCD_5x8DOTS)
    lcd_write_cmd(LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF)
    lcd_write_cmd(LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT)
    lcd_clear()

lcd_init()