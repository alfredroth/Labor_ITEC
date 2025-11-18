import machine
import time

from machine import Pin, I2C      #Lib fuer GPIO & i2c
from lib.ssd1306 import SSD1306_I2C   #Lib fuer Display
from lib.hcsr04 import HCSR04         #Lib fuer US-Sensor

# UART Schnittstelle definieren (UART0)
uart = machine.UART(1, baudrate=115200)
donoff = Pin( 36, Pin.OUT) # Anzeige AUS (High)  EIN (Low)

#Sensor definieren
sensor = HCSR04(trigger_pin=7, echo_pin=6,echo_timeout_us=1000000) # Pins & echo Pause(µs!)

#Display definierern und starten
i2c = SoftI2C(sda=Pin(17), scl=Pin(18))# I2C Bus für Display
reset=Pin(21, Pin.OUT,value=1) # Reset Pin für display muss 1->0->1
donoff.value(0) # Anzeige EIN
reset.value(1)#  
reset.value(0)
reset.value(1)
sleep(1)
s= 0 

display = ssd1306.SSD1306_I2C(128, 64, i2c)


def send_data(data):
    """Sends data over the UART interface."""
    uart.write(data + '\n')  # Daten schreiben

def main():
    m=0
    while True:
        s = sensor.distance_cm() # US-Sensor Wert aktualisieren
        donoff.value(0)
        m=m+1  # Zum hochzählen
        data_to_send = f"{s:.1f}"
        # print("Entfernung: {:.1f} cm".format(s))
        print(s)
        display.fill(0)
        display.text ("DEB-Black Box 1",00,0) #Text in Zeile 1
        display.text ("Messung "+str(m),00,20) #Text in Zeile 2
        display.text (str(s),00,40) #Text in Zeile 3
        display.show()
        send_data(data_to_send) #  Funktion send_data
        time.sleep(1) #Abtsatzeit

if __name__ == "__main__":
    main()







