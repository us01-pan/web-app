import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)

    while True:
        conn, addr = s.accept()
        with conn:
            request = conn.recv(1024).decode()
            print(request)
            response = 'HTTP/1.0 200 OK\n\nHello World'
            conn.sendall(response.encode())