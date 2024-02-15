# This is an example from "Computer Networking: A Top Down Approach" textbook chapter 2
import socket
import sys

'''
Client program that connects to a phonebook on a server. Client can add entries and
search for existing entries in the phonebook.
'''
def client():
    # Server Information
    serverName = '127.0.0.1' #'localhost'
    serverPort = 13000
    
    #Create client socket that useing IPv4 and TCP protocols 
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Error in client socket creation:',e)
        sys.exit(1)    
    
    try:
        #Client connect with the server
        clientSocket.connect((serverName,serverPort))
        while 1: 
            # Client receives a message from the server and print it
            message = clientSocket.recv(2048)
            print(message.decode('ascii'), end="")
            choice = input("")
            if choice == '':
                choice = 'n/a'
            # Client terminate connection with the server
            clientSocket.send(choice.encode('ascii'))
            #insert to phone book
            if choice == '1':
                message = clientSocket.recv(2048).decode('ascii')
                print(message, end='')
                name = input("")
                while name == '':
                    name = input(message)
                clientSocket.send(name.encode('ascii'))
                message = clientSocket.recv(2048).decode('ascii')
                print(message, end='')
                number = input("")
                while number == '':
                    number = input(message)
                clientSocket.send(number.encode('ascii'))
                print('')
            #serach phone book
            elif choice == '2':
                message = clientSocket.recv(2048).decode('ascii')
                print(message, end = '')
                name = input("")
                if name == '':
                    name = '-1'
                    clientSocket.send(name.encode('ascii'))
                else:
                    clientSocket.send(name.encode('ascii'))
                    message = clientSocket.recv(2048).decode('ascii')
                    print('Name    Number(s)')
                    print(message)
            #close connection with the server
            elif choice == '3':
                print('Connection is terminated.')
                clientSocket.close()
                break
        
    except socket.error as e:
        print('An error occured:',e)
        clientSocket.close()
        sys.exit(1)
    

#----------
client()
