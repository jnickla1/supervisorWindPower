import serial
import tkinter as tk

def read_from_arduino():
    if ser.in_waiting > 0:
        arduino_data = float(ser.readline().decode().strip())
        corrected_voltage0 = (arduino_data*4.96/1023.0/128.0/6.0)
        corrected_voltage1 = (corrected_voltage0-2.6117)*3.47/1.97*3.77/3.51
        print(corrected_voltage1)  # Display data in terminal
        update_gui(corrected_voltage1)  # Update GUI label with average voltage
       # except: update_gui(arduino_data)
    root.after(20, read_from_arduino)

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

root.after(20, read_from_arduino)
root.mainloop()
