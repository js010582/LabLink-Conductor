#Code does not work

import socket

def read_set_voltage(ip, port, channel):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        command = f'SOURce2:VOLT? {channel}\n'.encode()  # Query the set voltage
        s.sendall(command)
        response = s.recv(1024)  # Read the response
        return response.decode().strip()

# Configuration
host = '192.168.1.219'  # IP address of your Rigol DP832
port = 5555  # Common port for Rigol devices

# Read the set voltage of Channel 1
set_voltage = read_set_voltage(host, port, 'CH1')
print(f"Set Voltage on Channel 1: {set_voltage} V")
