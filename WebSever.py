import socket
import threading
def handleRequest(tcpSocket):
    # 1. Receive request message from the client on connection socket
    requestData = tcpSocket.recv(1024)
    # 2. Extract the path of the requested object from the message (second part of the HTTP header)
    requestList = requestData.decode().split("\r\n")
    reqHeaderLine = requestList[0]
    print("request line: " + reqHeaderLine)
    fileName = reqHeaderLine.split(" ")[1].replace("/", "")
    print("fileName: " + fileName)
    #  3. Read the corresponding file from disk
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    try:
        file = open("./" + fileName, 'rb')  # read the corresponding file from disk
        # 4. Store in temporary buffer
        content = file.read().decode()  # store in temporary buffer
        file.close()
        resHeader = "HTTP/1.1 200 OK\r\n" + \
                    "Server: " +myaddr+"\r\n"+ "\r\n"
        response = (resHeader + content).encode(encoding="UTF-8")  # send the correct HTTP response
    except FileNotFoundError:
        content = "SORRY!\n   404 NOT FOUND\n"
        resHeader = "HTTP/1.1 404 Not Found\r\n" + \
                    "Server:  " +myaddr+"\r\n"+ "\r\n"
        response = (resHeader + content).encode(encoding="UTF-8")  # send the correct HTTP response error
        # 5. Send the correct HTTP response error
        tcpSocket.sendall(response)
    # 6. Send the content of the file to the socket
    else:
        tcpSocket.sendall(response)
    # 7. Close the connection socket
    tcpSocket.close()
    print("Done\n")
    print("wait for connecting...")


def startServer(serverAddress, serverPort):
    # 1. Create server socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 2. Bind the server socket to server address and server port
    serverSocket.bind((serverAddress, serverPort))
    # 3. Continuously listen for connections to server socket
    serverSocket.listen(0)
    # 4. When a connection is accepted, call handleRequest function, passing new connection socket
    print("wait for connecting...")
    while True:
        try:
            Sock, clientAddr = serverSocket.accept()
            print("one connection is established, ", end="")
            print("address is: %s" % str(clientAddr))
            handleThread = threading.Thread(target=handleRequest, args=(Sock,))
            handleThread.start()
        except Exception as error:
            print(error)
            break
    #  5. Close server socket
    serverSocket.close()


if __name__ == '__main__':
    while True:
        try:
            hostPort = int(input("Input the port you want: "))
            startServer("", hostPort)
            break
        except Exception as e:
            print(e)
            continue
    # http://10.129.133.17:8080/index.html
    # wget 10.129.133.17:8080/index.html
    #10.129.139.237:8082/index.html