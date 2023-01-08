import socket
import sys
import os

if len(sys.argv) <= 1:
    print ('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpSerSock.bind(("", 8888))
tcpSerSock.listen(2)
# Fill in start.
# Fill in end.
while 1:
    # Start receiving data from the client
    print ('\nReady to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('Received a connection from:', addr)
    message = tcpCliSock.recv(4096)
    print("MESSAGE RECIEVED IS ")

    flag = False

    if message.split()[1] is None:
        continue

    file = message.split()[1]

    fileExist = "false"
    filetouse = file
    print(filetouse)

    filename = file.split('/')[1]
    file2 = message.split()[1].partition("/")[2]
    URLf = open("blacklist.txt", "r")

    fileExist = "false"
    for line in URLf.readlines():
        line = line.split('\n')[0]
        if line == file2:
            print("This URL is blocked")
            flag = True
            break

    URLf.close()

    if not flag:
        try:
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "rb")
            outputdata = f.read()
            # ProxyServer finds a cache file and generates a response message
            tcpCliSock.sendall("HTTP/1.0 200 OK\r\n".encode())
            tcpCliSock.sendall("Content-Type:text/html\r\n".encode())
            tcpCliSock.sendall("Content-Type: image/jpeg\r\n".encode())
            tcpCliSock.sendall("Content-Type: image/jpeg\r\n".encode())

            tcpCliSock.sendall(outputdata)
            f.close()
            print ('Read from cache')

        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxyserver
                 c = socket.socket(socket.AF_INET,socket. SOCK_STREAM)
                 file = file[1:]
                 hostn = file
                 hostn = file.replace("www.","",1)
                 print("host NAME is : ", hostn)

                 try:
                    print('connected to port 80')
                    fileobj = c.makefile('rwb',0)
                    # Connect to the socket to port 80

                    if not "Referer" in message:
                        print("**************Connecting to server***********")
                        # Connect to the socket to port 80
                        c.connect((hostn, 80))
                        conneted=hostn
                        fileobj.write(b'GET / HTTP/1.0\r\n\r\n')
                    else:
                        print("********Get path in referer********: " + hostn)
                        c.connect((conneted, 80))
                        fileobj.write(b'GET /' + hostn + ' HTTP/1.0\r\n\r\n'.encode())

                    buffer = fileobj.read()
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile = open("./" + filename,"wb")
                    for i in range(0, len(buffer)):
                        tmpFile.write(buffer[i])

                    tcpCliSock.sendall("HTTP/1.0 200 OK\r\n".encode())
                    tcpCliSock.sendall("Content-Type:text/html\r\n".encode())
                    tcpCliSock.sendall("Content-Type: image/jpeg\r\n".encode())
                    tcpCliSock.sendall(buffer)
                    tmpFile.close()
                    print('cache saved')

                 except:
                     print ("Illegal request")

            else:
                 print("error 404")
                 tcpCliSock.sendall("HTTP/1.0 404 page not found\r\n".encode())
                 tcpCliSock.sendall("Content-Type:text/html\r\n".encode())

            tcpCliSock.close()
 # Fill in start.
tcpSerSock.flush()
tcpSerSock.close()
 # Fill in end.-