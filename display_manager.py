import time
from PIL import Image, ImageDraw, ImageFont

class DisplayManager:
    def __init__(self):
        self.oled = None
        self.width = 128
        self.height = 64
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        
        try:
            import board
            import busio
            import digitalio
            import adafruit_ssd1306
            
            # SPI Setup based on user configuration
            spi = busio.SPI(board.SCK, MOSI=board.MOSI)
            dc = digitalio.DigitalInOut(board.D24)
            res = digitalio.DigitalInOut(board.D25)
            cs = digitalio.DigitalInOut(board.D5)
            
            self.oled = adafruit_ssd1306.SSD1306_SPI(self.width, self.height, spi, dc, res, cs)
            self.clear()
            print("OLED Display initialized successfully.")
        except Exception as e:
            print(f"WARNING: OLED Display could not be initialized: {e}")
            self.oled = None

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        if self.oled:
            self.oled.fill(0)
            self.oled.show()

    def show_message(self, line1, line2=""):
        # Clear image buffer
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        
        # Draw a nice border
        self.draw.rectangle((0, 0, self.width-1, self.height-1), outline=255, fill=0)
        self.draw.rectangle((2, 2, self.width-3, self.height-3), outline=255, fill=0)

        # Draw text
        # Using default font, centering logic
        try:
            # Try to load a font if available, else use default
            font = ImageFont.load_default()
        except:
            font = None

        # Line 1
        w1, h1 = self.draw.textbbox((0, 0), line1, font=font)[2:]
        self.draw.text(((self.width - w1) // 2, 15), line1, font=font, fill=255)
        
        # Line 2
        if line2:
            w2, h2 = self.draw.textbbox((0, 0), line2, font=font)[2:]
            self.draw.text(((self.width - w2) // 2, 35), line2, font=font, fill=255)

        if self.oled:
            self.oled.image(self.image)
            self.oled.show()
        else:
            print(f"DISPLAY MOCK: [{line1}] [{line2}]")

    def show_welcome(self, name):
        self.show_message("WELCOME,", name.upper() + "!")

    def show_locked(self):
        self.show_message("SYSTEM LOCKED", "Waiting for face...")

    def show_unlocked(self):
        self.show_message("ACCESS GRANTED", "Lock is Open")

    def show_closing(self):
        self.show_message("CLOSING LOCK", "Please wait...")
