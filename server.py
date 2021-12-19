import socket
from datetime import datetime
import threading
import logging
from settings import *
import os
import pathlib
from settings import  *

ROOT_DIR = os.path.abspath(os.getcwd())
FILES_DIR = 'files'

def main():
    log_setup()
    initial_port = 80
    with socket.socket() as s:
        try:
            while True:
                if is_free_port(initial_port):
                    print(f"Using port {initial_port}")
                    s.bind(('', initial_port))
                    break
                else:
                    initial_port=+1
        except OSError:
            s.bind(('', 8080))
            print("Using port 8080")
        else:
            s.listen(5)
            while True:
                conn, addr = s.accept()
                print("Connected",addr)
                threading.Thread(target=connection, args=[conn, addr]).start()

def is_free_port(port):
    sock = socket.socket()
    sock.settimeout(3)
    try:
        sock.bind(('', port))
    except:
        return False
    else:
        return True
    finally:
        sock.close()

def connection(conn, addr):
    with conn:
        data = conn.recv(REQUEST_LENGTH)
        if data == b"":
            conn.close()
        request = data.decode()
        print(request)
        resp, content = response(request, addr)

        conn.sendall(resp.encode() + content)

def response(conn, addr):
    try:
        file = conn.split('\n')[0].split()[1][1:]
    except:
        file = 'index.html'
    if not file:
        file = 'index.html'
    if os.path.exists(ROOT_DIR + os.sep + FILES_DIR+ os.sep + file):
        dir_file = pathlib.Path(FILES_DIR, file)
        file_type = file.split(".")[-1]
        if file_type in ALLOWED_FORMATS:
            code = '200'
            data= open_file(dir_file)
            size = os.path.getsize(dir_file)
            response = get_response(file_type, code, size)
        else:
            code = '403'
            file = "403.html"
            file_type = file.split(".")[-1]
            data = open_file(dir_file)
            size = os.path.getsize(dir_file)
            response = get_response(file_type, code,size)
    else:
        code = '404'
        file = "404.html"
        dir = pathlib.Path(FILES_DIR, file)
        file_type = file.split(".")[-1]
        data = open_file(dir)
        size = os.path.getsize(dir)
        response = get_response(file_type, code,size)

    log(code, addr, file)
    return response, data

def log(error_number, addr, file):
    logging.info(f"""Date {get_date()} IP-address: {addr} File path: {file} Code: {error_number} """)

def log_setup():
    logging.basicConfig(
    level = logging.INFO,
    handlers = [
                   logging.FileHandler('server.log', encoding='UTF-8'),
                   logging.StreamHandler(),
               ],

    )

def open_file(file):
    with open(file, "rb") as f:
        data = f.read()
    return data

def get_date():
    return datetime.now()

def get_response(file_type, code, size):
    return f"""HTTP/1.1 {code} {CODES[code]}
    Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GTM')}
    Server: WebServer
    Content-Type: {TYPES[file_type]}
    Content-Length: {size*2}
    Connection: close\n\n"""


if __name__ == '__main__':
    main()