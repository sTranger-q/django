import socket
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
# 响应体定义

# 响应格式：响应行、响应头、空行、响应体.

def handle_connection(conn,addr):
    request =b''
    import time
    time.sleep(10)
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
    print(request)
    conn.send(response.encode())
    conn.close()

def main():
    # ip
    # socket.AF_INET    决定了要用ipv4地址（32位的）与端口号（16位的）的组合
    # socket.SOCK_STREAM   PPROTO_TCP TCP传输协议
    serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    serversocket.bind(('127.0.0.1',8000))
    serversocket.listen(5)
    print('http://127.0.0.1:8000')
    try:
        while True:
            conn,address = serversocket.accept()
            handle_connection(conn,address)
    finally:
        serversocket.close()

if __name__ == '__main__':
    main()
