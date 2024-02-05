# EKG Arduino

This project utilises the AD8323 EKG sensor to monitor heart activity. The included code enables user to record EKG segments and save them to PDF
. Schemes for both Raspberry Pi and Arduino are proposed.

**Arduino code**

File `readEKG.ino` is inspired by [this website](https://navody.dratek.cz/navody-k-produktum/ekg-monitoring-srdecni-frekvence-ad8232.html) and it reads the senzor output and writes it to the serial port.

**Python code**

File `main.py` reads the data from the serial port and processes it. Parameters FRAMES and WINDOW customize the recorded segment. Most recent WINDOW number of datapoints are shown on live graph and pressing the R key saves FRAMES number of upcomming windows. Pressing the Q key will terminate the program.
