import socket

port = 21
host = "ftp.3700.network"
user = "wangjus"
password = "QFEt6svMOZLXhIp3DqgA"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(15)
sock.connect((host, port))
message = sock.recv(4096)
print(message)

data_user = 'USER wangjus\r\n'
sock.sendall(bytes(data_user.encode()))
message = sock.recv(4096)

data_pass = 'PASS QFEt6svMOZLXhIp3DqgA\r\n'
sock.sendall(bytes(data_pass.encode()))
message = sock.recv(4096)
print(message)

data_type = 'TYPE I\r\n'
sock.sendall(bytes(data_type.encode()))
message = sock.recv(4096)
print(message)

data_mode = 'MODE S\r\n'
sock.sendall(bytes(data_mode.encode()))
message = sock.recv(4096)
print(message)

data_stru = 'STRU F\r\n'
sock.sendall(bytes(data_stru.encode()))
message = sock.recv(4096)
print(message)