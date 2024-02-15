# This is an example from "Computer Networking: A Top Down Approach" textbook chapter 2
# You can try this with nc localhost 12000
# See the following link for more details about the socket liberary (https://docs.python.org/3/library/socket.html)

import socket
import sys


'''
Server program that hosts a phonebook consisting of names and the phone numbers associated
with those names.
'''
def server():
    #Server port
    serverPort = 13000

    #Create server socket that uses IPv4 and TCP protocols
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Error in server socket creation:',e)
        sys.exit(1)

    #Associate 12000 port number to the server socket
    try:
        serverSocket.bind(('', serverPort))
    except socket.error as e:
        print('Error in server socket binding:',e)
        sys.exit(1)

    print('The server is ready to accept connections')

    #The server can only have one connection in its queue waiting for acceptance
    serverSocket.listen(1)
    numbers = {}
    try:
        #Server accepts client connection
        connectionSocket, addr = serverSocket.accept()
        welcome_message = 'Welcome to the online phone book.\n\nPlease select the operation\n1)Add a new entry\n2)Search\n3)Terminate the connection\n\nChoice: '.encode('ascii')
        connectionSocket.send(welcome_message)
        while(1):
            #Server receives client message, and decodes it
            choice_raw = connectionSocket.recv(2048)
            choice = choice_raw.decode('ascii')
            print(choice)
            #add to phone book if choice is 1
            if choice == '1':
                ask_name = "Enter the name: "
                connectionSocket.send(ask_name.encode('ascii'))
                name = connectionSocket.recv(2048).decode('ascii').strip()
                ask_number = "Enter the phone Number: "
                connectionSocket.send(ask_number.encode('ascii'))
                number = connectionSocket.recv(2048).decode('ascii').strip()
                add_phone_number(name, number, numbers)
            #search for phonebook entry if choice is 2
            elif choice == '2':
                message = 'Enter the search word: '
                connectionSocket.send(message.encode('ascii'))
                name = connectionSocket.recv(2048).decode('ascii').strip()
                if name == '-1':
                    pass
                else:
                    res = search_phonebook(name, numbers)
                    message = format_result(res)
                    connectionSocket.send(message.encode('ascii'))
            #Server terminates client connection
            menu = 'Please select the operation\n1)Add a new entry\n2)Search\n3)Terminate the connection\n\nChoice: '
            connectionSocket.send(menu.encode('ascii'))

    except socket.error as e:
        print('An error occured:',e)
        serverSocket.close()
        sys.exit(1)
    except:
        print('Goodbye')
        serverSocket.close()
        sys.exit(0)

'''
Adds entry to phonebook. If name already exists, appends it to the list where name is the
key.
Parameters:
    name: string- name of the person to add to the phonebook
    number: string- number to add to the phonebook that cooresponds to the name
'''
def add_phone_number(name, number, numbers):
    if name in numbers.keys():
        numbers[name].append(number)
    else:
        numbers[name] = [number]

'''
Searches phonebook to find entry that matches or contains the search criteria
Parameters:
    name: string- substring of name of the person to search
    numbersL dict- dictionary containing names as key and a list of numbers as the value
'''
def search_phonebook(name, numbers):
    res = []
    for book_names in numbers.keys():
        if name in book_names:
            res.append((book_names, numbers[book_names]))
    return res


'''
Formats string send back to client program to print.
'''
def format_result(res):
    message = ''
    for data in res:
        print(data)
        message += str(data[0])
        message += '    ' + str(data[1]) + '\n'
    message += '\n'
    return message


#-------
server()
