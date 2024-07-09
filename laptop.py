import socket
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button

# Initialize controllers
keyboard = KeyboardController()
mouse = MouseController()

# Function to handle received data
def handle_data(data):
    parts = data.split(":")
    if parts[0] == "kp":
        if parts[1] == 'Key.space':
            keyboard.press(' ')
        else:
            keyboard.press(parts[1])
    elif parts[0] == "kr":
        if parts[1] == 'Key.space':
            keyboard.release(' ')
        else:
            keyboard.release(parts[1])
    elif parts[0] == "mc":
        if parts[1] == 'left':
            button = Button.left
        elif parts[1] == 'right':
            button = Button.right
        mouse.position = (int(parts[2]), int(parts[3]))
        mouse.click(button)

# Setup socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.105', 12345))

try:
    while True:
        data = client_socket.recv(1024).decode()
        if data:
            handle_data(data)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client_socket.close()
