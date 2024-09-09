import socket

HOST = '127.0.0.1'
PORT = 65432
message = "GET / HTTP/1.0\r\n"
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server is listening on {HOST}:{PORT}")

while True:
    
    client_socket, address = server_socket.accept()
    print(f"Accepted client")
    
    try:
        data = client_socket.recv(1024)
        print(data.decode('utf-8'))
        client_socket.send(data)
        if data:
            print("Client disconnected")
            break
        message_length = len(data.decode('utf-8'))
        client_socket.send(message_length.to_bytes(4, byteorder='big'))
    except Exception as e:
        print("Error")
    finally:
        client_socket.close()
server_socket.close()
        