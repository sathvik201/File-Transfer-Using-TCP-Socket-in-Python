import socket
import threading


# Server function to receive a file
def start_server():
    server_address = ('localhost', 65432)

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind(server_address)

        # Listen for incoming connections
        server_socket.listen()
        print(f"Server listening on {server_address[0]}:{server_address[1]}")

        # Accept a connection
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            with open('received_file.txt', 'wb') as file:
                while True:
                    # Receive data from the client
                    data = conn.recv(1024)
                    if not data:
                        print("No more data received. File transfer complete.")
                        break
                    # Write the received data to a file
                    file.write(data)
            print("File received and saved as 'received_file.txt'")

            # Display the content of the received file
            with open('received_file.txt', 'r') as file:
                content = file.read()
                print("Content of the received file:")
                print(content)


# Client function to send a file
def start_client():
    server_address = ('localhost', 65432)

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect(server_address)
        print(f"Connected to server at {server_address[0]}:{server_address[1]}")

        # Open the file to send
        file_path = '/content/New Text Document.txt'  # Corrected to match the file created
        with open(file_path, 'rb') as file:
            # Read and send the file content in chunks
            while chunk := file.read(1024):
                client_socket.sendall(chunk)
        print("File sent successfully.")


# Write some example content to a file in Colab to simulate a real file
with open('file_to_send.txt', 'w') as f:
    f.write('This is an example file content that will be sent to the server.')

# Threading to simulate client and server interaction
server_thread = threading.Thread(target=start_server)
client_thread = threading.Thread(target=start_client)

# Start the server thread
server_thread.start()

# Start the client thread
client_thread.start()

# Wait for both threads to complete
server_thread.join()
client_thread.join()