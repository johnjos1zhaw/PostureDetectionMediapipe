import socket
import cv2
import numpy as np
import struct

# Create a socket connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000))  # Use '0.0.0.0' to accept connections from any IP address
server_socket.listen(0)
connection, address = server_socket.accept()
connection = connection.makefile('rb')

try:
    while True:
        # Read the length of the image as a packed 32-bit unsigned int.
        image_len = struct.unpack('<L', connection.read(4))[0]
        if not image_len:
            break

        # Read the image data.
        image_data = connection.read(image_len)

        # Convert the image data to a NumPy array.
        image = np.frombuffer(image_data, dtype=np.uint8)

        # Decode the image.
        frame = cv2.imdecode(image, 1)

        # Display the image.
        cv2.imshow('Video Stream', frame)

        # Break the loop if 'q' is pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    connection.close()
    server_socket.close()
    cv2.destroyAllWindows()

