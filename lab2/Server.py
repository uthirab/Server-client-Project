#Name: Uthira Baskaran
#Student ID :1001573527

import socket
import threading
from tkinter import *

class MyServer(object):
    def __init__(self, host):
        self.socketnolist = []                                              # list to store socket numbers
        self.host = host                                                    # host
        self.port = 1337                                                    # port no
        self.servsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # connect server
        self.servsoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsoc.bind((self.host, self.port))                           # bind server
        self.usernames = []                                                 # empty list for username records
        self.state = {}                                                     # dictionary list to store the states
        threading.Thread(target=self.clientalking).start()                  # thread to start receiving client message

    def newframe(self,root):                                                #creates GUI
        self.gui = root
        self.gui.title("Server")                                            #title for the gui
        fr = Frame(self.gui, width=200, height=200)                         # creates frame
        fr.pack(side=LEFT, padx=25, pady=25)
        scroll_bar1 = Scrollbar(fr)
        scroll_bar1.pack(side=RIGHT, fill=Y)
        self.text_box = Text(fr, height=20, width=40, yscrollcommand=scroll_bar1.set)  #creates screen for the display
        self.text_box.pack(side=LEFT, fill=Y)

    def BroadCastAllData(self, message):                                    # function to send the message to all clients
        for S_list in Client_server_list:
            if S_list != self.servsoc:                                      # if it is not the socket  message is sent to all the client
                try:
                    S_list.sendall(message)                                 # send all data at once
                except:                                                     # Connection was closed.
                    S_list.close()
                    Client_server_list.remove(S_list)

    def status(self,message, c_name):                                       # Function to update the status of participants
        name = c_name
        msg = message.split(':')                                            # Splits the status from other content
        self.state.update({name:msg[4]})                                    # update the dictionary with the current status


    def client_name(self, address):                                         # to map client
        for i in range(len(self.socketnolist)):
            if address == self.socketnolist[i]:                             # if the current address matches with list , the index is taken
                self.c_name = self.usernames[i]                             # index is used to match with username list
                return self.c_name

    def dictstate(self,d):                                                  # initialize the INIT state at the beginign
        if len(self.state)<=3:                                              # only the participant's status is updated
            self.state[d]=['Init']
            print(self.state)

    def clientname(self, client):                                           # to get the client name from user
        client.send("Enter user name(upto 8 character)".encode())
        username = client.recv(4096)                                        # receive client name from client
        username = username.decode()
        a,d = str(username).split(']')                                      #split user name from other content
        if len(d) <= 8:                                                     #checking if the length is lesser than equal to 8
            self.usernames.append(d)                                        #appending username to the list
            self.text_box.insert(END, d + '\n')
        else:
            client.send(("User Name too big. Give user name 1-8 character long").encode())
            username = client.recv(4096)                                    #receive client new user name
            username = username.decode()
            a,d = str(username).split(']')
            if len(d) <= 8:
                self.usernames.append(d)
                self.text_box.insert(END, d + '\n')
                print(d)
            self.dictstate(d)                                               #updates the key of the dictonary function

    def clientalking(self):                                                 #connecting to client
        self.servsoc.listen(5)                                              #socket listens and the buffer is 4
        Client_server_list.append(self.servsoc)                             #add the server to the list
        while True:
            client, address = self.servsoc.accept()                         #client and socket number are stored in 2 variable
            Client_server_list.append(client)                               #add client to list
            cood = client.recv(4096)
            coodde = cood.decode()                                          # server discovers the coordinator
            if "coordinator" in coodde:
                self.text_box.insert(END, "Coordinator Discovered" + '\n')
            self.clientname(client)                                         #call function clientname to get the client name from user
            self.socketnolist.append(address[1])                             #store the socket numbers in a list
            print("Server started!")
            c_name = self.client_name(address[1])                           #figure out client the client name
            self.text_box.insert(END, "\rClient ({0}) connected".format(c_name) + '\n')
            self.BroadCastAllData("Client ({0}) entered room\n".format(c_name).encode()) #send all the client that a client has entered
            threading.Thread(target=self.ClientDataReceiving, args=(client, address)).start()   #start thread to receive data from client

    def http(self, response):                                               #function to print everything it receives to the gui
        b = response
        if b != "log off":                                                  #check if the client is not loggin off
            string,http=b.split('[')
            self.text_box.insert(END, str(http) + '\n')

    def clientlogof(self, response, c_name):                                #function to close the client
        r = response
        if r != "log off":                                                  #continue if the client is not logging off
            pass
        else:                                                               #if the client is logging off
            try:
                self.BroadCastAllData(("\rClient ({0}) is offline\n".format(c_name).encode()))  #send info to other clients
                self.text_box.insert(END, "\rClient ({0}) is offline\n".format(c_name) + '\n')
                Client_server_list.remove(socket)                                               #remove the socket from the list
            except Exception as msg:                                                            #catch exception and print it
                self.text_box.insert(END, msg + '\n')

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
                    a = str(response).split(']')                            # splits the message from HTTP content
                    r= str(a[0]).split('[')
                    message=r[0]+a[1]
                    if 'State:' in message:                                 #receiving state information from client and updating the dictionary
                        self.status(message,c_name)
                    elif 'status' in message:                               # if the participant request to know about the status of other participants
                        for x in self.state:
                            r= x+' Status:'+self.state[x]+'\n'             #it prints the participants status to other participants
                            print(r)
                            self.BroadCastAllData(r.encode())
                    else:
                        message1 = "\r[{}]: {}".format(c_name, message)         #message formart
                        self.text_box.insert(END, message1 + '\n')
                        q = open("log.txt", 'a+')                               #to append the message in file
                        q.write(message1)
                        q.close()
                        self.BroadCastAllData(message1.encode())                 #to send mesage to everyone
                else:
                    raise socket.error('Client got Disconnected')           #client disconnected
            except Exception as msg:                                        #when Error happens and client got disconnected
                c_name = self.client_name(address[1])                       #get the client name
                self.text_box.insert(END,"\rClient {0} disconnected.".format(c_name)+ '\n')
                self.BroadCastAllData(("\rClient ({0}) is offline\n".format(c_name).encode()))  #send it to everyone
                self.text_box.insert(END, "\rClient ({0}) is offline\n".format(c_name) + '\n')
                client.close()                                              #close the client
                Client_server_list.remove(socket)                           #remove the client from the list
                return

Client_server_list = []                                                 # list to store client details
gui = Tk()                                                              # initialize the gui
tServer = MyServer(' ')                                                 # open the class
tServer.newframe(gui)
mainloop()
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

