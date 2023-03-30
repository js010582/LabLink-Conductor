import PySimpleGUI as sg
import pyvisa
import pyvisa_sim
import time

class PowerSupply:
    def __init__(self, visa_address):
        self.resource_manager = pyvisa.ResourceManager('@sim')
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

        # Set initial values for voltage, current, ovp, and ocp
        self.voltage_value = 32.0
        self.current_value = 1.0
        self.ovp_value = 34.0
        self.ocp_value = 3.8

        # Create layout for window
        layout = [[sg.Text('Voltage (V):'), sg.InputText(default_text=self.voltage_value, key='-VOLTAGE-')],
                  [sg.Text('Current (A):'), sg.InputText(default_text=self.current_value, key='-CURRENT-')],
                  [sg.Text('Output Voltage:'), sg.Text('0.0', size=(10, 1), key='-VOLTAGE_OUT-')],
                  [sg.Text('Current Output:'), sg.Text('0.0', size=(10, 1), key='-CURRENT_OUT-')],
                  [sg.Text('OVP (V):'), sg.InputText(default_text=self.ovp_value, key='-OVP-')],
                  [sg.Text('OCP (A):'), sg.InputText(default_text=self.ocp_value, key='-OCP-')],
                  [sg.Button('Set'), sg.Checkbox('Output', key='-OUTPUT-')]]

        # Create window
        self.window = sg.Window('FlatSat PS Control', layout)

    def set_values(self):
        voltage = float(self.window['-VOLTAGE-'].Get())
        current = float(self.window['-CURRENT-'].Get())
        ovp = float(self.window['-OVP-'].Get())
        ocp = float(self.window['-OCP-'].Get())
        self.ps.set_voltage(voltage)
        self.ps.set_current(current)
        self.ps.set_ovp(ovp)
        self.ps.set_ocp(ocp)

    def toggle_output(self):
        if self.window['-OUTPUT-'].Get():
            self.ps.output_on()
        else:
            self.ps.output_off()

    def start(self):
        while True:
            event, values = self.window.read(timeout=5000)
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            if event == 'Set':
                self.set_values()
            if event == '-OUTPUT-':
                self.toggle_output()
            voltage = self.ps.get_voltage()
            current = self.ps.get_current()
            self.window['-VOLTAGE_OUT-'].Update(voltage)
            self.window['-CURRENT_OUT-'].Update(current)

        self.window.close()
        self.ps.close()

gui = PowerSupplyGUI('FlatSat_PS')
gui.start()
