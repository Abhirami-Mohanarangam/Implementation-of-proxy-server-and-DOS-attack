from Proxy_Cache_DS import *
import socket
import sys
import _thread
import datetime
import os
import pickle


cache = LFUCache(3);


def cache_fn(messageString, client_socket):
    
    print('Connected Accepted')
    
    HttpTypeMethod = messageString[0]
    URLpath = messageString[1]
    URLpath = URLpath[7:]
    
    
    print("Request is ", HttpTypeMethod, " to URL : ", URLpath)
    print("--------------------------------------------------")
    
    
    start = datetime.datetime.now()
    current_file = "/" + URLpath + ".txt"
    print(current_file[1:])
    try:
        #Search in the cache file
        file = open(current_file[1:], "r")
        contents = file.readlines()
        print("Match found in cache and reading the file\n")
        
        cache.insertItem(URLpath)
        print_cache(cache)
        
        for i in range(0, len(contents)):
            client_socket.send(contents[i].encode())
            
        print("Time taken to read from Cache:",datetime.datetime.now() - start , " Secs")
    
    except IOError:
        #Fetch from the main server at port 80
        start = datetime.datetime.now()
        print("Cache File not Found\n File is being fetched from Server to Create Cache\n")
       
        Proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_url = URLpath
        print(host_url)
        try:
            Proxy_server.connect((host_url, 80))
            cache.insertItem(URLpath)
            save_object(cache)
            print_cache(cache)
            print("Socket Connected on default Port 80 to fetch")
            ser_cache_file = Proxy_server.makefile('rwb', 0)
            
            ser_cache_file.write(bytes("GET " + "/ HTTP/1.1\r\nHost:"+ URLpath +"\r\n\r\n",encoding='utf8'))           
            br = ser_cache_file.readlines()
            
            print(br)
            temp = open("./" + URLpath +'.txt', "w")
      
            for dt in br:
                temp.write(str(dt))
                client_socket.send(bytes(str(dt),encoding='utf-8'))
            
        except:
            print("Not a  Valid URL/ Data Could not be written to file")
        print("Time taken to read from Server:",datetime.datetime.now() - start," Secs")
    print('Written data to file')
    client_socket.close()

def save_object(obj):
    try:
        os.remove('cache.pkl')
        # print("try save")
    except:
        print("Creating cache file")
        # print("except save")
    with open('cache.pkl', 'wb') as output:
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def main():
	
        try:
            global cache
            with open('cache.pkl', 'rb') as input:
                cache = pickle.load(input)
                print_cache(cache)
		
        except:
            print("Cache file doesn't exist. It is yet to be created")
        port_server = 8055
            
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# server socket
        print("Server is started")
        server_socket.bind(('192.168.1.5', port_server))
        server_socket.listen(5)
        while True:
            print("Bind Successful")
            print("-------------------------------------")
            client_socket, addr = server_socket.accept() 
            print("Received Connection from <Host,Port> ", addr)
            message = client_socket.recv(5000).decode()
            
           
            messageString = str(message).split()
            if len(messageString) <= 1 or len(messageString) > 2:
                
                d = "HTTP/1.1 200 OK\r\n"
                d += "Content-Type: text/html; charset=utf-8\r\n"
                d += "\r\n"
                d += "<html><body>Hello World</body></html>\r\n\r\n"
                client_socket.sendall(d.encode())
                client_socket.shutdown(socket.SHUT_RDWR)
                continue		
            
            _thread.start_new_thread(cache_fn ,(messageString, client_socket))
            #if len(messageString) <= 1 or len(messageString) > 2:
             #   client_socket.shutdown(socket.SHUT_RDWR)

if __name__ == '__main__':
	main()