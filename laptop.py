import socket
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button

# Initialize controllers
keyboard = KeyboardController()
mouse = MouseController()

# Function to handle received data
def handle_data(data):
    try:
        parts = data.split(":")
        if len(parts) < 2:
            print(f"Received malformed data: {data}")
            return
        
        action = parts[0]
        key = parts[1]
        
        if action == "kp":
            if key.startswith('Key.'):
                key = getattr(Key, key.split('.')[1], key)
            keyboard.press(key)
        elif action == "kr":
            if key.startswith('Key.'):
                key = getattr(Key, key.split('.')[1], key)
            keyboard.release(key)
        elif action == "mc" and len(parts) == 4:
            if key == 'left':
                button = Button.left
            elif key == 'right':
                button = Button.right
            else:
                print(f"Received unknown button: {key}")
                return
            
            x, y = int(parts[2]), int(parts[3])
            mouse.position = (x, y)
            mouse.click(button)
        else:
            print(f"Received unknown action or malformed data: {data}")
    except Exception as e:
        print(f"Error handling data: {data} -> {e}")

# Setup socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(('PC_IP_ADDRESS', 12345))
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
