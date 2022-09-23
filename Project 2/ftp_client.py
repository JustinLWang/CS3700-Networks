from ipaddress import ip_interface
import socket
import argparse
import sys
from urllib.parse import urlparse

USER = "wangjus"
PASSWORD = "QFEt6svMOZLXhIp3DqgA"

# Parses command line arguments
def add_parser():
    parser = argparse.ArgumentParser(description='Parser command line arguments', usage='$./3700ftp [operation] [-p1 param1] [-p2 param2]')
    parser.add_argument('operation')
    parser.add_argument('-p1', dest='param1', required=False)
    parser.add_argument('-p2', dest='param2', required=False)
    args = parser.parse_args(sys.argv[1:])
    
    return args

def log_in(sock):
    data_user = 'USER wangjus\r\n'
    sock.sendall(bytes(data_user.encode()))
    sock.recv(4096)

    data_pass = 'PASS QFEt6svMOZLXhIp3DqgA\r\n'
    sock.sendall(bytes(data_pass.encode()))
    log_in_message = sock.recv(4096)
    print(log_in_message)

def configure(sock):
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

def get_data_channel_ip_port(sock):
    open_data_channel = 'PASV \r\n'
    sock.sendall(bytes(open_data_channel.encode()))
    message_data_channel = sock.recv(4096).decode()
    string_message = "".join(message_data_channel)
    modified_string = string_message.replace('(', "")
    modified_string = modified_string.replace(')', "")
    modified_string = modified_string.replace('.\r\n', "")
    modified_string = modified_string.split(' ')[4]
    ip_port = modified_string.split(',')
    ip = ".".join(ip_port[0:4])
    port = (int(ip_port[4:][0]) << 8) + int(ip_port[4:][1])

    return (ip, port)

def open_data_channel(ip, port):
    data_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_channel.settimeout(15)
    data_channel.connect((ip, port))

    return data_channel
    
    

def request_operation(sock, oper, p1="", p2=""):
    if (oper == 'quit'):
        data = 'QUIT\r\n'
        sock.sendall(bytes(data.encode()))
        message = sock.recv(4096)
        print(message)
        sock.close()
    elif (oper == 'mkdir'):
        url = urlparse(p1)
        path = url[2]
        data = 'MKD ' + path + '\r\n'
        sock.sendall(bytes(data.encode()))
        message = sock.recv(4096)
        print(message)
    elif (oper == 'rmdir'):
        url = urlparse(p1)
        path = url[2]
        data = 'RMD ' + path + '\r\n'
        sock.sendall(bytes(data.encode()))
        message = sock.recv(4096)
        print(message)
    elif (oper == 'ls'):
        ip_port = get_data_channel_ip_port(sock)
        data_channel = open_data_channel(ip_port[0], ip_port[1])
        
        url = urlparse(p1)
        path = url[2]
        data = 'LIST ' + path + '\r\n'
        sock.sendall(bytes(data.encode()))
        message = sock.recv(4096)
        print(message)
        data_message = data_channel.recv(4096)
        print(data_message)
        data_channel.close()
    elif (oper == 'cp'):
        ip_port = get_data_channel_ip_port(sock)
        data_channel = open_data_channel(ip_port[0], ip_port[1])

        local_path = p1
        url = urlparse(p2)
        url_path = url[2]
        data = 'STOR ' + local_path + " " + url_path + '\r\n'
        print(data)
        sock.sendall(bytes(data.encode()))
        message = sock.recv(4096)
        print(message)
        data_message = data_channel.recv(4096)
        print(data_message)
        data_channel.close()
        
        

        



def run_operations(sock):
    while (True):
        # Parse command line 
        args = add_parser()
        oper = args.operation
        arg1 = args.param1

        if (args.param2):
            arg2 = args.param2
        
        if oper == 'quit':
            request_operation(sock, oper)
            break
        if oper == 'mkdir':
            url = arg1
            request_operation(sock, oper, url)
            break
        if oper == 'rmdir':
            url = arg1
            request_operation(sock, oper, url)
            break
        if oper == 'ls':
            url = arg1
            request_operation(sock, oper, url)
            break
        if oper == 'cp':
            local_path = arg1
            url_path = arg2
            request_operation(sock, oper, local_path, url_path)
            break


    

def main():
    # Connection Information
    port = 21
    host = "ftp.3700.network"

    # Connect and Log in into server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(15)
    sock.connect((host, port))
    sock.recv(4096)
    log_in(sock)
    
    # Configure
    configure(sock)
    
    # Operation Loop
    run_operations(sock)

if __name__ == '__main__':
  main()
        












