import socket

def set_voltage(ip, port, channel, voltage):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        command = f':VOLT:LEV:IMM:AMPL {voltage}\n'.encode()  # Construct the command to set voltage
        s.sendall(command)
        # Optionally, you can wait for the device to acknowledge the command
        # response = s.recv(1024)
        # return response.decode().strip()

# Configuration
host = '192.168.1.219'  # IP address of your Rigol DP832
port = 5555  # Common port for Rigol devices

# Set the voltage of Channel 1 to 2.0V
set_voltage(host, port, 'CH1', 1.35)