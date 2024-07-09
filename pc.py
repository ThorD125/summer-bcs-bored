import socket
from pynput import keyboard, mouse

# Function to send data to the client
def send_data(data):
    try:
        client_socket.sendall(data.encode())
    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
        print("Connection lost. Stopping...")
        keyboard_listener.stop()
        mouse_listener.stop()

# Keyboard event handlers
def on_key_press(key):
    try:
        send_data(f"kp:{key.char}")
    except AttributeError:
        send_data(f"kp:{key}")

def on_key_release(key):
    try:
        send_data(f"kr:{key.char}")
    except AttributeError:
        send_data(f"kr:{key}")

# Mouse event handlers
def on_click(x, y, button, pressed):
    if pressed:
        send_data(f"mc:{button.name}:{x}:{y}")

# Setup socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(1)
print("Waiting for connection...")

try:
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    # Setup listeners
    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()
except KeyboardInterrupt:
    print("Server stopped.")
finally:
    if 'client_socket' in locals():
        client_socket.close()
    server_socket.close()
