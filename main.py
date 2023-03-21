# Program:  LabLink-Conductor Program
# Author:   Jasper Sandhu
# Date:     3/20/23

import PySimpleGUI as sg
import socket
from easy_scpi import scpi_instrument
# from easy_scpi import SCPI

# Establish connection to the power supply
def connect_to_device(ip_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_address, port))
    return SCPI(s)

# Update the settings for the power supply
def set_power_supply_values(device, channel, voltage, current, over_voltage, over_current):
    device.write(f'INST OUT{channel}')
    device.write(f'VOLT {voltage}')
    device.write(f'CURR {current}')
    device.write(f'VOLT:PROT {over_voltage}')
    device.write(f'CURR:PROT {over_current}')

# Define the layout for the GUI
layout = [
    [sg.Text("IP Address:"), sg.InputText(key="ip_address")],
    [sg.Text("Port:"), sg.InputText(key="port")],
    [sg.Button("Connect")],
    [sg.Text("Channel:"), sg.Combo(["1", "2"], key="channel")],
    [sg.Text("Voltage (V):"), sg.InputText(key="voltage")],
    [sg.Text("Current (A):"), sg.InputText(key="current")],
    [sg.Text("Over Voltage (V):"), sg.InputText(key="over_voltage")],
    [sg.Text("Over Current (A):"), sg.InputText(key="over_current")],
    [sg.Button("Set"), sg.Button("Exit")]
]

# Create the window
window = sg.Window("Dual Power Supply Controller", layout)

# Event loop
device = None
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    elif event == "Connect":
        print("Trying to connect")
        try:
            ip_address = values["ip_address"]
            port = int(values["port"])
            device = connect_to_device(ip_address, port)
            sg.popup("Connected to power supply!")
        except Exception as e:
            sg.popup("Error connecting to power supply:", str(e))
    elif event == "Set":
        if device:
            try:
                channel = values["channel"]
                voltage = float(values["voltage"])
                current = float(values["current"])
                over_voltage = float(values["over_voltage"])
                over_current = float(values["over_current"])

                set_power_supply_values(device, channel, voltage, current, over_voltage, over_current)
                sg.popup("Settings updated!")
            except Exception as e:
                sg.popup("Error updating settings:", str(e))
        else:
            sg.popup("Error: Not connected to a power supply.")

# Close the window
window.close()
