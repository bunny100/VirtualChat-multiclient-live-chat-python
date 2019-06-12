from socket import *
import tkinter
from threading import Thread
import time



def user_send(event=None):  
    formats = ["mp4", "pdf", "docx", "jpg", "png", "raw", "gif", "ai", "tiff", "psd", "eps", "mp3", "jpeg", "wav" , "mpeg4" , "mkv" , "avi" , "mov" , "txt", "ppt" "csv" ,"doc" , "aac", "wma", "mpeg2"]
    
    format_flag = True
    msg = my_msg.get()
    t0 = "\\sleep\\"
    t1= msg[0:7]
    #checks for file or text message
    for x in formats:
        if msg.endswith(x):        
                format_flag = False

    #if it is a file
    if format_flag == False:
            
            my_msg.set("")
            
            #check if file is present
            try:
                    #send file name as message
                    client_socket.send(bytes(msg, "utf8"))
                    #send file
                    f = open(msg,'rb')
                    l = f.read(4096000)
                    client_socket.send(l)
                    
                    f.close()
            except:
                    print("file not found")
                    IOError
    else:
            #sleep client's recieve and send if message is sleep
            if t0 == t1:
                t = int(msg[7:])
                time.sleep(t)
                
                
            my_msg.set("")
            #sends every message to server
            client_socket.send(bytes(msg, "utf8"))
            
            #closes client's socket after sending message of quit
            if msg == "\\quit":
                container.insert(tkinter.END, "You left the conversation")
                client_socket.close()
                main_window.quit()




def user_receive():
               
        #forever loop to recieve messages
        while True:
                #decoded msg
                #file size is 4MB maximum
                msg = client_socket.recv(4096000)
                #to check if it is a file or text message
                try:
                        ifnotpic = msg.decode("utf8")
                        filename = ifnotpic
                        
                except:
                        ifnotpic = False
                #if it is a text message
                if ifnotpic != False: 
                        container.insert(tkinter.END, msg)
                #if it is a digital file
                else:        
                        with open(filename,'wb') as f:
                                f.write(msg)                        
                                f.close()
                        
                                






#Program GUI
main_window = tkinter.Tk()
main_window.geometry("600x300")
main_window.title("Virtual Chat")

#frame
messages_frame = tkinter.Frame(main_window)

#msg
my_msg = tkinter.StringVar()
my_msg.set("Type here: ")

#container
container = tkinter.Listbox(messages_frame, height=15, width=100)
container.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
container.pack()

messages_frame.pack()

#block
message_block = tkinter.Entry(main_window, textvariable=my_msg, width = 80)
message_block.bind("<Return>", user_send)
message_block.pack()

#button
message_button = tkinter.Button(main_window, text="Send", command=user_send)
message_button.pack()



main_window.protocol("WM_DELETE_WINDOW")


#AF_INET family for sddressing system, SOCK_STREAM for type of connection
client_socket = socket(AF_INET, SOCK_STREAM)
#getting local IP automatically (dynamic IP)
IP = gethostbyname(gethostname())
client_socket.connect((IP, 4510))

if __name__ == "__main__":
        #thread to run receive parallel with GUI Loop
        receive_thread = Thread(target=user_receive).start()
        tkinter.mainloop()
            

