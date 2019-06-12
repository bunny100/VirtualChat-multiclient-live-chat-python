# VirtualChat-multiclient-live-chat-python
A python based multi user live chat system including various functionalities (block/unblock/sleep/name). Send files and messages on the go.

you can send live messages between connected users.

it is just like group chat prototype of whatsapp.

Procedure:
=> make a copy of client file for every new user.
=> I have made it for server and clients on same machine, but you can always connect cients from different machines, you just have to give IP address of server machine in every client file you want to connect.
=> first run server.py file and then every client.py file and it gets connected to server automatically
=> you have to first enter your name in the text field.
=> then you can send messages
=> file can be sent if they are put into the folder where client.py file is present
=> type "filename.fileformat" and it will be sent to every client connected.
=> you can always change your name, block anyother person (only the person blocked will not be able to send you messages), unblock the blocked users, and also you can sleep notifications for any amount of time (seconds), syntax is as follows

					\name\newname 				              (\name\john)
					\block\username to be blocked 		  (\block\bella)
					\unblock\username to be unblocked 	(\unblock\bella)
					\sleep\10 				                  (turn off notifications for 10 seconds)
					\quit					                      (to leave the conversation)
