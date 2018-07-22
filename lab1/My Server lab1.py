#Name: Uthira Baskaran
#Student ID :1001573527

import socket
import threading
import datetime


class MyServer(object):
    def __init__(self, host, port):
        self.host = host                                                    #host
        self.port = port                                                    #port no
        self.servsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #connect server
        self.servsoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsoc.bind((self.host, self.port))                           #bind server
        self.usernames = []                                                 #empty list for username records
        print("Do you want to retrieve the Old conversation? yes/no?")      #to print the past conversation
        if input() == 'yes':                                                #if we want the past conversation
            with open("log.txt") as q:                                      #open the file
                for line in q:
                    print(line)                                             #print everyline

    def BroadCastAllData(self, message):                                    # function to send the message to all clients
        for S_list in Client_server_list:
            if S_list != self.servsoc:                                      # if it is not the socket  message is sent to all the client
                try:
                    S_list.sendall(message)                                 # send all data at once
                except:                                                     # Connection was closed.
                    S_list.close()
                    Client_server_list.remove(S_list)

    def client_name(self, address):                                         #to map client
        for i in range(len(socketnolist)):
            if address == socketnolist[i]:                                  # if the current address matches with list , the index is taken
                self.c_name = self.usernames[i]                             # index is used to match with username list
                return self.c_name

    def clientname(self, client):                                           # to get the client name from user
        client.send("Enter user name(upto 8 character)".encode())
        username = client.recv(4096)                                        # receive client name from client
        username = username.decode()
        a, b, c, d = str(username).split(':')                               #split user name from other content
        if len(d) <= 8:                                                     #checking if the length is lesser than equal to 8
            self.usernames.append(d)                                        #appending username to the list
        else:
            client.send(("User Name too big. Give user name 1-8 character long").encode())
            username = client.recv(4096)                                    #receive client new user name
            username = username.decode()
            a, b, c, d = str(username).split(':')
            if len(d) <= 8:
                self.usernames.append(d)
                print(d)

    def clientalking(self):                                                 #connecting to client
        self.servsoc.listen(4)                                              #socket listens and the buffer is 4
        Client_server_list.append(self.servsoc)                             #add the server to the list
        while True:
            client, address = self.servsoc.accept()                         #client and socket number are stored in 2 variable
            Client_server_list.append(client)                               #add client to list
            self.clientname(client)                                         #call function clientname to get the client name from user
            socketnolist.append(address[1])                                 #store the socket numbers in a list
            print("Server started!")
            c_name = self.client_name(address[1])                           #figure out client the client name
            print("\rClient ({0}) connected".format(c_name))
            self.BroadCastAllData("Client ({0}) entered room\n".format(c_name).encode()) #send all the client that a client has entered
            threading.Thread(target=self.ClientDataReceiving, args=(client, address)).start()   #start thread to receive data from client

    def http(self, response):                                               #function to print http
        b = response
        if b != "log off":                                                  #check if the client is not loggin off
            l1 = 'GET/client.http\r\n ' \
                 'Host: 10.219.139.223\r\n ' \
                 'User-Agent:/pycharm\r\n ' \
                 'Content-Type:Text\r\n'
            l2 = ' Content-Length:'                                          #variable containing all the detail
            l3 = ' date : '
            date = str(datetime.datetime.now()) + str('\r\n')               #get current date
            c1 = str(len(b))                                      #it gets size of the message received from client
            http = l1 + l2 + c1 + str('\r\n') + l3 + date + b + str('\n')   #concat the total http message
            print(str(http))                                                #print the http

    def clientlogof(self, response, c_name):                                #function to close the client
        r = response
        if r != "log off":                                                  #continue if the client is not logging off
            pass
        else:                                                               #if the client is logging off
            try:
                self.BroadCastAllData(("\rClient ({0}) is offline\n".format(c_name).encode()))  #send info to other clients
                print("\rClient ({0}) is offline\n".format(c_name))
                Client_server_list.remove(socket)                                               #remove the socket from the list
            except Exception as msg:                                                            #catch exception and print it
                print(msg)

    def ClientDataReceiving(self, client, address):                         #function to receive data from the client
        print("Listening to Client")
        while True:                                                         # keep running to receive messages from client
            try:
                mes = client.recv(4096)                                     # receive data from client
                if mes:                                                     #checks if  there is any message
                    response = mes.decode()
                    c_name = self.client_name(address[1])                   #to get the client name that is stored
                    self.clientlogof(response, c_name)                      #to check if the client is logging off
                    self.http(response)                                     # to print in http format
                    message = "\r[{}]: {}".format(c_name, mes.decode())     #message formart
                    print(message, end="")                                  #to print the messaage in server console
                    print("\nThread number={}\n".format(threading.get_ident()))         #printing thread no to show thread
                    q = open("log.txt", 'a+')                               #to append the message in file
                    q.write(message)
                    q.close()
                    self.BroadCastAllData(message.encode())                 #to send mesage to everyone
                else:
                    raise socket.error('Client got Disconnected')           #client disconnected
            except Exception as msg:                                        #when Error happens and client got disconnected
                c_name = self.client_name(address[1])                       #get the client name
                print("\rClient {0} disconnected.".format(c_name))
                self.BroadCastAllData(("\rClient ({0}) is offline\n".format(c_name).encode()))  #send it to everyone
                print("\rClient ({0}) is offline\n".format(c_name))
                client.close()                                              #close the client
                Client_server_list.remove(socket)                           #remove the client from the list
                return
if __name__ == "__main__":
    Client_server_list = []                                                 # list to store client details
    socketnolist = []                                                       # list to store socket numbers
    portno = 1337                                                           #port number
    tServer = MyServer(' ', portno)                                         #open the class
    tServer.clientalking()                                                  #start the function clienttalking


#https://stackoverflow.com/questions/31080499/python-socket-running-server-and-client-from-the-same-pc
#http://www.bogotobogo.com/python/python_network_programming_server_client.php
#https://www.binarytides.com/code-chat-application-server-client-sockets-python/
#https://github.com/metonimie/python-networking/blob/master/chat/tcp_client.py
#https://github.com/metonimie/python-networking/blob/master/chat/tcp_server.py
#http://codingnights.com/coding-fully-tested-python-chat-server-using-sockets-part-1/
#https://www.geeksforgeeks.org/simple-chat-room-using-python/
#https://www.binarytides.com/python-socket-programming-tutorial/
#https://www.binarytides.com/category/programming/sockets/python-sockets-sockets/
#https://stackoverflow.com/questions/26445331/how-can-i-have-multiple-clients-on-a-tcp-python-chat-server
#https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
#https://www.python-course.eu/tkinter_text_widget.php
#http://danielhnyk.cz/simple-server-client-aplication-python-3/
#http://docs.python-requests.org/en/master/user/quickstart/
#http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
#https://www.python-course.eu/python_tkinter.php
#http://sebsauvage.net/python/gui/
#http://www.sfentona.net/?p=2239
#https://stackoverflow.com/questions/42976749/python-3-6-multithread-tcp-echo-server-for-more-than-one-client
#https://stackoverflow.com/questions/36060346/creating-a-simple-chat-application-in-python-sockets
#https://stackoverflow.com/questions/23507779/python-network-threading-simple-chat-waits-for-user-to-press-enter-then-gets-me
#https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
#https://stackoverflow.com/questions/20745352/creating-a-multithreaded-server-using-socketserver-framework-in-python

