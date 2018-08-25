from controller import ConnectSQL as Conn
import  controller
import socket
 
c = None
def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)
     
    #total data partwise in an array
    total_data=[];
    data='';
     
    #beginning time
    import time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
         
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin = time.time()
           # else:
                #sleep for sometime to indicate a gap
                #time.sleep(0.1)
        except:
            pass
     
    #join all parts to make final string
    return ''.join(total_data)


class User:
    
    def __init__(self):
        self.id = 1
        self.username = 1
        self.password = 1
        self.city = 1
        self.flag = None
    
    #----------------------------------------------------------------------
    def SignUp(self,username,password,city):
        
        print (password)
        print (username)
        print (city)
        #conObj = controller.ConnectSQL() 
        conObj = Conn()
        conObj.Open()
        with Conn.con:
            if conObj.CheckCity(city) == 0:
                conObj.WriteToCity(city,)
            id = conObj.TranCityToId(city,)
            
            conObj.SignUp(username, password,id)
        data = "Sign up successfully!"
        return data
            
    #----------------------------------------------------------------------
    def SignIn(self,username,password):
        conOb = Conn()
        conOb.Open()
        data = ""
        with Conn.con:
            if conOb.CheckSignIn(username,password) > 0:
                data = data + "1,Sign successfuly!\n"
                self.id = conOb.CheckSignIn(username, password)
                self.flag = 1
            else:
                data = data + "0,Sign in fail!\n"
                self.flag = 0
        return data
    
    #----------------------------------------------------------------------
    def SignOut(self):
        self.flag = 0
        data = "You was sign out!\n"
        """"""
        return data
        
    #----------------------------------------------------------------------
    def isSignIn(self):
        """"""
        if self.flag == 1:
            return 1
        return 0
    
    #----------------------------------------------------------------------
    def ShowFriend(self,id):
        """"""
        data = ""
        if self.isSignIn():
            conOb = Conn()
            conOb.Open()
            data = data + conOb.Showfriend(id)
        else:
            data = data + "Ban chua dang nhap\n"
        return data
    
    #----------------------------------------------------------------------
    def EditInfoFriend(self,friend):
        """"""
        data = ""
        global c
        if self.isSignIn():
            data = data + self.ShowFriend(self.id)
            
            conOb = Conn()
            conOb.Open()
            id2 = conOb.TranNameToId(friend)
            if id2 > 0:
                data = data + "Tinh trang ban be hien tai: ,"
                if conOb.CheckBlock(self.id, id2) == 0:
                    data += "Friends\n"
                if conOb.CheckBlock(self.id, id2) == 1:
                    data += "Block\n"
                else:
                    data += "Close Friend\n"
                
                data +=  ("Nhap thay doi\n1.Block\n2.Boblock\n3.CloseFriend")
                c.sendall(data)
                choose = c.recv(1024)
                
                if choose == 1:
                    if (conOb.CheckBlock(self.id, id2) == 0):
                        conOb.UpdateStatusfriend(1, self.id, id2)
                        data = ("---------Block Successfuly---------\n")
                        conOb.Showfriend(self.id)
                    else:
                        data = ("Ban da block nguoi nay\n")
            
                if choose == 2:
                    if (conOb.CheckBlock(self.id, id2) )== 1 and (conOb.CheckWhoBlock(self.id,id2) == self.id):
                        conOb.UpdateStatusfriend(0, self.id, id2)
                        data = ("Ban da block nguoi nay\n")
                    else:
                        data = ("---Ban khong co quyen bo block hoac chua block---\n")
        
                if choose == 3:
                    conOb.UpdateStatusfriend(2, self.id, id2)
                    data = ("-----Ban than da duoc them-------\n")
            
            else:
                data = ("-----Tai khoan khon ton tai-----\n")
        else:
            data = ("---------Ban chua dang nhap.--------\n\n")
        
        c.sendall(data)
    
    #----------------------------------------------------------------------
    def AddFriend(self,id):
        """"""
        if self.isSignIn() == 1:
            newfr = raw_input("Nhap ten nguoi ban muon them: ")
            conOb = Conn()
            conOb.Open()
            id2 = conOb.TranNameToId(newfr)
            if id2 > 0:
                if conOb.CheckBlock(id, id2) == 0 and conOb.CheckFriend(id, id2) != 0:
                    conOb.WriteToFriend(id, id2)
                    conOb.Showfriend(id)
                else:
                    print("------You were blocked by her  or You was friend ----------\n\n")
              
            else:
                print("----Tai khoan khong ton tai-----------\n")
        else:
            print("---------Ban chua dang nhap.--------\n\n")
        
    
    #----------------------------------------------------------------------
    def ShowFriendByCity(self,id):
        """"""
        if self.isSignIn() == 1:
            conOb = Conn()
            conOb.Open()
            data = conOb.ShowFriendByCity(id)
        else: print ("Ban chua dang nhap\n")
        return data
    
    #----------------------------------------------------------------------
    def SendMess(self,id):
        """"""
        if self.isSignIn() == 1:
            conOb = Conn()
            conOb.Open()
            self.ShowFriend(id);
            namefr = raw_input("Nhap ten ban be: ")
            id2 = conOb.TranNameToId(namefr)
            if id2 > 0 :
                if(conOb.CheckBlock(id, id2) != 1):
                    mess = raw_input("Nhap tin nhan:")
                    import time
                    localtime = time.asctime(time.localtime(time.time()))
                    conOb.WriteToMess(id, id2, mess, localtime)
                else: 
                    print("Ban da bi block\n")
            else: 
                print("Tai khoan khong ton tai.\n")
    
    #----------------------------------------------------------------------
    def ShowMess(self,id):
        """"""
        if self.isSignIn() == 1:
            conOb = Conn()
            conOb.Open()
            conOb.SelectMessenger(id)
    
    
    
    #----------------------------------------------------------------------
    def ShowMessDetail(self,id1):
        """"""
        if self.isSignIn() ==1:
            frien = raw_input("Chon nguoi dung: ")
            conOb = Conn()
            conOb.Open()
            id2 = conOb.TranNameToId(frien)
            if id2 > 0:
                conOb.ShowMessDetail(id1, id2)
            else: 
                print("----Tai khoan khong ton tai----\n")
        
        
        
                        
def main():
    
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12349          # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port
    s.listen(5)
    
                    # Now wait for client connection.    
    use = User()
    global c
    c, addr = s.accept()
    while True:
        
        
        data = c.recv(1024)
        data = data.split(",")
        choose = (int) (data[0])
        
        print(choose)
        if choose == 1:
            c.sendall(use.SignUp(data[1],data[2],data[3]))
        if choose == 2:
            c.sendall(use.SignIn(data[1],data[2]) )
        
        if choose == 3:
            use.EditInfoFriend(data[1]) 
        if choose == 4:
            print("use id: ",use.id)
            c.sendall(use.ShowFriendByCity(use.id).encode())
        if choose == 5:
            c.sendall( use.SendMess(use.id) )
        if choose == 6:
            c.sendall(use.ShowMess(use.id))
        if choose == 7:
            c.sendall (use.ShowMessDetail(use.id))
    
    

        
if __name__ == '__main__':
    main()
        
        
        
