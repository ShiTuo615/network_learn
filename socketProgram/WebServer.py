from fileinput import filename
from socket import *
import sys
import threading

def webProcess(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        print(message)
        filename = message.split()[1]
        f = open(filename[1:], encoding='utf-8')
        outputdata = f.read()
        #注意这里，长度一定要填，而且要是encode()以后的长度，不然对不上的，长度不填，html标签之间就必须隔一行空格。。。还有结尾这里是\r\n\r\n
        header = 'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Type: text/html\r\nContent-Length: %d\r\n\r\n' % len(outputdata.encode())
        connectionSocket.send(header.encode())
        connectionSocket.send(outputdata.encode())
        # for i in range(0, len(outputdata)):
        #     print(outputdata[i])
        #     connectionSocket.send(outputdata[i].encode())
        # connectionSocket.send("\n".encode())
        connectionSocket.close()
    except IOError:
        header = 'HTTP/1.1 404 Not Found'
        connectionSocket.send(header.encode())
        connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 1200
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Ready to serve...')
while True:
    connectionSocket, addr = serverSocket.accept()
    thread = threading.Thread(target=webProcess, args=(connectionSocket,))
    thread.start()

serverSocket.close()
sys.exit()    