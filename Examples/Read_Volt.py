import socket

def read_voltage(ip, port, channel):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        command = f':SOURce<1>:MEAS:VOLT? {channel}\n'.encode()  # Construct the command to measure voltage
        s.sendall(command)
        response = s.recv(1024)  # Read the response
        return response.decode().strip()

# Configuration
host = '192.168.1.219'  # IP address of your Rigol DP832
port = 5555  # Common port for Rigol devices, adjust if your settings differ

# Read the voltage of Channel 1
voltage = read_voltage(host, port, 'CH1')
print(f"Measured Voltage on Channel 1: {voltage} V")