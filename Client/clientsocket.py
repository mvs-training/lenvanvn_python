import socket
from clientchat import User

#----------------------------------------------------------------------

def main():
    
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12349              # Reserve a port for your service.
    
    s.connect((host, port))
    
    use = User()
    while True:
        
        choose = int(input("Nhap vao lua chon: \n"))
        
        if choose == 1:
            s.sendall(use.SignUp())
            data = s.recv(1024)
            print (data)
        if choose == 2:
            s.sendall( use.SignIn() )
            data = s.recv(1024)
            data.split(",")
            print(data)
        if choose == 3:
            data = "3,"
            friend = raw_input("Nhap vao ten ban be can chinh sua: ")
            data += friend
            s.sendall(data)
            data = s.recv(1024)
            print(data)
            data = raw_input("Nhap vao thay doi: ")
            s.sendall(data)
            data = s.recv(1024)
            print(data)
        if choose == 4:
            s.sendall(use.ShowFriendByCity())
            data = s.recv(1024)
            print(data)            
        if choose == 5:
            use.SendMess(use.id)
        if choose == 6:
            use.ShowMess(use.id)
        if choose == 7:
            use.ShowMessDetail(use.id)
    
    

        
if __name__ == '__main__':
    main()