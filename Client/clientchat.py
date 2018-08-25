
class User:
    
    def __init__(self):
        self.id = 1
        self.username = 1
        self.password = 1
        self.city = 1
        self.flag = None
    
    #----------------------------------------------------------------------
    def SignUp(self):
        print ("-------Dien cac thong tin de dang ky!-------\n")
        username = raw_input()
        
        
        password = raw_input()
        
        city = raw_input()
        
        print (password)
        print (username)
        print (city)
        data = ""
        data = data + "1,"+username+","+password + "," +city
        return data
        
            
    #----------------------------------------------------------------------
    def SignIn(self):
        
        username = raw_input("Nhap vao usernam: \n")
        password = raw_input("Nhap vao password: \n")
        data = ""
        data = data +"2,"+username +"," +password
        return data
  
    #----------------------------------------------------------------------
    def SignOut(self):
        self.flag = 0
        print ("You was sign out!\n")
        """"""
               
    #----------------------------------------------------------------------
    def EditInfoFriend(self):
        """"""
        data = ""
        friend = raw_input("Nhap vao ten ban be can chinh sua: ")
        data += friend
        
        
    
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
    def ShowFriendByCity(self):
        data = "4,"
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
        
        
        
                        

        
        
        
