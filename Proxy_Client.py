import socket


host = '192.168.1.5'
port = 8055

message ='GET http://www.facebook.com'

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((host,port))

client_socket.send(bytes(message,encoding='utf8'))


data = 1
while True:
    
    print(str(data))
    
    data = client_socket.recv(5000).decode('utf-8')
    
    if not data:
        break
    
client_socket.close()


    
    
        
    
        
        
   
    
