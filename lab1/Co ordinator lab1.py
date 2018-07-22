#Name: Uthira Baskaran
#Student ID :1001573527

import socket
import datetime
from tkinter import *
from threading import Thread
from threading import Timer

class MyClient():                                                                       #my client class
    def __init__(self, root):                                                           #initial function and store the value
        self.gui = root
        self.newframe()

    def newframe(self):                                                                 #creates GUI
        self.gui.title("Coordinator")                                                 #title for the gui
        fr = Frame(self.gui, width=200, height=200)                                     #creates frame
        fr.pack(side=LEFT, padx=25, pady=25)
        fr1 = Frame(fr, width=75, height=75)
        fr1.pack(side=BOTTOM)
        scroll_bar1 = Scrollbar(fr)
        scroll_bar1.pack(side=RIGHT, fill=Y)
        self.text_box = Text(fr, height=15, width=40, yscrollcommand=scroll_bar1.set)  #creates screen for the display
        self.text_box.pack(side=LEFT, fill=Y)
        self.entry_box = Entry(fr1, width=60)                                          #create box to type
        self.entry_box.pack(anchor=CENTER, expand=1, pady=10, padx=5)
        self.entry_box.focus_set()
        self.but_ton = Button(fr1, text='Send', command=self.printtext)                 #button to send, log in and to quit
        self.but_ton1 = Button(fr1, text='Login', command=self.connectserver1)
        self.but_ton2 = Button(fr1, text='Quit', command=self.quit)
        self.but_ton3=Button(fr1,text="Request", command=self.voting)
        self.but_ton.pack(side=RIGHT)
        self.but_ton1.pack(side=LEFT)
        self.but_ton2.pack(side=RIGHT)
        self.but_ton3.pack(side=LEFT)

    def messagesending(self,content):  # function to send the message to the server
        string1 = content
        currenttime = datetime.datetime.now().replace(microsecond=0)
        diff = (currenttime - self.stdtime)
        self.stdtime = currenttime
        l1 = 'POST/Coodinator.http\r\n ' \
             'Host: 10.219.139.223\r\n ' \
             'User-Agent:/pycharm\r\n ' \
             'Content-Type:Text\r\n'
        l2 = ' Content-Length:'  # variable containing all the detail
        l3 = ' date : '
        date = str(datetime.datetime.now()) + str('\r\n')  # get current date
        c1 = str(len(string1))  # it gets size of the message received from client
        http = l1 + l2 + c1 + str('\r\n') + l3 + date + str(']') + string1
        self.myclisock.sendall((str(diff) + str(':') + str('[') + http).encode('utf-8'))  # send to client

    def timmer(self):
        if len(self.userlist1)!=3:
            if self.counter !=1:
                self.abort()

    def voting(self):
        vote="Please Vote to store the String"
        self.messagesending(vote)
        self.counter=0
        Timer(15, self.timmer, ()).start()
        self.messagesending("You have 50 seconds to Vote...\n" )
        print("participant in Wait mode")

    def commit(self):                                                                     #Global Commit
        self.messagesending("Globalcommit")
        print("participant in Commit mode")
        print("participant in Init mode")

    def abort(self):                                                                     #Global abort
        self.messagesending("Globalabort")
        print("participant in Abort mode")
        print("participant in Init mode")
        self.counter=1
        self.userlist=[]

    def quit(self):                                                                     #to log off the client
        self.myclisock.send(("log off").encode('utf-8'))
        self.gui.destroy()                                                              #destroys the gui

    def printtext(self):                                                                #function to send the message to the server
        string = self.entry_box.get()                                                   #get input
        currenttime = datetime.datetime.now().replace(microsecond=0)
        diff = (currenttime - self.stdtime)
        self.stdtime=currenttime
        l1 = 'POST/client.http\r\n ' \
             'Host: 10.219.139.223\r\n ' \
             'User-Agent:/pycharm\r\n ' \
             'Content-Type:Text\r\n'
        l2 = ' Content-Length:'                                                        # variable containing all the detail
        l3 = ' date : '
        date = str(datetime.datetime.now()) + str('\r\n')                              # get current date
        c1 = str(len(string))                                                               # it gets size of the message received from client
        http = l1 + l2 + c1 + str('\r\n') + l3 + date + str(']')+ string
        self.myclisock.sendall((str(diff) + str(':') +str('[')+ http).encode('utf-8'))        #send to client
        self.entry_box.delete(0, END)

    def connectserver1(self):                                                           #connect to server
        PORT = 1337
        HOST = socket.gethostname()
        self.myclisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #initialize socket
        self.myclisock.connect((HOST, PORT))                                            #connect to server
        self.stdtime = datetime.datetime.now().replace(microsecond=0)                   #initial time
        self.myclisock.sendall(("coordinator").encode())
        self.commit_count = 0
        self.userlist=[]
        self.userlist1=[]
        print("participant in Init mode")
        Thread(target=self.receivemsg).start()                                          #start thread to keep receiving messages

    def commitabort(self,msg):
        usernam = msg.split(']')
        username = usernam[0].split('[')
        self.userlist.append(username[1])
        self.text_box.insert(END, 'commited' + '\n')
        self.userlist1=set(self.userlist)
        if len(self.userlist1) == 3:
            self.commit()
            self.userlist = []

    def receivemsg(self):                                                               #to receive message
        while True:
            msg = self.myclisock.recv(1024).decode('utf-8')                             #receive message from server
            if ':commit' in msg:
                self.commitabort(msg)
            if ':abort' in msg:
                self.abort()
            self.text_box.insert(END, msg + '\n')                                       # display it in gui
            self.text_box.see(END)


gui = Tk()                                                                             #initialize the gui
MyClient(gui)                                                                          #start the class MyClient
mainloop()                                                                             #start the GUI


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
#https://www.quora.com/How-do-you-create-a-timeout-function-in-Python