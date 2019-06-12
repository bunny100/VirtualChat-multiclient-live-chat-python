from socket import *
from threading import Thread
import time

#conn = connection
def incoming_connections():
    #listens for ten clients' connection requests (makes a queue for 10 and gives upper bound to queue)
    server_socket.listen(10)
    
    #always runs to accept incoming connections
    while True:
        #socket_discription, address
        conn, address = server_socket.accept()             
        
        #send message by server to every client upon connection
        conn.send(bytes("Type your name and press enter!\n", "utf8"))
        
        #threading makes sure to run handle_conn() function inside accept_incoming_connections()
        Thread(target=messages, args=(conn,)).start()


def messages(conn):
    
    #check file format
    formats = ["mp4", "pdf", "docx", "jpg", "png", "raw", "gif", "ai", "tiff", "psd", "eps", "mp3", "jpeg", "wav" , "mpeg4" , "mkv" , "avi" , "mov" , "txt", "ppt" "csv" ,"doc" , "aac", "wma", "mpeg2"]
        
    #every first message is a client's name
    conn_name = conn.recv(1024).decode("utf8")
    conn.send(bytes("Welcome to Virtual Chat\n\n", "utf8"))
    for x in conns:
        x.send(bytes("                  "+conn_name+" joined the conversation", "utf8"))
    conns[conn] = conn_name 
    
    while True:
            #recieve messages
            msg = conn.recv(4096000)
            try:
                
                format_flag = True
                decoded_msg = msg.decode("utf8")
                check = decoded_msg[0:7] #check for block/sleep
                double_check= decoded_msg[0:9] #check for unblock
                triple_check = decoded_msg[0:6] #check for name change
        
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
            #if anything is recieved by server
            if msg:
                if decoded_msg != False:
                    #checking normal text message (a message to send every conn straight away)
                    if msg != bytes("\\quit", "utf8") and check != "\\block\\" and check != "\\sleep\\" and double_check != "\\unblock\\" and triple_check != "\\name\\" and format_flag == True:
                        #if this sender is blocked by someone than send his message to everyone except the one who blocked him.
                        if conn_name in blacklist:
                            for x in conns:
                                flag = True
                                for y in blacklist[conn_name]:
                                    
                                
                                    if conns.get(x) == y:
                                        flag = False
                                        break
                                    
                                
                                    elif conns.get(x) != y:
                                        flag = flag
                                        continue
                                if flag == True:
                                    x.send(bytes(conn_name +": ", "utf8")+msg)
                                else:
                                    
                                    continue
                                        

                        #if not blocked by anyone
                        else:
                            for x in conns:
                                x.send(bytes(conn_name+": ", "utf8")+msg)
                    #if its a text message but also a filename 
                    elif msg != bytes("{quit}", "utf8") and check != "\\block\\" and check != "\\sleep\\" and double_check != "\\unblock\\" and triple_check != "\\name\\" and format_flag == False :
                        if conn_name in blacklist:
                            for x in conns:
                                flag = True
                                for y in blacklist[conn_name]:
                                    
                                
                                    if conns.get(x) == y:
                                        flag = False
                                        break
                                    
                                
                                    elif conns.get(x) != y:
                                        flag = flag
                                        continue
                                if flag == True:
                                    x.send(msg)
                                else:
                                    
                                    continue
                                        

                        
                        else:
                            for x in conns:
                                x.send(msg)

                                
                    #if someone blocked some other
                    elif check == check_blocked:
                        #name of person being blocked
                        blocked = decoded_msg[7:]
                        #blacklist of blocked persons against everyone, who blocked them (tuple)
                        if blocked in blacklist:
                            blacklist[blocked].append(conn_name)

                            
                        else:
                            
                            l = []
                            blacklist[blocked] = l
                            blacklist[blocked].append(conn_name)
                            
                        conn.send(bytes("                  You blocked "+blocked+" :(", "utf8"))
                    
                    #check if someone unblocked some other
                    elif double_check == check_unblocked:
                        
                        unblocked = decoded_msg[9:]
                        if unblocked in blacklist:
                            for x in blacklist[unblocked]:
                                if x == conn_name:
                                    blacklist[unblocked].remove(conn_name)
                                    
                        #notify unblock
                        conn.send(bytes("                  You unblocked "+unblocked+" :)", "utf8"))

                    
                    #this condition is to avoid sending anyone's "\sleep\" msg to chat box (main "sleep" condition in conn file)
                    elif check == check_sleep:
                        how_much_sleep = decoded_msg[7:]
                        
                        time.sleep(int(how_much_sleep))

                        
                    #check if someone changed his name
                    elif triple_check == check_name:
                        
                        #assigning new name
                        new_name = decoded_msg[6:]
                        
                        conns[conn] = new_name


                        for x in conns:
                                x.send(bytes("                  "+conn_name+" has changed name to "+ new_name, "utf8"))


                        #update name in blacklist (name being blocked by someone)
                        for y in blacklist:
                            if y == conn_name:
                                blacklist[new_name] = blacklist.pop(conn_name)
                                conn_name = new_name
                                
                        #update name in blacklist (if name blocked someone else)
                        for z in blacklist:
                            if conn_name in blacklist[z]:
                                blacklist[z].remove(conn_name)
                                blacklist[z].append(conn_name)
                        #name now equals new name
                        conn_name = new_name
                        
                    #if any client's message is \quit then close its connection and remove that client.    
                    else:

                        
                        conn.close()
                        del conns[conn]
                        
                        for x in conns:
                            x.send(bytes("                  "+conn_name+" has left the conversation", "utf8"))
                        break
                        
                        
                    
                #if its not a text message but a file (because it cannot be decoded)
                else:
                    if conn_name in blacklist:
                            for x in conns:
                                flag = True
                                for y in blacklist[conn_name]:
                                    
                                
                                    if conns.get(x) == y:
                                        flag = False
                                        break
                                    
                                
                                    elif conns.get(x) != y:
                                        flag = flag
                                        continue
                                if flag == True:
                                    x.send(msg)
                                else:
                                    
                                    continue

                    else:
                        for x in conns:    
                            x.send(msg)

                        

                      
              

conns = {}
blacklist = {}
#AF_INET family for sddressing system, SOCK_STREAM for type of connection
server_socket = socket(AF_INET, SOCK_STREAM)
#getting local IP automatically (dynamic IP)
IP = gethostbyname(gethostname())
server_socket.bind((IP, 4510))


if __name__ == "__main__":

    
    main_process = Thread(target=incoming_connections()).start()
    socket.close()
