Examine and replicate circuit_schematic.pdf as in circuit_image.


First install Arduino IDE (https://www.arduino.cc/en/software) so you can upload the simple_voltmeter3_copy.ino code to your arduino.
Second install various python packages: 

'''
sudo apt-get install python3-tk (linux)
brew install python3-tk (mac)
pip3 install pyserial
pip3 install threading
''' 

Then run DeviceTester_linux.py or DeviceTester_mac.py. You may need to adjust the constants so that it reads 0 depending on the precise value of your resistors.

Finally import votage_log.txt into the "total wind poweer scores.xls" document at columnL, and perform a text-to-data split along spaces.
