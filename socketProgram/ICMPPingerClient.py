from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    
    while count < countTo:
        thisVal = ord(chr(string[count+1])) * 256 + ord(chr(string[count]))
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(string):
        csum = csum + ord(chr(string[len(string) - 1]))
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while True:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == [] : # timeout
            return "Request timed out"

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        #fill in start
        #Fetch the ICMP header from the IP packet
        header = recPacket[20:28]
        header_type, header_code, header_checksum, header_packet_ID, header_sequence =struct.unpack("bbHHh", header)

        if header_type != 0 or header_code != 0 or header_packet_ID != ID or header_sequence != 1 :
            if header_type == 3 and header_code == 0 :
                return "目的网络不可达"
            if header_type == 3 and header_code == 1 :
                return "目的主机不可达"
            if header_type == 3 and header_code == 2 :
                return "目的协议不可达"
            if header_type == 3 and header_code == 3 :
                return "目的端口不可达"
            if header_type == 3 and header_code == 6 :
                return "目的网络未知"
            if header_type == 3 and header_code == 7 :
                return "目的主机未知"
            if header_type == 4 and header_code == 0 :
                return "源抑制"
            if header_type == 12 and header_code == 0 :
                return "IP首部损坏"
            return "Request error."       

        #fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <=0:
            return "Request timed out"
        return howLongInSelect


def sendOnePing(mySocket, destAddr, ID):
    #header is type(8), code(8), checksum(16), id(16), sequence(16)

    myChecksum = 0

    #make a dummy header with a 0 checksum
    #struct --- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    # bytes_In_double = struct.calcsize("d")
    # data = (192 - bytes_In_double) * "Q"
    # data = struct.pack("d", time.time()) + bytes(data.encode('utf-8'))
    data = struct.pack("d", time.time())

    #caculate the checksum on the data and the dummy header
    #例子里面写错了，这里不能转成str再算校验和，而要在里面把每个byte转成char来算，才行
    myChecksum = checksum(header + data)

    #get the right checksum, and put in the header
    if sys.platform == 'darwin':
        #covert 16-bit intefers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")

    # sock_raw is a powerful socket type, for more detail: http://sock-raw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF

    sendOnePing(mySocket, destAddr, myID)
    
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay



def ping(host, timeout = 3):
    dest = gethostbyname(host)
    print("Pinging " + dest + " using python:")
    print("")
    #send ping requests to a server separated by approximately one second
    while True:
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)
    return delay

ping("baidu.com")