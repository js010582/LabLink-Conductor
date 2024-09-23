import socket

def get_device_identity(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(b'*IDN?\n')  # Send the SCPI command to ask for device identity
        response = s.recv(1024)  # Read the response
        return response.decode().strip()

# Configuration
host = '192.168.1.219'  # Replace with the actual IP address of your Rigol DP832
port = 5555  # Common port for Rigol network-enabled devices

# Get the identity of the device
identity = get_device_identity(host, port)
print("Device Identity:", identity)

