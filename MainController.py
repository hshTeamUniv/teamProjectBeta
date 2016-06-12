from Deck import *
from Player import *
from Card import *
from OutputView import *
from tkinter import *
class MainController:
    def __init__(self,playerNames,direction):
        players = [Player(name) for name in playerNames]
        self.setDirectionAndSetNames(players,direction)
        #self.direction = direction
        #players = self.chooseDirection(players,direction)
        #self.__playerNames = [p.name for p in players ]
        self.__players={p.name:p for p in players}
        self.__failFrame=None
        self.__recordRank=[]
        
    def chooseDirection(self,playerNameList,dir=True):
        if(len(playerNameList)>2 and dir == False):
            temp = playerNameList[1:]
            temp.reverse()
            playerNameList=[playerNameList[0]]+temp
            return playerNameList
        else:
            return playerNameList

    def distributeCardToPlayers(self,players,deck):#complete
        deck.shuffle()
        idx = 0
        playercount = len(players)
        while(deck!=[]):
            idx %=playercount
            players[idx].importCard(deck[0])
            idx += 1
            deck = deck[1:]
        
        return players
    
    def setDirectionAndSetNames(self,tempplayers,direction=True):
        self.direction = direction
       # players = [Player(name) for name in playerNames]
        players = self.chooseDirection(tempplayers,direction)
        self.__playerNames = [p.name for p in players ]
    def getPlayerOrder(self,pnames):
        result = ""
        for i in range(len(pnames)):
            result += pnames[i]+"\n"
        return result
    def moveListOrder(self,listv):#complete
        if(type(listv) == list and listv!=[]):
            listv = listv[1:]+[listv[0]]
        return listv
    def shuffleCurrentHand(self):
        #print(self.__players[self.__playerNames[0]].getDeck()[0])
        print("sch")
        self.__players[self.__playernamesIngame[0]].shuffleDeck()
        self.__players[self.__playernamesIngame[0]].getCardFrame().update()
        
    def sortCurrentHand(self):
        self.__players[self.__playernamesIngame[0]].sortDeck()
        self.__players[self.__playernamesIngame[0]].getCardFrame().update()
        
    def isDropCardMode(self):#complete
        c=False
        for pn in self.__playernamesIngame:
            b=self.__players[pn].hasSameLevelCard
            print(b)
            c= (c or b)
        if(not c and self.isDropCardsMode):
            self.isDropCardsMode=False
        if(not self.isDropCardsMode):    
            return False
        return c
    def checkPublicFrameNeedToDisable(self,publicframe):#complete
        if(self.isPlayerPoppedCard):
            for chd in publicframe.winfo_children():
                chd.configure(state='disable')
             
    def refreshDisplayedCardFrame(self):#noc
        print("rdcf")
        pn=self.__playernamesIngame
        if(len(self.ov.winfo_children())>0 and self.__failFrame==None):
            self.__players[pn[0]].getCardFrame().tkraise()
            if(len(pn)>1):
                if(self.isDropCardMode()):
                    self.ov.preparingFrame.tkraise()
                else:
                    pcf=self.__players[pn[1]].getPublicCardFrame()
                    pcf.tkraise()
                    self.checkPublicFrameNeedToDisable(pcf)   
    def ExistRemoveablePlayer(self):#complete
        #self.__playernamesIngame =self.__playernamesIngame
        if(len(self.__playernamesIngame) >1 and len(self.__players[self.__playernamesIngame[1]].getDeck() )==0  and self.__failFrame==None and len(self.ov.winfo_children())>0):
            #현재 플레이어가 다음 플레이어의 마지막으로 남은 1장을 뽑아 다음 플레이어의 순서가 필요없어진경우 플레이어제거  
            name = str(self.__playernamesIngame[1])
            remaincardcount = str(len(self.__players[self.__playernamesIngame[1]].getDeck()))
            self.__playernamesIngame.remove(self.__playernamesIngame[1])
            self.ov.porderlv.delete(1)
            self.__recordRank.append(name+"\n"+remaincardcount)
        if(len(self.__playernamesIngame) >0 and len(self.__players[self.__playernamesIngame[0]].getDeck() )==0 and len(self.ov.winfo_children())>0):
            name = str(self.__playernamesIngame[0])
            remaincardcount = str(len(self.__players[name].getDeck()))
            self.__playernamesIngame = self.__playernamesIngame[1:]
            self.ov.porderlv.delete(0)
            self.__recordRank.append(name+"\n"+remaincardcount)
        if(len(self.__playernamesIngame)==1):
            for fr in self.ov.winfo_children():
                fr.destroy()
            self.__failFrame = hoonWork.FailFrame(self.ov,self.__playernamesIngame[0]).setName(self.__playernamesIngame[0])
            self.__failFrame.tkraise()
            
    def refreshPlayerRank(self): #complete
        if(self.__failFrame==None and len(self.ov.winfo_children())>0):
            playerns = self.__playernamesIngame
            players=self.__players
            stackrank = self.__recordRank
            temprst = {}
            for i in range(len(playerns)):
                p=players[playerns[i]]
                if(not len(p.getDeck()) in temprst):
                    temprst[len(p.getDeck())] = []
                temprst[len(p.getDeck())].append(p.name)
            keys = list(temprst.keys())
            keys.sort()
            rst = []
            self.ov.pranklv.delete(0, max(self.ov.pranklv.size()-1,0))
            for sr in stackrank:
                name,count=sr.split('\n')
                self.ov.pranklv.insert( self.ov.pranklv.size(),(name +", "+str(count)+"장"))
            for k in keys:
                for n in temprst[k]:
                    self.ov.pranklv.insert( self.ov.pranklv.size(),(n +", "+str(k)+"장"))
            print("rpr")
    
    def transmitCard(self,card,nextTurn=False):#noc
        self.__players[self.__playernamesIngame[0]].importCard(card)
        self.isPlayerPoppedCard=True
        self.setUserPullCardState(True)
        if(nextTurn):
            self.changeText()
    def setUserPullCardState(self,isPulled):
        self.isUserPulledCard=isPulled
        
    def changeText(self,forceMode=False):
        if(not self.isPlayerPoppedCard and not (self.isDropCardsMode or forceMode)):
            tkinter.messagebox.showinfo("error","상대 카드를 뽑아주십시오.")
        elif(len(self.__playernamesIngame)>0 and (self.__players[self.__playernamesIngame[0]].hasSameLevelCard) and not(forceMode or self.isDropCardsMode)):
            tkinter.messagebox.showinfo("error","버릴 수 있는 카드가 존재합니다")
        else:
            self.isUserPulledCard=False
            self.nextPlayerOrder(True)
    def nextPlayerOrder(self,lvChange=False):
        self.isPlayerPoppedCard=False
        #self.__playernamesIngame=self.__playernamesIngame
        if(len(self.__playernamesIngame) >0 and len(self.__players[self.__playernamesIngame[0]].getDeck() )==0 and self.__failFrame==None and len(self.ov.winfo_children())>0):
            self.__playernamesIngame = self.__playernamesIngame[1:]
        else:
            self.__playernamesIngame=self.moveListOrder(self.__playernamesIngame)
            if(lvChange):
                self.ov.porderlv.insert(self.ov.porderlv.size(),self.ov.porderlv.get(0))
        self.__players[self.__playernamesIngame[0]].getCardFrame().tkraise()
        if(len(self.__playernamesIngame)>1 and self.__failFrame==None):
            if(self.isDropCardMode()):
                self.ov.preparingFrame.tkraise()
            else:
                self.__players[self.__playernamesIngame[1]].getPublicCardFrame().tkraise()
            
        if(lvChange and len(self.ov.winfo_children())>0):
            self.ov.porderlv.delete(0)
        return self.__playernamesIngame
    def popCards(self):
        p = self.__players[self.__playernamesIngame[0]]
        if(self.isDropCardsMode):
            isSuccess = p.delSelectedCardsFromFrame()
            #self.isPlayerPoppedCard = isSuccess
            if(isSuccess):
                self.nextPlayerOrder(True)
        else:
            
            isSuccess = p.delSelectedCardsFromFrame()
            print("self.isPlayerPoppedCard",self.isPlayerPoppedCard)
            if(not self.isPlayerPoppedCard):
                self.isPlayerPoppedCard = isSuccess
            
            self.refreshDisplayedCardFrame()
    def initWidgetRefreshView(self):
        self.refreshDisplayedCardFrame()
        self.refreshPlayerRank()
    def play(self):#noc
        ovconfig = {}
        OV_ConfigKeys= OutputView.configKeyList()
        self.isPlayerPoppedCard=False
        self.isUserPulledCard=False
        self.isDropCardsMode=True
        if(self.__failFrame!=None):
            try:
                self.__failFrame.destroy()
            except:
                pass
            self.__failFrame=None
        self.__recordRank.clear()
        
        isDropCardsMode=True
        self.__playernamesIngame = self.__playerNames[:]
        ovconfig[OV_ConfigKeys[4]] = []
        ovconfig[OV_ConfigKeys[5]] = []
        ovconfig[OV_ConfigKeys[6]] = self.__playernamesIngame[:]
        ovconfig[OV_ConfigKeys[7]]=self.initWidgetRefreshView
        playerframeconfig={}
        playerframeconfigKeys = Player.someInternalConfigKeys()
        playerframeconfig[playerframeconfigKeys[0]] = self.ExistRemoveablePlayer
        playerframeconfig[playerframeconfigKeys[1]] = self.refreshPlayerRank
        playerframeconfig[playerframeconfigKeys[2]] = self.refreshDisplayedCardFrame
        playerframeconfig[playerframeconfigKeys[3]] = self.transmitCard
        for name in self.__playernamesIngame:
            p = self.__players[name]
            p.setFrameConfigs(playerframeconfig)
            p.getDeck().clear()
            ovconfig[OV_ConfigKeys[4]].append(p.getCardFrame)
            ovconfig[OV_ConfigKeys[5]].append(p.getPublicCardFrame)
        deck = Deck()
        players = [self.__players[name] for name in self.__playernamesIngame]
        self.distributeCardToPlayers(players,deck)
        
        
        self.ov = OutputView.showGUI()
        ovconfig[OV_ConfigKeys[0]] = self.changeText
        ovconfig[OV_ConfigKeys[1]] = self.popCards
        ovconfig[OV_ConfigKeys[2]] = self.shuffleCurrentHand
        ovconfig[OV_ConfigKeys[3]] = self.sortCurrentHand
        
            
        self.ov.setInternalConfigs(ovconfig)
        self.ov.create_widgets()
        
        
        self.ov.master.mainloop()
mc = MainController([("p"+str(i)) for i in range(1,5)],True)
mc.play()