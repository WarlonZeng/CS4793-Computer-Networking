from socket import *
import ssl
import base64
#from email.mime.image import MIMEImage
#from email.mime.multipart import MIMEMultipart
#import os

def main():
    msg = '\r\n I love computer networks!'
    endmsg = '\r\n' + "." + '\r\n'
    mailserver = 'smtp.gmail.com'
    myEmail = 'example@gmail.com'
    myPassword = 'example'
    targetEmail = 'example@gmail.com'

    clientSocket = socket(AF_INET, SOCK_STREAM);
    clientSocket.connect((mailserver, 587))
    recv = clientSocket.recv(1024)
    print recv
    if recv[:3] != '220':
        print '220 reply not received from server.'

    heloCommand = 'HELO smtp.google.com\r\n'
    clientSocket.send(heloCommand)
    recv = clientSocket.recv(1024)
    print recv
    if recv[:3] != '250':
        print '250 reply not received from server.'

    command = "STARTTLS\r\n" #tls
    clientSocket.send(command)
    recv = clientSocket.recv(1024)
    print recv
    if recv[:3] != '220':
        print '220 reply not received from server.'
    
    secureClientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
    secureClientSocket.send('auth login\r\n') #auth
    recv = secureClientSocket.recv(1024)
    print recv
    if recv[:3] != '334':
        print '334 reply not received from server.'

    secureClientSocket.send(base64.b64encode(myEmail)+'\r\n')
    recv = secureClientSocket.recv(1024)
    print recv
    if recv[:3] != '334':
        print '334 reply not received from server.'
        
    secureClientSocket.send(base64.b64encode(myPassword)+'\r\n')
    recv = secureClientSocket.recv(1024)
    print recv
    if recv[:3] != '235':
        print '235 reply not received from server.'

    for i in range (0, 5):   
    #Send MAIL FROM command and print server response.
        secureClientSocket.send('MAIL FROM: <' + myEmail + '>\r\n')
        recv = secureClientSocket.recv(1024)
        print recv
        if recv[:3] != '250':
            print '250 reply not received from server.'

    #Send RCPT TO command and print server response.
        secureClientSocket.send('RCPT TO: <' + targetEmail + '>\r\n')
        recv = secureClientSocket.recv(1024)
        print recv
        if recv[:3] != '250':
            print '250 reply not received from server.'

    #Send DATA command and print server response.
        secureClientSocket.send('DATA\r\n')
        recv = secureClientSocket.recv(1024)
        print recv
        if recv[:3] != '354':
            print '354 reply not received from server.'

    #Send message data.
        secureClientSocket.send(('Subject: SMTP Google Server Testing' + '\r\n'))
        secureClientSocket.send(('From: ' + myEmail + '\r\n'))
        secureClientSocket.send(('To: ' + targetEmail + '\r\n'))
        secureClientSocket.send(msg)
    
    #Message ends with a single period.
        secureClientSocket.send(endmsg)
        recv = secureClientSocket.recv(1024)
        print recv
        if recv[:3] != '250':
            print '250 reply not received from server.'

    #Send QUIT command and get server response.
    secureClientSocket.send('QUIT\r\n')
    secureClientSocket.close()

    print "successful mail"

    pass

main()
