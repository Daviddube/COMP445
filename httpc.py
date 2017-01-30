import socket
import argparse
import sys

def httpc():
    conn = socket.create_connection(('httpbin.org', 80))
    try:
        line = 'GET /status/418 HTTP/1.0\nHost: httpbin.org\n\n'
        request = line.encode("utf-8")
        conn.sendall(request)
        # MSG_WAITALL waits for full request or error
        response = conn.recv(1000, socket.MSG_WAITALL)
        sys.stdout.write("Replied: " + response.decode("utf-8"))
    finally:
        conn.close()
            




#parser = argparse.ArgumentParser()
#parser.add_argument("-v", help="verbose")
#parser.add_argument("-d", help="server port", type=int, default=8007)
#args = parser.parse_args()
httpc()