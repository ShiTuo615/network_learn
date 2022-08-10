from socket import *
import time

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

RTTList = []
RTTMin = float(1)
RTTMax = float(0)

maxTimes = int(input('please enter test times:'))
for i in range(1, maxTimes, 1):
    try:
        oldTime = time.time()
        sendTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(oldTime))
        message = 'package %d, client local time:%s' %(i +1, sendTime)

        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, severAddress = clientSocket.recvfrom(2048)
        rtt = time.time() - oldTime
        RTTList.append(rtt)
        RTTMax = max(rtt, RTTMax)
        RTTMin = min(rtt, RTTMin)
        print("ping %d %s RTT:%f" %(i + 1, modifiedMessage.decode(), rtt))
    except Exception as e:
        print('Request timed out')
        print('error is %s' %str(e))
print("\n>> Summary: RTT Min: %f, RTT MAX: %f, RTT Mean: %f" % (RTTMin, RTTMax, sum(RTTList)/len(RTTList)))
clientSocket.close()        
