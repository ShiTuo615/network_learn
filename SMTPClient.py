from socket import *
import base64

subject = "I Love U"
contentType ="text/plain"
msg = "\r\n I Love U"
endMsg = "\r\n.\r\n"

mailServer = "smtp.qq.com"

fromAddress = "846705130@qq.com"
toAddress = "846705130@qq.com"
#端口要用这个，这个是帮助文档里的端口，不是一般的smtp端口
fromPort = 587

#qq邮箱的smtp只能用授权码来代替密码
fromAddressPwd = "drszisjwfcpzbbfj"

userName = base64.b64encode(fromAddress.encode())
passwd = base64.b64encode(fromAddressPwd.encode())

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, fromPort))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

heloCommand = "HELO ALICE\r\n"
clientSocket.send(heloCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

#Auth
clientSocket.send('AUTH LOGIN\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

#密码和用户名要用base64加密后的发送
clientSocket.send((userName +'\r\n'.encode()))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server.')

clientSocket.send((passwd +'\r\n'.encode()))
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '235':
    print('235 reply not received from server.')


#Send email
MailFromCommand = "MAIL FROM: <" + fromAddress + ">\r\n"
clientSocket.sendall(MailFromCommand.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

#Send RCPT
RcptTO = 'RCPT TO: <' + toAddress + '>\r\n'
clientSocket.sendall(RcptTO.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

#Send Data
Data = 'DATA\r\n'
clientSocket.send(Data.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '354':
    print('354 reply not received from server.')

#Send message data
Message = 'from:' + fromAddress +'\r\n'
Message += 'to:' + toAddress +'\r\n'
Message += 'subject:' + subject +'\r\n'
Message += 'Content-Type:' + contentType + '\r\n'
Message += msg
clientSocket.sendall(Message.encode())

#fill in end
clientSocket.sendall(endMsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server.')

QuitMsg = 'QUIT'
clientSocket.send(QuitMsg.encode())

clientSocket.close()