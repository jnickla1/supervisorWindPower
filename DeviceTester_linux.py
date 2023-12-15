# Wind Power Device Test Phase Automated

import tkinter as tk
import serial
import time
import threading




def doit():
    t = threading.current_thread()
    while getattr(t, "do_run", True):
        read_from_arduino()
        time.sleep(20/1000)
    print("Stopping as you wish.")


# Function to read data from Arduino
def read_from_arduino():
    if ser.in_waiting > 0:
        arduino_data = float(ser.readline().decode().strip())
        corrected_voltage0 = (arduino_data*4.96/1023.0/128.0/6.0)
        corrected_voltage1 = (corrected_voltage0-2.6117)*3.47/1.97*3.77/3.51
        print(corrected_voltage1)  # Display data in terminal
        update_voltage_display(corrected_voltage1)  # Update GUI label with average voltage
       # except: update_gui(arduino_data)


# Function to update voltage display
def update_voltage_display(voltage):
    global average_label
    average_label.config(text=f"Average Voltage: {voltage:.2f} V")
    # Update maximum voltage if needed
    # Keep track of maximum voltage received during the test
    global max_voltage
    global max_label
    if (abs(voltage) > max_voltage) and ( abs(voltage) <4.8) :
        max_voltage = abs(voltage)
        max_label.config(text=f"Max Voltage: {max_voltage:.2f} V")

# Function to start device test phase
def start_device_test():
    global max_voltage
    global average_label
    global max_label
    max_voltage = 0.0  # Reset max voltage
    # Start reading from Arduino
    while ser.in_waiting > 0:
        ser.readline() #clear anomalous readings that have built up in serial port
    arduino_thread = threading.Thread(target=doit)
    arduino_thread.daemon = True  # Set as daemon to close when main window closes
    arduino_thread.start()
    global th
    setattr(th, "timenow", 45) #45

    # Create device test window
    device_test_window = tk.Toplevel(root)
    device_test_window.title("Device Test Phase")
    device_test_window.geometry('400x200')

    # Countdown timer for 30 seconds
    countdown =30 #30
    countdown_label = tk.Label(device_test_window, font=('Helvetica', 24))
    countdown_label.pack(padx=20, pady=40)

    # Labels to display average and max voltage
    average_label = tk.Label(device_test_window, font=('Helvetica', 18))
    average_label.pack()
    max_label = tk.Label(device_test_window, font=('Helvetica', 18))
    max_label.pack()

    # Function to update countdown label
    def update_countdown():
        nonlocal countdown
        if countdown > 0:
            countdown_label.config(text=str(countdown))
            countdown -= 1
            device_test_window.after(1000, update_countdown)
        elif countdown > -15: #-15
            arduino_thread.do_run=False
            countdown_label.config(text=str(countdown))
            countdown -= 1
            average_label.config(text="End of test - remove turbine")
            # Stop displaying maximum voltage after 15 seconds
            device_test_window.after(1000, update_countdown)
            
        
        else:
            # Log maximum voltage and timestamp to a file
            log_data(max_voltage)
            # Close device test window after logging data
            global test_screen
            test_screen=False
            device_test_window.destroy()

    # Start countdown
    update_countdown()

def draw(event):
    if event.char == ' ':
        start_device_try()
    elif event.char == 's':
        start_3min()


def start_device_try():
    global first_open
    global th
    if(getattr(th, "timenow")<180):
        if(first_open):
            start_device_test()
            first_open=False
        else:
            global max_label
            if(not(max_label.winfo_exists())):
                start_device_test()

# Function to log data to a file
def log_data(voltage):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("voltage_log.txt", "a") as file:
        file.write(f"{timestamp}, Max Voltage: {voltage:.9f} V\n")


def cd():
    global timer_label_obj
    t = threading.current_thread()
    while (getattr(t, "timenow") > 0) :
        ts = getattr(t, "timenow")
        m, s = divmod(ts, 60)
        timer_label_obj.config(text=str('{:02d}:{:02d}'.format(m,s)))
        setattr(t, "timenow", ts-1)
        time.sleep(1)
        if ts == 60:
            if(first_open):
                root.bell()
            else:
                global max_label
                if(not(max_label.winfo_exists())):
                    root.bell()
        if ts == 45:
            start_device_try()
            
    timer_label_obj.config(text="Begin")
    global th
    th = threading.Thread(target=cd)
    setattr(th, "timenow", 180)
    
    
def start_3min():
    global th
    th.start()


global first_open
first_open = True
# Arduino Serial Connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace 'COM3' with your port

# Create GUI
root = tk.Tk()
root.title("Device Test Setup")
root.geometry('300x200')
# Button to start device test
start_button = tk.Button(root, text="Start Device Test", command=start_device_try)
start_button.pack(padx=20, pady=(40,0))
timer_label_obj = tk.Label(root, font=('Helvetica', 24))
timer_label_obj.config(text="Begin")
timer_label_obj.pack()

global th
th = threading.Thread(target=cd)
setattr(th, "timenow", 180)
three_button = tk.Button(root, text="Start 3min Countdown", command=start_3min)
three_button.pack()
root.bind('<Key>', draw)
root.mainloop()
