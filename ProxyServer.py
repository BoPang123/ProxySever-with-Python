import os
from socket import *

def GET(clientSocket,recvData):
    fileName =recvData.split()[1].split("//")[1].replace('/', '')
    print("receive message:"+recvData)
    print("fileName: " + fileName)
    filePath = "./" + fileName.split(":")[0].replace('.', '_')
    print("file Path:"+filePath)
    try:
        file = open(fileName, 'rb')
        print("File is found in proxy server.")
        responseMsg = file.read()
        clientSocket.sendall(responseMsg)
        print("Send, done.")
    except:
        print("File is not exist.\nSend request to server...")
        try:
            Sock = socket(AF_INET, SOCK_STREAM)
            serverName = fileName.split(":")[0]
            print("sever name :"+serverName)
            print("ip: "+gethostbyname(serverName))
            Sock.connect((serverName, 80))
            Sock.sendall(recvData.encode("UTF-8"))
            responseMsg = Sock.recv(4069)
            print("File is found in server.")
            clientSocket.sendall(responseMsg)
            print("Send, done.")
            # cache
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            cache = open(filePath + "./index.html", 'w')
            cache.writelines(responseMsg.decode("UTF-8").replace('\r\n', '\n'))
            cache.close()
            print("Cache, done.")
        except:
            print("Connect timeout.")
def PUT(clientSocket,recvData):
    fileName = recvData.split()[1].split("//")[1].replace('/', '')
    proxyClientSocket = socket(AF_INET, SOCK_STREAM)
    serverName = fileName.split(":")[0]
    proxyClientSocket.connect((serverName, 80))
    proxyClientSocket.sendall(recvData.encode("UTF-8"))
    responseMsg = proxyClientSocket.recv(4069)
    print(responseMsg)
def POST(clientSocket,recvData):
    fileName = recvData.split()[1].split("//")[1].replace('/', '')
    proxyClientSocket = socket(AF_INET, SOCK_STREAM)
    serverName = fileName.split(":")[0]
    proxyClientSocket.connect((serverName, 80))
    proxyClientSocket.sendall(recvData.encode("UTF-8"))
    responseMsg = proxyClientSocket.recv(4069)
    print(responseMsg)
def HEAD(clientSocket,recvData):
    print(recvData)
    header = "HTTP/ 1.1 200 OK\r\n\r\n"
    clientSocket.send(header.encode())
    print("HEAD method has been finished")
def DELETE(clientSocket,recvData):
    fileName=recvData.split()[1].replace('/','')
    print("fileName: " + fileName)
    filePath=fileName
    os.remove(filePath)
    print("Delected: "+ fileName)
def handleReq(clientSocket):
    # recv data
    # find the fileName
    # judge if the file named "fileName" if existed
    # if not exists, send req to get it
    recvData = clientSocket.recv(4096).decode()
    requestType = recvData.split(" ")[0]
    print("request type:"+requestType)
    if(requestType=="GET"):
        GET(clientSocket,recvData)
    elif(requestType=='PUT'):
        PUT(clientSocket,recvData)
    elif (requestType == 'DELETE'):
        DELETE(clientSocket,recvData)
    elif (requestType == 'POST'):
        POST(clientSocket,recvData)
    elif (requestType == 'HEAD'):
        HEAD(clientSocket,recvData)
    elif (requestType == 'CONNECT'):
        print(recvData)
        GET(clientSocket,recvData)
    else:
        print("No this type.")
        MAIN1()


def startProxy(port):
    proxyServerSocket = socket(AF_INET, SOCK_STREAM)
    proxyServerSocket.bind(("", port))
    proxyServerSocket.listen(5)
    while True:
        try:
            print("Proxy is waiting for connecting...")
            clientSocket, addr = proxyServerSocket.accept()
            print("Connect established")
            handleReq(clientSocket)
            clientSocket.close()
        except Exception as e:
            print("error: {0}".format(e))
            break
    proxyServerSocket.close()


def MAIN1():
    while True:
        try:
            port = int(input("choose a port number over 1024:"))
        except ValueError:
            print("Please input an integer rather than {0}".format(type(port)))
            continue
        else:
            if port <= 1024:
                print("Please input an integer greater than 1024")
                continue
            else:
                break
    startProxy(port)
def MAIN2():
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    port=input("choose a port number over 1024:")
    tcpSerSock.bind(('', int(port)))
    tcpSerSock.listen(3)
    while 1:
        print('Prepare to receive the response message from the client...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('Received a connection from：', addr)
        message = tcpCliSock.recv(4096).decode()
        print('The message sent by the client：', message)
        filename = message.split()[1].partition("//")[2].replace('/', '_')
        print('filename：', filename)
        fileExist = "false"
        try:
            print('The proxy server is checked for files：', filename)
            f = open(filename, "r")
            outputdata = f.readlines()
            fileExist = "true"
            print('The file exists on the proxy server')
            for i in range(0, len(outputdata)):
                tcpCliSock.send(outputdata[i].encode())
            print('Read from cache')
        except IOError:
            if fileExist == "false":
                print('The file is not in the proxy server, and the remote server is requested for a web page')
                c = socket(AF_INET, SOCK_STREAM)
                hostn = message.split()[1].partition("//")[2].partition("/")[0]
                print('Host Name: ', hostn)
                try:
                    c.connect((hostn, 80))
                    print('The socket connects to port 80 on the host')
                    c.sendall(message.encode())
                    buff = c.recv(4096)
                    tcpCliSock.sendall(buff)
                    tmpFile = open("./" + filename, "w")
                    tmpFile.writelines(buff.decode().replace('\r\n', '\n'))
                    tmpFile.close();
                except:
                    print("The proxy server failed to request a web page from the remote server")
            else:
                print('File exists, but IOError still occurs')
        print('Close the socket：tcpCliSock')
        tcpCliSock.close();
    print('Close the socket：tcpSerSock')
    tcpSerSock.close();


print("There are two ways to make a proxy" )
print("way 1: use wget and visit a website")
print("way 2: use the browser and get the html document\n")
way=input("Which way you want?  ")
if(way=="1"):
    MAIN1()
elif(way=="2"):
    MAIN2()
else:
    print("No this way")


    #wget https://lancaster.ac.uk/ -e use_proxy=yes -e http_proxy=10.129.133.17:8080
    #wget lancaster.ac.uk -e use_proxy=yes -e http_proxy=10.129.133.17:8080
    #wget csdn.net -e use_proxy=yes -e http_proxy=10.129.133.17:8080
    # wget youku.com -e use_proxy=yes -e http_proxy=10.129.133.17:8080
    # wget baidu.com -e use_proxy=yes -e http_proxy=10.130.39.200:8080
    #wget gov.cn -e use_proxy=yes -e http_proxy=10.130.39.200:8080
    #wget https://eternallybored.org -e use_proxy=yes -e http_proxy=10.130.39.200:8080
    #http://gaia.cs.umass.edu/wireshark-labs/INTRO-wireshark-file1.html