from asyncio.windows_events import NULL
from http import server
from http.server import BaseHTTPRequestHandler
from io import BytesIO
from socket import *
import sys
import os
from http import *

#测试网址：http://gaia.cs.umass.edu/wireshark-labs/INTRO-wireshark-file1.html
#设置代理，参见这个https://blog.csdn.net/m0_67392010/article/details/124459780
def makeHttpRequest(request):
    fields = request.split("\r\n")
    fields = fields[1:]
    output = {}
    for field in fields:
        if (field == '' or field =='\r\n' or field == '\r\n\r\n'):
            continue
        key,value = field.split(':', 1)
        output[key] = value
    return output

#if len(sys.argv) <= 1:
#    print('Usage : "Python ProxyServer.py server_ip: It is the IP address of Proxy Server')
#    sys.exit(2)

#create a server socket, bind it to a port and start listening
serverPort = 1200
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', serverPort))
tcpSerSock.listen(1)
message = ''

while True:
    #Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    output = makeHttpRequest(message)
    #不让除了测试地址以外的进来处理
    if output.get('Host') is NULL or output.get("Host").strip() != 'gaia.cs.umass.edu' :
        continue
    #Extract the filname from the given message
    print('a message from client: ' , message)
    filename = message.split()[1].partition("//")[2]
    print('filename is: ', filename)
    fileExist = "false"
    filetouse = "/" + filename
    print("filetouse is: ", filetouse)
    try:
        #check wether the file exist in the cache
        f = open("WEB/" + filetouse, encoding='utf-8')
        outputdata = f.read()
        f.close()
        fileExist = "true"
        #ProxyServer finds a chche hit and generate a response message
        header = 'HTTP/1.0 200 OK\r\nConnection: close\r\nContent-Type: text/html\r\nContent-Length: %d\r\n\r\n' % len(outputdata.encode())
        tcpCliSock.send(header.encode())
        tcpCliSock.send(outputdata.encode())
        print('Read from cache')
    #Error handling for file not found in cache
    except IOError as e:
        if fileExist == "false":
            #create a socket on the proxyServer
            print('creating socket on proxyServer')
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.","", 1)
            print("hostn is: ", hostn)
            try:
                #connect to the socket to port 80
                serverName = hostn.partition("/")[0]
                c.connect((serverName, 80))
                #create a temporary file on this cocket and ask port 80 for the file requestd by the client
                fileobj = c.makefile('rwb', 0)
                fileobj.write(message.encode())
                #read the response into buffer
                serverResponse = fileobj.read()
                #create a new file in the chache for the request file
                #Also send the response in the buffer to client socket and the corresponding file in the cache
                filename = "WEB/" + filename
                filesplit = filename.split("/")
                for i in range(0, len(filesplit) - 1):
                    if not os.path.exists("/".join(filesplit[0:i+1])):
                        os.makedirs("/".join(filesplit[0:i+1]))
                tmpFile = open(filename, "wb")
                serverResponse = serverResponse.split(b'\r\n\r\n')[1]
                print("serverResponse is: ",serverResponse)
                tmpFile.write(serverResponse)
                tmpFile.close()
                tcpCliSock.send("HTTP/1.1 200 OK/r/n".encode())
                tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
                tcpCliSock.send(serverResponse)
            except Exception as e:
                print('Illegal request')
            c.close()
        else:
            # Http response message for file not found
            print("ENT ERROR")
        #close the client and the server socket
    tcpCliSock.close()
tcpSerSock.close()