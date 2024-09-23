import pyvisa
import time
import tkinter as tk
from tkinter import ttk



class PowerSupply:
    def __init__(self, visa_address):
        self.resource_manager = pyvisa.ResourceManager()
        self.visa_address = visa_address
        self.instrument = None
        
    def connect(self):
        self.instrument = self.resource_manager.open_resource(self.visa_address)
        self.instrument.write_termination = '\n'
        self.instrument.read_termination = '\n'
        self.instrument.timeout = 5000 # set timeout to 5 seconds

    def reset(self):
        self.instrument.write("SYST:PRES")
    
    def set_voltage(self, voltage):
        self.instrument.write(f"SOUR:VOLT:LEV:IMM:AMPL {voltage}")
    
    def get_voltage(self):
        self.instrument.write(":MEAS:SCAL:VOLT:DC?")
        voltage = self.instrument.read()
        return voltage
    
    def set_current(self, current):
        self.instrument.write(f"SOUR:CURR:LEV:IMM:AMPL {current}")
    
    def get_current(self):
        self.instrument.write(":MEAS:SCAL:CURR:DC?")
        current = self.instrument.read()
        return current
    
    def set_ovp(self, voltage):
        self.instrument.write(f"SOUR:VOLT:PROT:LEV {voltage}")
    
    def set_ocp(self, current):
        self.instrument.write(f"SOUR:CURR:PROT:LEV {current}")
    
    def output_on(self):
        self.instrument.write(":OUTP:STATe:IMM ON")
    
    def output_off(self):
        self.instrument.write(":OUTP:STATe:IMM OFF")

    def idn(self):
        return self.instrument.query("*IDN?")

    def close(self):
        self.instrument.close()
        self.resource_manager.close()

class PowerSupplyGUI():
    def __init__(self, visa_address):
        self.ps = PowerSupply(visa_address)
        self.ps.connect()

        self.root = tk.Tk()
        self.root.title("FlatSat PS Control")

        # Set initial values for voltage, current, ovp, and ocp
        self.voltage_value = tk.DoubleVar(value=32.0)
        self.current_value = tk.DoubleVar(value=1.0)
        self.ovp_value = tk.DoubleVar(value=34.0)
        self.ocp_value = tk.DoubleVar(value=3.8)

        # Create labels and entry widgets for voltage and current
        voltage_label = ttk.Label(self.root, text="Voltage (V):")
        voltage_label.grid(row=0, column=0)
        self.voltage_entry = ttk.Entry(self.root, width=10,textvariable=self.voltage_value)
        self.voltage_entry.grid(row=0, column=1)
        
        current_label = ttk.Label(self.root, text="Current (A):")
        current_label.grid(row=1, column=0)
        self.current_entry = ttk.Entry(self.root, width=10,textvariable=self.current_value)
        self.current_entry.grid(row=1, column=1)

        #voltage_output = ttk.Label(self.root, text="Output Voltage (V):")
        self.vout_label = tk.Label(self.root, text="Voltage Output:")
        self.vout_label.grid(row=0, column=2)
        self.vout_value = tk.DoubleVar(value=0.0)
        self.vout_indicator = tk.Label(self.root, textvariable=self.vout_value)
        self.vout_indicator.grid(row=0, column=3)

        self.iout_label = tk.Label(self.root, text="Current Output:")
        self.iout_label.grid(row=1, column=2)
        self.iout_value = tk.DoubleVar(value=0.0)
        self.iout_indicator = tk.Label(self.root, textvariable=self.iout_value)
        self.iout_indicator.grid(row=1, column=3)

        self.meas_voltage_current()
    
        # Create labels and entry widgets for OVP and OCP
        ovp_label = ttk.Label(self.root, text="OVP (V):")
        ovp_label.grid(row=2, column=0)
        self.ovp_entry = ttk.Entry(self.root, width=10, textvariable=self.ovp_value)
        self.ovp_entry.grid(row=2, column=1)

        ocp_label = ttk.Label(self.root, text="OCP (A):")
        ocp_label.grid(row=3, column=0)
        self.ocp_entry = ttk.Entry(self.root, width=10, textvariable=self.ocp_value)
        self.ocp_entry.grid(row=3, column=1)

          # Create a button to set the voltage, current, OCP, OVP values
        set_button = ttk.Button(self.root, text="Set", command=self.set_values)
        set_button.grid(row=4, column=1)

        # Create a toggle button to turn the output on and off
        self.output_state = tk.BooleanVar()
        output_button = ttk.Checkbutton(self.root, text="Output", variable=self.output_state, command=self.toggle_output)
        output_button.grid(row=4, column=0)

         # Set initial values for voltage, current, OVP, and OCP
        self.ps.set_voltage(self.voltage_value.get())
        self.ps.set_current(self.current_value.get())
        self.ps.set_ovp(self.ovp_value.get())
        self.ps.set_ocp(self.ocp_value.get())
      
    def set_values(self):
        voltage = float(self.voltage_entry.get())
        current = float(self.current_entry.get())
        ovp = float(self.ovp_entry.get())
        ocp = float(self.ocp_entry.get())
        self.ps.set_voltage(voltage)
        self.ps.set_current(current)
        self.ps.set_ovp(ovp)
        self.ps.set_ocp(ocp)

    def toggle_output(self):
        if self.output_state.get():
            self.ps.output_on()
        else:
            self.ps.output_off()

    def start(self):
        self.root.mainloop()

    def meas_voltage_current(self):
        voltage = self.ps.get_voltage()
        current = self.ps.get_current()
        self.vout_value.set(voltage)
        self.iout_value.set(current)
        self.root.after(5000, self.meas_voltage_current)
        
# App Start
gui = PowerSupplyGUI("FlatSat_PS")
gui.start()
