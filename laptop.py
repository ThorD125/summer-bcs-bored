import socket
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button

# Initialize controllers
keyboard = KeyboardController()
mouse = MouseController()

# Function to handle received data
def handle_data(data):
    parts = data.split(":")
    if parts[0] == "kp":
        key = parts[1]
        if key.startswith('Key.'):
            key = getattr(Key, key.split('.')[1])
        keyboard.press(key)
    elif parts[0] == "kr":
        key = parts[1]
        if key.startswith('Key.'):
            key = getattr(Key, key.split('.')[1])
        keyboard.release(key)
    elif parts[0] == "mc":
        if parts[1] == 'left':
            button = Button.left
        elif parts[1] == 'right':
            button = Button.right
        mouse.position = (int(parts[2]), int(parts[3]))
        mouse.click(button)

# Setup socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(('192.168.1.105', 12345))
    print("Connected to server.")

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                handle_data(data)
        except ConnectionResetError:
            print("Connection to server lost.")
            break
except KeyboardInterrupt:
    print("Client stopped.")
finally:
    client_socket.close()
