from tkinter import *
import tkinter.messagebox
import json
from StringData import *
from jahakWork import *
class WaitingRoom(Frame):
    def  __init__(self,master,resp):
        super().__init__(master)
        self.__tk = master
        sel.setNextScene = None
        if (not( "user_name" in resp)):
            resp["user_name"] = []
        if ( not ("computer_count" in resp)):
            resp["computer_count"] = 0
        if(not ('isRightDir' in resp)):
            resp['isRightDir']=True
        #self.pack(pady=20)
        self.__totalPlayerCount = 0
        self.__firstAccess = True
        self.__resp = {}
        for key in resp:
           self.__resp[key] = resp[key] 
        for previousName in resp['user_name']:
            self.__resp['user_name'].append(previousName)
        self.create_wdigets(self.__resp)
        
              
        
        
        
       
    
    
    def showDialogHadMinPlayer(self):
        tkinter.messagebox.showinfo(StringData.getDlgTitle_minPlayer(),StringData.getDlgContent_minPlayer())
    @property
    def result(self):
        return self.__resp

    def packList(self):
        size = self.listbox_playerlist.size()
        if('user_name' in self.__resp):
            self.__resp['user_name'].clear()
        else:
            self.__resp['user_name']=[]
        for i in range(size):
            self.__resp["user_name"].append(self.listbox_playerlist.get(i))
        return self.__resp        
    #def destroy(self):
    #    self.packList()
    #    super().destroy()   
    def getChoosePlayDiection_Frame(self,names,dirRespCarrier,createMode = False,master=None):
        self.people = names[:]
        self.peopleCount = len(self.people)
        if(createMode and master!=None):
            self.__cpdFrame=Frame(master)
            master.grid_rowconfigure(0, weight=1)
            master.grid_columnconfigure(0, weight=1)
            self.__cpdFrame.grid(row=0,column=0)
            self.__cpdFrame.pack(expand=True,fill=BOTH)
            self.cpd_create_widgets(self.__cpdFrame,dirRespCarrier)
            self.button1_clicks = 0
            self.button2_clicks = 0
        return self.__cpdFrame
        
    def cpd_create_widgets(self,frame,resp):
        initName = "none"
        if(len(self.people)!=0):
            initName = self.people[0]
            
        self.display = Label(frame, text="'"+initName+"'순서방향을 정해주십시오")
        self.display.grid(row=0, column=1)
        Label(frame, text=' ').grid(row=1,column=1)
        self.button1 = Button(frame)
        self.button1["text"] = "순방향"
        self.button1["command"] = lambda: self.cpd_update_count(frame,resp,1-1)
        self.button1.grid(row=2, column=0)
        self.button2 = Button(frame)
        self.button2['text'] = '역방향'
        self.button2['command'] = lambda: self.cpd_update_count(frame,resp,2-1)
        self.button2.grid(row=2, column=2)
        #Button(self, text="quit", command=self.quit).grid(row=4, column=2)
    def cpd_nextPlayer(self,frame,resp):
        if(self.people==[] or len(self.people)==1):
            self.cpd_end_sequence(frame,resp)
        else:
            self.people = self.people[1:]
            txt = self.display['text']
            after = txt[txt.index("'",1):]
            self.display['text'] = "'"+self.people[0]+after
    def cpd_update_count(self,frame,resp,which):
        if(not which):
            self.button1_clicks += 1
        else:
            self.button2_clicks += 1
        self.cpd_nextPlayer(frame,resp)
    def setNextScene(self,sc):
        self.__scene=sc
    def cpd_end_sequence(self,frame,resp):
        
        end_button = self.button1_clicks + self.button2_clicks
        isRightDir = True
        key_isRightDir = "isRightDir"
        if end_button == self.peopleCount : 
            if self.button1_clicks > self.button2_clicks :
                Label(frame, text='순방향으로 정하셨습니다').grid(row=3, column=1)
            elif self.button1_clicks < self.button2_clicks : 
                Label(frame, text='역방향으로 정하셨습니다').grid(row=3, column=1)
                isRightDir=False
            else : 
                la = [1,2]
                random.shuffle(la)
                if la[0] == 1 : 
                    Label(frame, text='순방향으로 정하셨습니다').grid(row=3, column=1)
                    
                else : 
                    Label(frame, text='역방향으로 정하셨습니다').grid(row=3, column=1)
                    isRightDir=False
        #self.__resp['isRightDir']=isRightDir
        resp[key_isRightDir] = isRightDir
        #frame.quit()
        #self.quit()
        #self.master.quit()
        self.__scene()
        print("endseq")
    
    def doSyncCkbEnableComputer(self):
        pass
    def doPlay(self):
        size = self.listbox_playerlist.size()
        if(size>1):
            self.__resp = self.packList()
            for chd in self.winfo_children():
                chd.destroy()
                del chd
            
            cpd = self.getChoosePlayDiection_Frame(self.__resp['user_name'],self.__resp,True,self) #ChoosePlayDirection(self,self.__resp['user_name'])
            
            
            cpd.pack(expand=True,fill=BOTH)
        else:
            self.showDialogHadMinPlayer()
        #self.destroy()
    def create_wdigets(self,resp=None):
        self.__lb1 = Label(self,text=StringData.getLableTitlePlayerCountHeader())
        self.__lb1.grid(row=0,column=0)
        self.label_totalPlayerCount= Label(self,justify=LEFT,text=str(self.__totalPlayerCount)+"명")
        self.label_totalPlayerCount.grid(row=0,column=1)
        self.__btn1 = Button(self,text=StringData.getBtnTxtPlayerDel(),command=self.delPlayer)
        self.__btn1.grid(row=0,column=3)
        self.listbox_playerlist = Listbox(self,selectmode="SINGLE",height=8,width=35)
        self.listbox_playerlist.grid(row=1,column=0,columnspan=4)
        self.entry_inputnewplayerName = Entry(self,width=20,justify=LEFT)
        self.entry_inputnewplayerName.grid(row=2,column=0,columnspan=2)
        self.__btn2 = Button(self,text=StringData.getBtnTxtPlayerAdd(),command=self.addPlayer)
        self.__btn2.grid(row=2,column=3)
        self.__btn3 = Button(self,text=StringData.getBtnTxtDoPlay(),command=self.doPlay)
        self.__btn3.grid(row=3,column=4)
        #self.__ckb_enable_computer = Checkbutton(master,text="컴퓨터 사용",command=self.doSyncCkbEnableComputer).
        if(resp!=None and type(resp)==list and self.__firstAccess == True):
            self.__firstAccess = False
            for prevName in resp:
                if(prevName != ''  ):
                    self.listbox_playerlist.insert(self.listbox_playerlist.size(),prevName)
                
            self.label_totalPlayerCount['text'] = str(self.listbox_playerlist.size())+StringData.getPeopleCountUnit()
        '''    
        if("user_name" in resp and resp["user_name"] != None and type(resp["user_name"]) == list and self.__firstAccess == True):
            self.__firstAccess = False
            
            tl = resp["user_name"]
            print ("enter",tl)
            for v in tl:
                print(v)
                if(v != ''  ):
                    self.listbox_playerlist.insert(self.listbox_playerlist.size(),v)
                    
            self.label_totalPlayerCount['text'] = str(self.listbox_playerlist.size())+StringData.getPeopleCountUnit()
            #resp["user_name"].clear()    
        '''
        self.entry_inputnewplayerName.bind("<Return>",self.addPlayer)
        self.pack(padx=20,pady=20)
        #self.resizeWindowSize()
    #def eventInput(self,event):
    #    self.addPlayer()
    
    def delPlayer(self):
        idx = self.listbox_playerlist.curselection()
        if(idx != ()):
            self.listbox_playerlist.delete(idx)
            self.label_totalPlayerCount['text'] = str(self.listbox_playerlist.size())+StringData.getPeopleCountUnit()
            
    def addPlayer(self,event=None):
        pname = self.entry_inputnewplayerName.get()
        if(pname == '' or pname == []):
            tkinter.messagebox.showinfo(StringData.getErrorText(),StringData.getUserNameEmptyErrorMsgBoxContent())
        else:
            size = self.listbox_playerlist.size()
            hasSamePlayer = False
            for i in range(size):
                if(pname == self.listbox_playerlist.get(i)):
                    hasSamePlayer = True
                    break
            if(hasSamePlayer):
                tkinter.messagebox.showinfo(StringData.getDlgTitle_existRegisteredPlayer(),StringData.getDlgContent_existRegisteredPlayer())
            elif(size>7):
                tkinter.messagebox.showinfo(StringData.getDlgTitle_maxPlayer(),StringData.getDlgContent_maxPlayer())
            else:
                self.listbox_playerlist.insert(self.listbox_playerlist.size(),pname)
                self.label_totalPlayerCount['text'] = str(self.listbox_playerlist.size())+StringData.getPeopleCountUnit()
            
        self.entry_inputnewplayerName.delete(0,END)
class InputViews:
    @staticmethod
    def getPlayerNameList():
        response = {}
        root = Tk()
        root.title("Waiting Room")
        WaitingRoom(root,response)
        root.mainloop()
        return response
    @staticmethod
    def getPlayerNameListWithParam(resp):
        
        root = Tk()
        root.title("Waiting Room")
        WaitingRoom(root,resp)
        root.mainloop()
        return resp

def main():
    root = Tk()
    playerNameList = {}
    playerNameList = InputView.getPlayerNameList()
    while(playerNameList["user_name"] == [] or not ( 2<=len(playerNameList["user_name"])<=8)):
        playerNameList = InputView.getPlayerNameListWithParam(playerNameList)
    print(playerNameList)
#main()
