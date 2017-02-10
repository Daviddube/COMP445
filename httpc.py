import socket
import argparse
import sys

def httpc(method, URL, header, verbose, inline, file, o):
    
    host = URL.split('/')[0]

    conn = socket.create_connection((host, 80))
    
    try:
        path = ''
        if len(URL.split('/')) > 1:
            count = 0
            for i in URL.split('/'):
                if count != 0:
                    path += '/' + URL.split('/')[count]
                count += 1
        print(args)
        print(path)
        if method == 'get':
            line = 'GET ' + path + ' HTTP/1.0\nHost: ' + host + '\n\n'
            if header:
                for i in header:
                    line += i + '\n'
        elif method == 'post':
            line = 'POST ' + path + ' HTTP/1.0\nHost: ' + host + '\n'
            if header:
                for i in header:
                    line += i + '\n'
            if inline and file:
                sys.exit(1)
            if inline:
                #add the content length
                line+= 'Content-length:' + str(len(inline)) + '\n'
                line += '\n'
                line += inline + '\n'
            if file:
                with open(file) as f:
                    line += f.readlines()
            line += '\n'
        print('Line' + line)
        request = line.encode("utf-8")
        conn.sendall(request)
        # MSG_WAITALL waits for full request or error
        response = conn.recv(1000, socket.MSG_WAITALL)
        if o is not None:
            with open(o, "a+") as f:
                if verbose:
                    f.write(response.decode("utf-8"))
                else:
                    f.write(response.decode("utf-8").split("\r\n\r\n")[1])
        else:
            if verbose:
                sys.stdout.write("Replied: " + response.decode("utf-8"))
            else:
                sys.stdout.write("Replied: " + response.decode("utf-8").split("\r\n\r\n")[1])

    finally:
        conn.close()
            




parser = argparse.ArgumentParser()
parser.add_argument("method", nargs="?", help="post argument")
parser.add_argument("-v", dest="verbose", action="store_true", help="verbose")
parser.add_argument("-u", action="append", dest="header", help="header")
parser.add_argument("--d", nargs="?", dest="inline", help="verbose")
parser.add_argument("-f", nargs="?", dest="file", help="verbose")
parser.add_argument("URL", help="server host")
parser.add_argument("-o", nargs="?", dest="o", help="write response in file")
args = parser.parse_args()
httpc(args.method, args.URL, args.header, args.verbose, args.inline, args.file, args.o)