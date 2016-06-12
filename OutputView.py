from tkinter import *
import threading
from Deck import *
#from Util import *
from Player import *
from Util import *
import tkinter.messagebox
import hoonWork
from test.test_dynamicclassattribute import PropertyDel

class OutputView(Frame):

    @staticmethod
    def configKeyList():
        return ["nextTurnCmd","popCardsCmd","deckShuffleCmd","deckSortCmd","initPlayerCardFrames","initPlayerPublicCardFrames","initPlayerNames","initWidgetRefreshView"]
    def __init__(self,master):
        super().__init__(master)
        configKeyList = OutputView.configKeyList()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.porderlv=None
        self.__topframe=None
        self.pranklv=None
        self.__configs={key:None for key in configKeyList}
        self.frame5container=None
        self.frame2container=None
        self.pack(fill=BOTH,padx=10,pady=10,expand=True)
    #def setPlayerLists(self):
    @property
    def internalConfigs(self):
        return self.__configs
    def setInternalConfigs(self,karg):
        for key in karg:
            self.__configs[key] = karg[key]
    @property
    def topFrame(self):
        return self.__topframe
    @property
    def orderListView(self):
        return self.porderlv
    @property
    def rankListView(self):
        return self.pranklv
    @property
    def preparingFrame(self):
        return self.__preparingFrame
    def create_widgets(self):
        
        self.__topframe = PanedWindow(self,orient=VERTICAL)
        self.__topframe.pack(fill=BOTH,anchor=CENTER,expand=True)
        self.__topframe.grid(row=0,column=0,sticky="news")

        frame4 = PanedWindow(self.__topframe)
        topcardframe = Frame(self.__topframe)
        bottomcardframe = Frame(self.__topframe)
        self.frame5container = Canvas(bottomcardframe,scrollregion=(0,0,1500,0))
        self.frame5 = Frame(self.frame5container)
        self.frame5.pack(fill=BOTH,expand=TRUE,padx=10)
        xscoller= Scrollbar(bottomcardframe,orient=HORIZONTAL,command=self.frame5container.xview)
        xscoller.pack(side=BOTTOM,fill=X,padx=10)
        self.frame5container.create_window((0,0), window=self.frame5, anchor=NW)
        self.frame5container.pack(fill=BOTH,expand=TRUE)
        self.frame5container.configure(xscrollcommand=xscoller.set)
        self.frame5container.create_oval(0,0,400,300,fill='red')
        self.frame2container = Canvas(topcardframe,scrollregion=(0,0,1500,0))
        frame2 = Frame(self.frame2container)
        frame2.pack(fill=BOTH,expand=TRUE)
        xscollertop= Scrollbar(topcardframe,orient=HORIZONTAL,command=self.frame2container.xview)
        xscollertop.pack(side=BOTTOM,fill=X,padx=10)

        self.frame2container.create_window((0,0), window=frame2, anchor=NW)
        self.frame2container.pack(side=TOP,fill=X,padx=10)
        self.frame2container.configure(xscrollcommand=xscollertop.set)
        
        self.__topframe.add(topcardframe,stretch="always")
        self.__topframe.add(frame4,stretch="always")
        self.__topframe.add(bottomcardframe,stretch="always")
        playerorderFrame = PanedWindow(frame4,orient=VERTICAL)
        playerRankFrame = PanedWindow(frame4,orient=VERTICAL)
        middleFrame = PanedWindow(frame4)
        
        self.porderlv = Listbox(playerorderFrame,selectmode=NONE,height=8,width=20)
        self.pranklv = Listbox(playerRankFrame,selectmode=NONE,height=8,width=22)
        playerorderFrame.add(Label(playerorderFrame,text="플레이어 순서"))
        playerRankFrame.add(Label(playerRankFrame,text="플레이어 현재 랭킹"))
        playerorderFrame.add(self.porderlv)
        playerRankFrame.add(self.pranklv)
        frame4.add(playerorderFrame,stretch="always")
        frame4.add(middleFrame,stretch="always")
        frame4.add(playerRankFrame,stretch="always")

        self.__preparingFrame = Frame(frame2)
        #self.__preparingFrame.pack(fill=X,expand=TRUE)
        self.__preparingFrame.pack(fill=X,expand=TRUE)
        self.__preparingFrame.grid(row=0,column=0,stick="news")
        Label(self.__preparingFrame,text="모든 플레이어들의 패에서 중복 숫자를 가진 카드들이  없을때 까지 기다리는중...").grid(row=0,column=0,columnspan=3)

        #self.__preparingFrame.pack()
        playerControllView = PanedWindow(middleFrame,orient=VERTICAL)
        playerControllView.add(Button(middleFrame,text="턴넘기기 ",command=self.__configs[OutputView.configKeyList()[0]]),stretch="always")
        playerControllView.add(Button(middleFrame,text="선택한 카드 버리기 ",command=self.__configs[OutputView.configKeyList()[1]]),stretch="always")
        playerControllView.add(Button(middleFrame,text="패 섞기 ",command=self.__configs[OutputView.configKeyList()[2]]),stretch="always")
        playerControllView.add(Button(middleFrame,text="패 정렬",command=self.__configs[OutputView.configKeyList()[3]]),stretch="always")
        middleFrame.add(playerControllView,stretch="always")
        initNames = self.__configs[OutputView.configKeyList()[6]]
        for i in range(len(initNames)):
            self.porderlv.insert(self.porderlv.size(),initNames[i])
            (self.__configs[OutputView.configKeyList()[4]])[i](parent=self.frame5,mgcls=self ,rootCanvas=self.frame5container)
            (self.__configs[OutputView.configKeyList()[5]])[i](parent=frame2,mgcls=self,rootCanvas=self.frame2container)
           
        self.__configs[OutputView.configKeyList()[7]]() 
        #self.refreshDisplayedCardFrame()
        #self.refreshPlayerRank()
        #self.__topframe.pack(fill=BOTH,expand=TRUE)
        self.frame5container.configure(scrollregion = self.frame5container.bbox("all"))
        self.frame2container.configure(scrollregion = self.frame2container.bbox("all"))
        self.doThread(self.frame5container,self.frame2container)
    def threadWork(self,f5c,f2c):#complete
        import time
        time.sleep(0.2)
        f5c.configure(scrollregion = f5c.bbox("all"))
        f2c.configure(scrollregion = f2c.bbox("all"))
    def doThread(self,f5c,f2c):#complete
        t = threading.Thread(target=self.threadWork ,args=(f5c,f2c,))
        t.start()
    @staticmethod
    def showGUI():
        window = Tk()
        screen_width = int(window.winfo_screenwidth()*0.97)
        screen_height = int(window.winfo_screenheight()*0.95)
        window.geometry(str(screen_width)+"x"+str(screen_height))
        
        ov = OutputView(window)
        return ov
        #window.mainloop()