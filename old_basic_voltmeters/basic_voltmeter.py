import serial
import tkinter as tk

def read_from_arduino():
    while True:
        if ser.in_waiting > 0:
            arduino_data = ser.readline().decode().strip()
            print(arduino_data)  # Display data in terminal
            try: update_gui(float(arduino_data))  # Update GUI label with average voltage
            except: update_gui(arduino_data)

def update_gui(avg_voltage):
    label.config(text=f"Average Analog Voltage: {avg_voltage:.2f} V")

# Arduino Serial Connection
ser = serial.Serial('/dev/cu.usbmodem1422101', 9600)  # Replace 'COM3' with your port

# Create GUI
root = tk.Tk()
root.title("Average Analog Voltage Display")

label = tk.Label(root, font=('Helvetica', 24))
label.pack(padx=20, pady=40)

# Start reading from Arduino
read_from_arduino()

root.mainloop()
