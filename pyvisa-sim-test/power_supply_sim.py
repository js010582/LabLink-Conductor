import pyvisa
import pyvisa_sim

pyvisa_sim.configure('power_supply.yaml')

rm = pyvisa.ResourceManager('@sim')
power_supply = rm.open_resource('TCPIP0::localhost::5025::SOCKET')

power_supply.write('OUTPut ON')
voltage = power_supply.query('VOLTage?')
current = power_supply.query('CURRent?')

print(f"Voltage: {voltage} V")
print(f"Current: {current} A")