from socket import *
import sys
import os

if len(sys.argv) <= 1:
    print ('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start.
tcpSerSock.bind(("", 8888))
tcpSerSock.listen(5)
# Fill in end.

while 1:
    # Start receiving data from the client
    print ('\nReady to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('Received a connection from:', addr)
    # Fill in start. 
    message = tcpCliSock.recv(4096)
    # Fill in end.
    print("Message is: ",message)

    file = message.split()[1]

    # Extract the filename from the given message 
    print (file) 
    filename = message.split()[1].partition("/")[2] 
    print (filename) 
    fileExist = "false" 
    filetouse = "/" + filename 
    print (filetouse)

    filename = file.split('/')[1]
    file2 = message.split()[1].partition("/")[2]
    blackList = open("blacklist.txt", "r")

    flag = False
    for line in blackList.readlines():
        line = line.split('\n')[0]
        if line == file2:
            print("This URL is blocked")
            flag = True
            break

    blackList.close()

    if not flag:
        try:
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "r")
            outputdata = f.read()
            # ProxyServer finds a cache file and generates a response message
            tcpCliSock.sendall("HTTP/1.0 200 OK\r\n".encode())
            tcpCliSock.sendall("Content-Type:text/html\r\n".encode())

            #Fill in start.
            tcpCliSock.sendall("Content-Type: image/jpeg\r\n".encode())
            tcpCliSock.sendall("Content-Type: image/jpeg\r\n".encode())
            tcpCliSock.sendall(outputdata)
            f.close()
            #Fill in end.

            print ('Read from cache')
        # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
                # Create a socket on the proxyserver
                # Fill in start.
                 c = socket.socket(socket.AF_INET,socket. SOCK_STREAM)
                 # Fill in end.
                 file = file[1:]
                 hostn = file
                 hostn = file.replace("www.","",1)
                 print("hostname: ", hostn)

                 try:
                    # Connect to the socket to port 80
                    #File in start
                    print('connected to port 80')
                    fileobj = c.makefile('r',0)

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