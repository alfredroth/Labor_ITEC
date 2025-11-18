# boot.py wird nur einmal ausgeführt


# Bibliotheken laden
import machine
from machine     import Pin, SoftI2C
from time        import sleep
from lib         import ssd1306
#===============================================================================
# Zuordnung der Hardware-Pins
LED   = Pin( 35, Pin.OUT) # Pin35 = interne LED
donoff = Pin( 36, Pin.OUT) # Anzeige (Display) AUS (High)  EIN (Low)
zeit=0.2 # Zeit in sekunden 200ms
k=1
while k<4:
    LED.value(1) # LED Ein  oder LED.value(1)
    sleep(zeit)
    LED.value(False) # LED Aus oder LED.value(0) 
    sleep(zeit)
    k=k+1


i2c = SoftI2C(sda=Pin(17), scl=Pin(18))# I2C Bus für Display
reset=Pin(21, Pin.OUT,value=1) # Reset Pin für display muss 1->0->1
donoff.value(0) # Anzeige EIN
reset.value(1)  
reset.value(0)
reset.value(1)
sleep(0.5) # Musst halt warten , sonst keine Komm zum i2c Teilnehmer(Display)


display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.fill(0)
display.text ("D E B",00,0) #Text in Zeile 1
display.text ("Labor ITEC ",00,20) #Text in Zeile 2
display.text ("BLACK BOX 1",00,45) #Text in Zeile 3
display.show()
sleep(1) # 
