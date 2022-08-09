import random
from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverPort = 12000
serverSocket.bind(('', serverPort))

while True:
    try:
        rand = random.randint(0, 10)
        message, address = serverSocket.recvfrom(1024)
        message = message.upper()

        if rand < 4:
            continue
        serverSocket.sendto(message, address)
    except Exception as e:
        print('error is %s' %str(e))
