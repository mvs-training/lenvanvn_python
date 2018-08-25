import sqlite3 
import sys
import os
class ConnectSQL:
    path = None
    con = None
    cur = None 
    
    #----------------------------------------------------------------------
    def  Open(self):
        ConnectSQL.path = os.path.dirname(__file__) + "/We4.db"
        ConnectSQL.con = sqlite3.connect(ConnectSQL.path)   
        ConnectSQL.cur = self.con.cursor()
    
    #----------------------------------------------------------------------    
    def SignUp(self,username, password, city):
        cur = ConnectSQL.con.cursor() 
        cur.execute("insert into User (username, password,city) values (?,?,?)", (username, password, city)) 
        print ("successfuly!\n")
        
    
    #----------------------------------------------------------------------
    def CheckCity(self,city):
        hascity = 0
        cur = ConnectSQL.con.cursor() 
        cur.execute("SELECT idc FROM city WHERE name = ? ", (city,) )
        row = cur.fetchone()
        if row != None:
            hascity = 1
        return hascity
     #----------------------------------------------------------------------
    def WriteToCity(self,name):
        sql = "INSERT INTO city(name) VALUES(?) "
        
        ConnectSQL.cur.execute(sql,(name,))
    
     #----------------------------------------------------------------------
    def TranCityToId(self,city):
        
        sql = "SELECT idc FROM city WHERE name = ?"
        self.cur.execute(sql,(city,))
        row = self.cur.fetchone()
        return row[0]
     #----------------------------------------------------------------------
    def CheckSignIn(self,user, passw):
        sql = "SELECT * FROM  user WHERE username = ? and password = ?"
        self.cur.execute(sql,(user,passw))
        row = self.cur.fetchone()
        if row == None :
            return -1
        return row[0]
    
    #----------------------------------------------------------------------
    
    def Showfriend(self,id):
        """"""
        data = ""
        print ("-------List Friends-----------\n")
        sql = "SELECT DISTINCT user.username FROM"\
              "(SELECT * FROM friend where (id1 = ? OR id2 = ?)"\
              "AND RelationshipStatus != 1 )  as A LEFT JOIN user ON \
              (A.id2 = user.id OR A.id1 = user.id)"
        self.cur.execute(sql,(id,id))
        row = self.cur.fetchone()
        while row!= None:
            data = data+ row[0] +","
            row= self.cur.fetchone()
        return data
            
    #----------------------------------------------------------------------
    def TranNameToId(self,frien):
        """"""
        
        sql = "SELECT id FROM User WHERE username = ?"
        self.cur.execute(sql,(frien,))
        row = self.cur.fetchone()  
        if row == None:
            return -1
        return row[0]
    
    #----------------------------------------------------------------------
    def CheckBlock(self,id1,id2):
        """"""
        isblock = 0
        sql = "SELECT RelationshipStatus FROM Friend WHERE (id1 = ? AND id2 = ?) OR (id1 = ? AND id2 = ?)"
        self.cur.execute(sql,(id1,id2,id2,id1))
        row = self.cur.fetchone()
        isblock = row[0]
        return isblock
    
    #----------------------------------------------------------------------
    def UpdateStatusfriend(self,status,id1,id2):
        
        """"""
        who = 0
        if status == 1:
            who = id1
        sql = "UPDATE Friend SET RelationshipStatus = ? , whoblock = ? WHERE (id1 = ? AND id2 = ?) OR (id1 = ? AND id2 = ?)"
        cur = ConnectSQL.con.cursor() 
        self.cur.execute(sql,(status,who,id1,id2,id2,id1))
        
    #----------------------------------------------------------------------
    def CheckWhoBlock(self,id1,id2):
        """"""
        whoblock = 0
        sql = "SELECT whoblock FROM Friend WHERE (id1 = ? AND id2 = ?) OR (id1 = ? AND id2 = ?)"
        self.cur.execute(sql,(id1,id2,id1,id2))
        row = self.cur.fetchone()
        whoblock = row[0]
        return whoblock
    
    #----------------------------------------------------------------------
    def CheckFriend(self,id,id2):
        """"""
        sql = "SELECT * FROM Friend WHERE ( id1 = ? AND id2 = ?) OR ( id1 = ? AND id2 = ?)"
        self.cur.execute(sql,(id,id2,id2,id))
        row = self.cur.fetchone()
        if row is not None:
            return 1
        return 0
    
    #----------------------------------------------------------------------
    def WriteToFriend(self,id1,id2):
        """"""
        sql = "INSERT INTO Friend VALUES (?,?,?,?,?)"
        import time
        localtime = time.asctime(time.localtime(time.time()))
        self.cur.execute(sql,(id1,id2,localtime,0,0))
     
    #----------------------------------------------------------------------
    def TranIdtoCity(self,id):
        """"""
        sql = "SELECT name FROM city WHERE idc = ?"
        self.cur.execute(sql,(id,))
        row = self.cur.fetchone()
        return row[0]
        
    #----------------------------------------------------------------------
    def TranIdtoUser(self,id):
        """"""
        sql = "SELECT username FROM User WHERE id = ?"
        self.cur.execute(sql,(id,))
        row = self.cur.fetchone()
        return row[0]
        
    #----------------------------------------------------------------------
    def ShowFriendByCity(self,id):
        """"""
        data = ""
        sql = "SELECT city.idc,User.id FROM city, User,Friend WHERE (Friend.id1 = ? or Friend.id2 = ?) and (User.id = Friend.id1 or User.id = Friend.id2)  and User.city = city.idc and User.id != ?"
        self.cur.execute(sql,(id,id,id))
        row = self.cur.fetchone()
        city = dict()
        while row != None:
            idc = row[0]
            idu = row[1]
            if city.get(row[0]) is None:
                city[idc] = [idu]
            else:
                city[idc].append(idu)
            row = self.cur.fetchone()
        
        for x in city:
            namecity = self.TranIdtoCity(x)
            data = data + str(namecity) + ","
            print ("City %s \n: ", namecity)
            print ("Danh sach ban be: ")
            dem = 1;
            for y in city[x]:
                nameuser = self.TranIdtoUser(y)
                print(dem,".",nameuser,"\n")
                data = data + str(nameuser)+ ","
                dem = dem+1
            print("\n\n")
            
            data = data +"."
            print (data)
        return data
    
    #----------------------------------------------------------------------
    def WriteToMess(self,id1,id2,mess,time):
        """"""
        sql = "INSERT INTO messenger VALUES (?,?,?,?,1)"
        self.cur.execute(sql,(id1,id2,mess,time))
        
    
    #----------------------------------------------------------------------
    def SelectMessenger(self,id):
        """"""
        sql = "SELECT DISTINCT user.username FROM" \
                "(SELECT * FROM messenger where idsen = ? ) as A LEFT JOIN user ON A.idrec = user.id"
        self.cur.execute(sql,(id,))
        row = self.cur.fetchone()
        print ("Danh sach tin nhan: \n")
        dem = 1
        while row is not None:
            print (dem,".", row[0], "\n")
            row = self.cur.fetchone()
    
    
    #----------------------------------------------------------------------
    def ShowMessDetail(self,id1,id2):
        """"""
        print("---------Detail-----\n")
        sql = "SELECT User.username, B.contend, B.time FROM (SELECT * FROM messenger WHERE (idsen = ? OR idsen = ?) AND (idrec = ? OR idrec =?) ) AS B LEFT JOIN  user ON user.id = B.idsen"
        self.cur.execute(sql,(id1,id2,id1,id2))
        row = self.cur.fetchone()
        while row != None:
            print(row[0], ":\n")
            print (row[1], "-",row[2],"\n")
            row = self.cur.fetchone()
        
            
            
        
        
        
        
