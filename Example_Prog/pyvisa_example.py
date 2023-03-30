import pyvisa

# Create a resource manager object
rm = pyvisa.ResourceManager('@sim')
rm.list_resources()

# Find the instrument's VISA address (you may need to change the string)
instrument_address = 'USB0::0x1234::0x5678::INSTR'
instrument = rm.open_resource(instrument_address)

# Send a command to the instrument
# instrument.write('MEASure:VOLTage:DC?')

# Read the response from the instrument
# response = instrument.read()

# Print the response
# print('The voltage is {} V'.format(response.strip()))

# Close the instrument
instrument.close()

# Close the resource manager
rm.close()
