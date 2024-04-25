import socket
import threading
from Crypto.Util.number import bytes_to_long, getPrime
import json

SERVER_HOST = '127.0.0.1' 
SERVER_PORT = 2568

FLAG = b"Redacted Flag"
NumofMess = 30
# 30 messages
messages = [
    b"A"*125,
    b"B"*125,
    b"C"*125,
    b"D"*125,
    b"E"*125,
    b"F"*125,
    b"G"*125,
    b"H"*125,
    b"I"*125,
    b"J"*125,
    b"K"*125,
    b"L"*125,
    b"M"*125,
    b"N"*125,
    b"O"*125,
    b"P"*125,
    b"Q"*125,
    b"R"*125,
    b"S"*125,
    FLAG,
    b"T"*125,
    b"U"*125,
    b"V"*125,
    b"W"*125,
    b"X"*125,
    b"Y"*125,
    b"Z"*125,
    b"1"*125,
    b"2"*125,
    b"3"*125
]


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)  # Listen for up to 5 incoming connections
print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

banner = """
 ::::::::  :::    :::     :::     :::::::::  ::::    :::       :::::::: ::::::::::: :::::::::: 
:+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:+:   :+:      :+:    :+:    :+:     :+:        
+:+        +:+    +:+  +:+   +:+  +:+    +:+ :+:+:+  +:+      +:+           +:+     +:+        
+#++:++#++ +#++:++#++ +#++:++#++: +#++:++#:  +#+ +:+ +#+      +#+           +#+     :#::+::#   
       +#+ +#+    +#+ +#+     +#+ +#+    +#+ +#+  +#+#+#      +#+           +#+     +#+        
#+#    #+# #+#    #+# #+#     #+# #+#    #+# #+#   #+#+#      #+#    #+#    #+#     #+#        
 ########  ###    ### ###     ### ###    ### ###    ####       ########     ###     ###        

"""


Instruction = b"Enter the index of the message you want (0-29): "

# Handle client 
def handle_client(client_socket, client_address):
    client_socket.send(banner.encode())
    while True:
        client_socket.send(Instruction)
        # Receive data from the client
        data = client_socket.recv(5).decode().strip("\n")
        print(data)
        if data.lower() == "exit":
            client_socket.send(b"You have successfully exited.\n")
            break

        # Process player input and send responses
        process_game_input(data,client_socket) 
    client_socket.close()

def encrypt_message(message):
    m = bytes_to_long(message)
    p = getPrime(1024)
    q = getPrime(1024)
    N = p * q
    e = 3
    c = pow(m, e, N)
    return N, e, c

def process_game_input(input_data,client_socket):
    try:
        message_index = int(input_data)
        if 0 <= message_index < NumofMess:
            selected_message = messages[message_index]
            N, e ,c = encrypt_message(selected_message)
            client_socket.send(b"Encrypted Message: \n")
            message = {"N":N,"e":e,"ciphertext":c}
            message = json.dumps(message)
            client_socket.send(message.encode())
            client_socket.send(b"\n")
        else:
            client_socket.send(b"Invalid index. Please enter a number between 0 and 29.\n")
    except ValueError:
        client_socket.send(b"Invalid input. Please enter a number.\n")
        


while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()



