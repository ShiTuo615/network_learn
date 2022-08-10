from socket import *
import sys

clientSocket = socket(AF_INET, SOCK_STREAM)
ServerPort = 1200
ServerName = '127.0.0.1'
clientSocket.connect((ServerName, ServerPort))

header = 'GET /HelloWorld.html HTTP/1.1\r\nHost: %s:%s\r\nConnection: close\r\n +\
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36\r\n +\
    Accept-Language: zh-CN\r\n\r\n' %(ServerName, ServerPort)
clientSocket.send(header.encode())
data = clientSocket.recv(10000)
print(data.decode())
data = clientSocket.recv(10000)
print(data.decode())
#有关于怎么写文档的见https://blog.csdn.net/qq_41286751/article/details/121574764
with open('response.html', 'wb+') as f:
    f.write(data)
clientSocket.close()