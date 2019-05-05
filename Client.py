from socket import *
from threading import Thread
import tkinter
import time


def receive():
               
    
        while True:
                msg = client_socket.recv(4096000)
                try:
                        ifnotpic = msg.decode("utf8")
                        filename = ifnotpic
                        
                except:
                        ifnotpic = False
                if ifnotpic != False:
                                               
                        #msg = client_socket.recv(1024).decode("utf8")
                        msg_list.insert(tkinter.END, msg)
                    #except OSError: # Possibly client has left the chat.
                     #   break
                #t=0
                else:
                        with open(filename,'wb') as f:
                                f.write(msg)                        
                                f.close()


def send(event=None):  # event is passed by binders.
    formats = ["mp4", "pdf", "docx", "jpg", "png", "raw", "gif", "ai", "tiff", "psd", "eps", "mp3", "jpeg", "wav" , "mpeg4" , "mkv" , "avi" , "mov" , "txt", "ppt" "csv" ,"doc" , "aac", "wma", "mpeg2"]
    format_flag = True
    global t
    msg = my_msg.get()
    t0 = "\\sleep\\"
    t1= msg[0:7]
    for x in formats:
            
        if msg.endswith(x):
                
                
                        
                format_flag = False

    if format_flag == False:
            
            my_msg.set("")  # Clears input field.
            #filename= msg
            client_socket.send(bytes(msg, "utf8"))
            f = open(msg,'rb')
            l = f.read(4096000)
            client_socket.send(l)
            
            f.close()

    else:               
            if t0 == t1:
                t = int(msg[7:])
                my_msg.set("")
                time.sleep(t)
                
                
            my_msg.set("")  # Clears input field.
            client_socket.send(bytes(msg, "utf8"))

            if msg == "\\quit":
                msg_list.insert(tkinter.END, "You left the conversation")
                client_socket.close()
                top.quit()
        
def send_file(event=None):        
            filename = my_picture.get()
            my_msg.set("")  # Clears input field.
            #filename= msg
            f = open(filename,'rb')
            l = f.read(4096000)
            client_socket.send(l)
            l = f.read(4096000)
            f.close()
            

def on_closing(event=None):
    
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.geometry("600x300")
top.title("Virtual Chat")

messages_frame = tkinter.Frame(top)

my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your message: ")
my_picture = tkinter.StringVar()
my_picture.set("Type filename here: ")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

message_field = tkinter.Entry(top, textvariable=my_msg, width = 80)
message_field.bind("<Return>", send)
message_field.pack()

message_button = tkinter.Button(top, text="Send", command=send)

message_button.pack()


top.protocol("WM_DELETE_WINDOW", on_closing)





client_socket = socket(AF_INET, SOCK_STREAM)
IP = gethostbyname(gethostname())
client_socket.connect((IP, 33000))


receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
    

