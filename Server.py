from socket import *
from threading import Thread
from multiprocessing import *
import time


def incoming_clients():
    #listens for five clients at a time (makes a queue for 5 to give prioritization.
    socket.listen(5)
    
    #always runs to accept incoming connections
    while True:
        client, client_address = socket.accept()
        
        print("%s:%s has connected." % client_address)
        #send message by server to every client upon connection
        client.send(bytes("Welcome to virtual chat! Now type your name and press enter!\n", "utf8"))
        
        #threading makes sure to run handle_client() function inside accept_incoming_connections()
        Thread(target=messages, args=(client,)).start()


def messages(client):  # Takes client socket as argument.
    
    #check file format
    formats = ["mp4", "pdf", "docx", "jpg", "png", "raw", "gif", "ai", "tiff", "psd", "eps", "mp3", "jpeg", "wav" , "mpeg4" , "mkv" , "avi" , "mov" , "txt", "ppt" "csv" ,"doc" , "aac", "wma", "mpeg2"]
        
    #every first message is a client's name
    name = client.recv(1024).decode("utf8")
    welcome = "Welcome %s! If you ever want to quit, type \quit to exit." % name
    client.send(bytes(welcome, "utf8"))
    #message goes to every person about every person joining the chat
    msg = "%s has joined the chat!" % name
    
    for sock in clients:
        sock.send(bytes("                  "+name+" has joined the chat", "utf8"))
    clients[client] = name #saves clients' name in a list at the place of every client's address
    print(clients)
    #after first message comes the chat part and this loop is forever to recv message anytime from clients and broadcasts them within itself through broadcast()
    while True:
            #send each client's message to every client
            msg = client.recv(4096000)
            try:
                
                format_flag = True
                decoded_msg = msg.decode("utf8")
                check = decoded_msg[0:7]
                double_check= decoded_msg[0:9]
                triple_check = decoded_msg[0:6]
        
                check_blocked = "\\block\\"
                check_sleep = "\\sleep\\"
                check_unblocked = "\\unblock\\"
                check_name = "\\name\\"

                #checking whether the file format is supported by our program
                for x in formats:
                    if decoded_msg.endswith(x):
                        
                        format_flag = False
                    
                
            except:
                decoded_msg = False                
            if msg:
                if decoded_msg != False:
                    #checking normal text message (a message to send every client straight away)
                    if msg != bytes("\\quit", "utf8") and check != "\\block\\" and check != "\\sleep\\" and double_check != "\\unblock\\" and triple_check != "\\name\\" and format_flag == True:
                        #if this sender is blocked by someone than send his message to everyone except the one who blocked him.
                        if name in blacklist:
                            for x in clients:
                                flag = True
                                for y in blacklist[name]:
                                    
                                
                                    if clients.get(x) == y:
                                        flag = False
                                        break
                                    
                                
                                    elif clients.get(x) != y:
                                        flag = flag
                                        continue
                                if flag == True:
                                    x.send(bytes(name +": ", "utf8")+msg)
                                else:
                                    
                                    continue
                                        

                        #if not blocked by anyone
                        else:
                            for sock in clients:
                                sock.send(bytes(name +": ", "utf8")+msg)
                    #if its not a text message but a file 
                    elif msg != bytes("{quit}", "utf8") and check != "\\block\\" and check != "\\sleep\\" and double_check != "\\unblock\\" and triple_check != "\\name\\" and format_flag == False:
                        if name in blacklist:
                            for x in clients:
                                flag = True
                                for y in blacklist[name]:
                                    
                                
                                    if clients.get(x) == y:
                                        flag = False
                                        break
                                    
                                
                                    elif clients.get(x) != y:
                                        flag = flag
                                        continue
                                if flag == True:
                                    x.send(msg)
                                else:
                                    
                                    continue
                                        

                        
                        else:
                            for sock in clients:
                                sock.send(msg)

                                
                    #if someone blocked some other
                    elif check == check_blocked:
                        #name of person being blocked
                        blocked = decoded_msg[7:]
                        #blacklist of blocked persons against everyone, who blocked them (tuple)
                        if blocked in blacklist:
                            blacklist[blocked].append(name)

                            
                        else:
                            
                            l = []
                            blacklist[blocked] = l
                            blacklist[blocked].append(name)
                            
                        client.send(bytes("                  You blocked "+blocked+" :(", "utf8"))
                    
                    #check if someone unblocked some other
                    elif double_check == check_unblocked:
                        
                        unblocked = decoded_msg[9:]
                        if unblocked in blacklist:
                            for x in blacklist[unblocked]:
                                if x == name:
                                    blacklist[unblocked].remove(name)
                                    
                        #notify unblock
                        client.send(bytes("                  You unblocked "+unblocked+" :)", "utf8"))

                    
                    #this condition is to avoid sending anyone's "\sleep\" msg to chat box (main "sleep" condition in client file)
                    elif check == check_sleep:
                        how_much_sleep = decoded_msg[7:]
                        
                        time.sleep(int(how_much_sleep))

                        
                    #check if someone changed his name
                    elif triple_check == check_name:
                        
                        #assigning new name
                        new_name = decoded_msg[6:]
                        
                        clients[client] = new_name


                        for sock in clients:
                                sock.send(bytes("                  "+name+" has changed name to "+ new_name, "utf8"))


                        #update name in blacklist (name being blocked by someone)
                        for y in blacklist:
                            if y == name:
                                blacklist[new_name] = blacklist.pop(name)
                                name = new_name
                                
                        #update name in blacklist (if name blocked someone else)
                        for z in blacklist:
                            if name in blacklist[z]:
                                blacklist[z].remove(name)
                                blacklist[z].append(new_name)
                        #name now equals new name
                        name = new_name
                        
                    #if any client's message is {quit} then close its connection and remove that client from clients' names list.    
                    else:

                        
                        client.close()
                        del clients[client]
                        
                        for sock in clients:
                            sock.send(bytes("                  "+name+" has left the chat", "utf8"))
                        break
                        
                        
                    
                #?????????
                else:
                    if name in blacklist:
                            for x in clients:
                                flag = True
                                for y in blacklist[name]:
                                    
                                
                                    if clients.get(x) == y:
                                        flag = False
                                        break
                                    
                                
                                    elif clients.get(x) != y:
                                        flag = flag
                                        continue
                                if flag == True:
                                    x.send(msg)
                                else:
                                    
                                    continue

                    else:
                        for sock in clients:    
                            sock.send(msg)

                        

                      
              

clients = {}
blacklist = {}

socket = socket(AF_INET, SOCK_STREAM)
#getting local IP automatically (dynamic IP)
IP = gethostbyname(gethostname())
socket.bind((IP, 33000))


if __name__ == "__main__":

    main_process = Process(target = incoming_clients())
    main_process.start()
    main_process.join()
    
