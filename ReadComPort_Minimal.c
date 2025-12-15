// C File zum auslesen vom COM Port - Black Box im Linux Betriebssystem

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

int main() {
    const char* port = "/dev/ttyUSB0";
    int serial_port = open(port, O_RDWR);


    struct termios tty;
    cfsetospeed(&tty, B115200);  // Baudrate setzen
    tty.c_cc[VTIME] = 10;       // 1s Timeout
    tty.c_cc[VMIN]  = 10;      // mindestens 10 Zeichen


    // Endlosschleife zum Lesen
    while (1) {
        char buffer[256];
        memset(buffer, 0, sizeof(buffer));
        int num_bytes = read(serial_port, buffer, sizeof(buffer));
        printf("Gelesen: %s\n", buffer); 
        // Ab hier die Aufgaben lösen...
    }

    close(serial_port);
    return 0;
}

