from tkinter import *
from StringData import *
class InputView:
    @staticmethod
    def getWaitingRoomFrameWithRspParam(master,resp):
        result = Frame(master)
        iv = InputView()
        iv.wr_init(result,master,resp)
        return result
    def wr_init(self,frame,master,resp):
        frame.tk = master
        #self.pack(pady=20)
        frame.totalPlayerCount = 0
        frame.firstAccess = True
        self.__wr_create_wdigets(frame,resp)
        if (not( "user_name" in resp)):
            resp["user_name"] = []
        if ( not ("computer_count" in resp)):
            resp["computer_count"] = 0
        if(not ('user_name' in resp)):
            resp['user_name']=[]
        frame.resp = resp
        
    def wr_doPlay(self,frame):
        size = frame.listbox_playerlist.size()
        if(size>1):
            frame.resp = self.wr_packList(frame)
            for chd in frame.winfo_children():
                chd.destroy()
                del chd
            
            cpd = self.getChoosePlayDiection_Frame(frame,frame.resp['user_name'],frame.resp,True,frame) #ChoosePlayDirection(self,self.resp['user_name'])
            cpd.pack(expand=True,fill=BOTH)
        else:
            self.showDialogHadMinPlayer()
    def __cpd_init(self,frame,master,playerNames):
        frame.pack(padx=10, pady=10)
        frame.button1_clicks = 0
        frame.button2_clicks = 0
        frame.end_button = 0
        frame.people = playerNames
        frame.peopleCount = len(playerNames)
        #self.create_widgets()
    def getChoosePlayDiection_Frame(self,frame,names,dirRespCarrier,createMode = False,master=None):
        frame.people = names[:]
        frame.peopleCount = len(frame.people)
        if(createMode):
            frame.cpdFrame=Frame(frame)
            self.__cpd_init(frame.cpdFrame,frame,names)
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.cpdFrame.grid(row=0,column=0)
            frame.cpdFrame.pack(expand=True,fill=BOTH)
            self.cpd_create_widgets(frame,frame.cpdFrame,dirRespCarrier)
            #frame.button1_clicks = 0
            #frame.button2_clicks = 0
        return frame.cpdFrame
        
    def wr_packList(self,frame):
        size = frame.listbox_playerlist.size()
        if('user_name' in frame.resp):
            frame.resp['user_name'].clear()
        else:
            frame.resp['user_name']=[]
        for i in range(size):
            frame.resp["user_name"].append(frame.listbox_playerlist.get(i))
        return frame.resp 
    def showDialogHadMinPlayer(self):
        tkinter.messagebox.showinfo(StringData.getDlgTitle_minPlayer(),StringData.getDlgContent_minPlayer())
    def __wr_create_wdigets(self,frame,resp=None):
        frame.lb1 = Label(frame,text=StringData.getLableTitlePlayerCountHeader())
        frame.lb1.grid(row=0,column=0)
        frame.label_totalPlayerCount= Label(frame,justify=LEFT,text=str(frame.totalPlayerCount)+"명")
        frame.label_totalPlayerCount.grid(row=0,column=1)
        frame.btn1 = Button(frame,text=StringData.getBtnTxtPlayerDel(),command=lambda: self.wr_delPlayer(frame))
        frame.btn1.grid(row=0,column=3)
        frame.listbox_playerlist = Listbox(frame,selectmode="SINGLE",height=8,width=35)
        frame.listbox_playerlist.grid(row=1,column=0,columnspan=4)
        frame.entry_inputnewplayerName = Entry(frame,width=20,justify=LEFT)
        frame.entry_inputnewplayerName.grid(row=2,column=0,columnspan=2)
        frame.btn2 = Button(frame,text=StringData.getBtnTxtPlayerAdd(),command=lambda: self.wr_addPlayer(frame))
        frame.btn2.grid(row=2,column=3)
        frame.btn3 = Button(frame,text=StringData.getBtnTxtDoPlay(),command=lambda:self.wr_doPlay(frame))
        frame.btn3.grid(row=3,column=4)
        #frame.ckb_enable_computer = Checkbutton(master,text="컴퓨터 사용",command=frame.doSyncCkbEnableComputer).
        if("user_name" in resp and resp["user_name"] != None and type(resp["user_name"]) == list and frame.firstAccess == True):
            frame.firstAccess = False
            
            tl = resp["user_name"]
            print ("enter",tl)
            for v in tl:
                print(v)
                if(v != ''  ):
                    frame.listbox_playerlist.insert(frame.listbox_playerlist.size(),v)
                    
            frame.label_totalPlayerCount['text'] = str(frame.listbox_playerlist.size())+StringData.getPeopleCountUnit()
            #resp["user_name"].clear()    
        frame.entry_inputnewplayerName.bind("<Return>",lambda event:self.addPlayer(frame,event))
        frame.pack(padx=20,pady=20)
        
    def wr_delPlayer(self,frame):
        idx = frame.listbox_playerlist.curselection()
        if(idx != ()):
            frame.listbox_playerlist.delete(idx)
            frame.label_totalPlayerCount['text'] = str(frame.listbox_playerlist.size())+StringData.getPeopleCountUnit()
            
    def wr_addPlayer(self,frame,event=None):
        pname = frame.entry_inputnewplayerName.get()
        if(pname == '' or pname == []):
            tkinter.messagebox.showinfo(StringData.getErrorText(),StringData.getUserNameEmptyErrorMsgBoxContent())
        else:
            size = frame.listbox_playerlist.size()
            hasSamePlayer = False
            for i in range(size):
                if(pname == frame.listbox_playerlist.get(i)):
                    hasSamePlayer = True
                    break
            if(hasSamePlayer):
                tkinter.messagebox.showinfo(StringData.getDlgTitle_existRegisteredPlayer(),StringData.getDlgContent_existRegisteredPlayer())
            elif(size>7):
                tkinter.messagebox.showinfo(StringData.getDlgTitle_maxPlayer(),StringData.getDlgContent_maxPlayer())
            else:
                frame.listbox_playerlist.insert(frame.listbox_playerlist.size(),pname)
                frame.label_totalPlayerCount['text'] = str(frame.listbox_playerlist.size())+StringData.getPeopleCountUnit()
            
        frame.entry_inputnewplayerName.delete(0,END)
        
    def cpd_create_widgets(self,topframe,frame,resp):
        initName = "none"
        if(len(frame.people)!=0):
            initName = frame.people[0]
            
        frame.display = Label(frame, text="'"+initName+"'순서방향을 정해주십시오")
        frame.display.grid(row=0, column=1)
        Label(frame, text=' ').grid(row=1,column=1)
        frame.button1 = Button(frame)
        frame.button1["text"] = "순방향"
        frame.button1["command"] = lambda: self.cpd_update_count(topframe,frame,resp,1-1)
        frame.button1.grid(row=2, column=0)
        frame.button2 = Button(frame)
        frame.button2['text'] = '역방향'
        frame.button2['command'] = lambda: self.cpd_update_count(topframe,frame,resp,2-1)
        frame.button2.grid(row=2, column=2)
        #Button(self, text="quit", command=self.quit).grid(row=4, column=2)
    def cpd_nextPlayer(self,topframe,frame,resp):
        if(frame.people==[] or len(frame.people)==1):
            self.cpd_end_sequence(topframe,frame,resp)
        else:
            frame.people = frame.people[1:]
            txt = frame.display['text']
            after = txt[txt.index("'",1):]
            frame.display['text'] = "'"+frame.people[0]+after
    def cpd_update_count(self,topframe,frame,resp,which):
        if(not which):
            frame.button1_clicks += 1
        else:
            frame.button2_clicks += 1
        self.cpd_nextPlayer(topframe,frame,resp)
    
    def cpd_end_sequence(self,topframe,frame,resp):
        
        end_button = frame.button1_clicks + frame.button2_clicks
        isRightDir = True
        key_isRightDir = "isRightDir"
        if end_button == frame.peopleCount : 
            if frame.button1_clicks > frame.button2_clicks :
                Label(frame, text='순방향으로 정하셨습니다').grid(row=3, column=1)
            elif frame.button1_clicks < frame.button2_clicks : 
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
        #self.resp['isRightDir']=isRightDir
        resp[key_isRightDir] = isRightDir
        topframe.quit()    
    
    @staticmethod
    def getPlayerNameList():
        response = {}
        root = Tk()
        root.title("Waiting Room")
        wr= InputView.getWaitingRoomFrameWithRspParam(root,response)
        root.mainloop()
        return response
    @staticmethod
    def getPlayerNameListWithParam(resp):
        root = Tk()
        root.title("Waiting Room")
        wr = InputView.getWaitingRoomFrameWithRspParam(root,resp)
        root.mainloop()
        return resp
def main():
    playerNameList = {}
    playerNameList = InputView.getPlayerNameList()
    while(playerNameList["user_name"] == [] or not ( 2<=len(playerNameList["user_name"])<=8)):
        playerNameList = InputView.getPlayerNameListWithParam(playerNameList)
    print(playerNameList)
main()