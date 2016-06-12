import json
import random
import time
from Deck import *
from Card import *
from tkinter import *
from StringData import *
import tkinter.messagebox
class CardButton(Button):
    __mainText=""
    __subText=""
    def __init__(self, master=None, **kargs):
        super().__init__( master, kargs)
        self.__cardObj=None
        if('card' in kargs):
            self.setCardObj(kargs['card'])
    
    def setCardObj(self,co):
        self.__cardObj = co
    def getCardObj(self):
        return self.__cardObj
    def setMainText(self,txt):
        self.__mainText=txt
        return self
    def getImage(self):
        return self.__cardObj.getImage()
    def setSubText(self,txt):
        self.__subText=txt
        return self
    def switchToMainText(self):
        if(self['text']!=self.__mainText):
            self['text']=self.__mainText
        return self
    def switchToSubText(self):
        if(self['text']!=self.__subText):
            self['text']=self.__subText
        return self
    def swipeText(self):
        if(self['text']==self.__mainText):
            self['text']==self.__subText
        else:
            self['text']==self.__mainText
        return self

class ValueContainedCheckButton(Checkbutton):
    def __init__(self,master,**cnf):
        super().__init__(master, cnf)
        self.val = IntVar()
        self.configure(variable=self.val)
        
    def getValue(self):
        return bool(self.val.get())    
    
class Player:
    @staticmethod
    def someInternalConfigKeys():
        return ["ExistRemoveablePlayerCmd","refreshPlayerRankCmd","refreshDisplayedCardFrameCmd","transmitCard"]
    __cPublicFrame=None
    @property
    def frameConfigs(self):
        return self.__FrameCnfs
    def setFrameConfigs(self,kargs):
        for key in kargs:
            self.__FrameCnfs[key] = kargs[key]
    __FrameCnfs = {}
    __rootPublicFrameCanvas=None
    __cPublicScroller=None
    __cScroller = None    
    __hand=None
    __name=""
    __cFrame = None
    def shuffleDeck(self):
        self.__hand = self.__hand.shuffle()
    selectedCardCount=0
    def getSelectedCardList(self):
        self.selectedCardCount=-1
        children = self.__cFrame.winfo_children()
        result = []
        for child in children:
            chd = child.winfo_children()
            if(chd[0].getValue() and chd[1].getCardObj().isDropable()):
                print(chd[0].getValue())
                result.append(chd[1].getCardObj())
        if(len(result)!=2):
            print("error")
            self.selectedCardCount=len(result)
            tkinter.messagebox.showinfo(StringData.getDlgTitle_cardPopError(),StringData.getDlgContent_cardPopError())
            result=[]
        else:
            if(result[0].getRawLevel() != result[1].getRawLevel() ):
                result=[]
        return result
        
    def delSelectedCardsFromFrame(self):
        self.isPlayerCardPoped=True
        return self.delCardsFromFrame(self.getSelectedCardList())
    def delCardsFromFrame(self,cards):
        if(len(cards)>2 or cards == () or cards == []):
            return False
        isRemoved = self.popTwoCards(cards)
        if(isRemoved):
            keymgcls =self.__keymgcls
        #self.__rootFrameCanvas.configure(scrollregion = self.__rootFrameCanvas.bbox("all"))
            self.__FrameCnfs[Player.someInternalConfigKeys()[0]]()
            self.__FrameCnfs[Player.someInternalConfigKeys()[1]]()
        return isRemoved
        
    def delCardFromFrame(self,btn,card,frame,**args):
        isDrpabe=card.isDropable()
        cd1=card.cloneCard()
        btn.destroy()
        self.__hand.remove(card)
        keymgcls = self.__keymgcls
        
        #if(keymgcls in args and args[keymgcls]!=None):
           
        self.__FrameCnfs[Player.someInternalConfigKeys()[0]]()
            
        self.__FrameCnfs[Player.someInternalConfigKeys()[3]](cd1)
        self.__FrameCnfs[Player.someInternalConfigKeys()[2]]()
        self.__FrameCnfs[Player.someInternalConfigKeys()[1]]()
        try:
            for chd in frame.winfo_children():
                chd.configure(state='disable') 
        except:
            pass
        del btn,card
    __keymgcls = 'mgcls'
    isPlayerCardPoped = False
    def getPublicCardFrame(self,**kargs):
        if('rootCanvas' in kargs and self.__rootPublicFrameCanvas == None):
            self.__rootPublicFrameCanvas=kargs['rootCanvas']
        rc = None
        erpfnc = None
        #mgcls = None
        #keymgcls =self.__keymgcls
        #if(keymgcls in kargs):
         #   self.__FrameCnfs[keymgcls] = kargs[keymgcls]
        #if(keymgcls in self.__FrameCnfs):
         #   mgcls = self.__FrameCnfs[keymgcls]
        
        if(self.__cPublicFrame != None):
            lst = self.__cPublicFrame.winfo_children()
            for i in lst:
                i.destroy()
        if(self.__cPublicFrame==None and 'parent' in kargs):
            master=kargs['parent']
            self.__cPublicFrame = Frame(master)
            try:
                self.__cPublicFrame.pack(fill=X,expand=TRUE)
            except:
                pass
            self.__cPublicFrame.grid(row=0,column=0,stick="news")
        
        for i in range(len(self.__hand)):
            
            btn =CardButton(self.__cPublicFrame,text=self.__hand[i].getButtonTextFormat(),wraplength=30,height=8,justify=CENTER).setMainText(self.__hand[i].getButtonTextFormat()).setSubText("Card"+str(i+1)).switchToSubText()
            btn.setCardObj(self.__hand[i])
            
            btn.config( command=lambda card=self.__hand[i],btn=btn:self.delCardFromFrame( btn,card,self.__cPublicFrame))
            btn.grid(row=0,column=i,rowspan=2,stick=N+S+E+W)
        if(self.__rootPublicFrameCanvas!=None):
            self.__rootPublicFrameCanvas.configure(scrollregion = self.__rootPublicFrameCanvas.bbox("all"))
                
        return self.__cPublicFrame
    @property
    def hasSameLevelCard(self):
        for i in range(len(Card.Levels())):
            count = 0
            for j in range(len(self.__hand)):
                if(self.__hand[j].getRawLevel()==i):
                    count+=1
            if(count>1):
                return True
        return False
            
    def ckbCommand(self):
        print("ckbcommand")
    def chgCkb(self,cb):
        cb.toggle()
        self.ckbCommand()
    def sortDeck(self):
        self.__hand.sort(key=lambda card: card.level)
    __rootFrameCanvas = None
    def getCardFrame(self,**kargs):
        self.isPlayerCardPoped=False
        if('rootCanvas' in kargs and self.__rootFrameCanvas == None):
            self.__rootFrameCanvas=kargs['rootCanvas']
        keymgcls = 'mgcls'
        #if(keymgcls in kargs):
        #    self.__FrameCnfs[keymgcls] = kargs[keymgcls]
        #if(keymgcls in self.__FrameCnfs):
        #    mgcls = self.__FrameCnfs[keymgcls]
        if(self.__cFrame!=None):# and len(self.__hand)!= len(self.__cFrame.winfo_children())):
            lst = self.__cFrame.winfo_children()
            for i in lst:
                i.destroy()
            
            for i in range(len(self.__hand)):
                Grid.columnconfigure(self.__cFrame,i,weight=1)
                p=PanedWindow(self.__cFrame,orient=VERTICAL)
                cb = ValueContainedCheckButton(p,command=self.ckbCommand,width=0)
                cb.pack(fill=X)
                txt= self.__hand[i].getButtonTextFormat()
                btn =CardButton(p,wraplength=30,height=8,text=txt).setMainText(self.__hand[i].getButtonTextFormat()).setSubText("Card"+str(i+1)).switchToMainText()
                btn.setCardObj(self.__hand[i])
                #img=btn.getImage()
                btn.config(command=lambda cb=cb: self.chgCkb(cb),height=8) #command=lambda card=self.__hand[i],btn=btn:self.delCardFromFrame( btn,card,mgcls=mgcls,isPublicFrame=False))
                btn.pack(fill=Y)
                #btn.image = img
                p.add(cb)
                p.add(btn)
                p.grid(row=0,column=i,rowspan=2,stick=N+S+E+W) #.pack(side=LEFT)
            
        if(self.__cFrame==None and 'parent' in kargs):
            master = kargs['parent']
            self.__cFrame = Frame(master)
            try:
                self.__cFrame.pack(fill=BOTH,expand=TRUE)
            except:
                pass
            leng = len(self.__hand)
            for i in range(len(self.__hand)):
                Grid.columnconfigure(self.__cFrame,i,weight=1)
                p=PanedWindow(self.__cFrame,orient=VERTICAL)
                txt= self.__hand[i].getButtonTextFormat()
                cb = ValueContainedCheckButton(p,command=self.ckbCommand,width=0)
                cb.pack(fill=X)
                btn =CardButton(p,wraplength=30,height=8).setMainText(self.__hand[i].getButtonTextFormat()).setSubText("Card"+str(i+1)).switchToMainText()
                btn.setCardObj(self.__hand[i])
                #img = btn.getImage()
                btn.config(command=lambda cb=cb: self.chgCkb(cb),height=8) #lambda card=self.__hand[i],btn=btn:self.delCardFromFrame( btn,card,mgcls=mgcls,isPublicFrame=False))
                #btn.image = img
                btn.pack(fill=Y)
                
                p.add(cb)
                p.add(btn)
                p.grid(row=0,column=i,rowspan=2,stick=N+S+E+W) #.pack(side=LEFT)
                
            self.__cFrame.grid(row=0,column=0,stick="news")
        
        if(self.__rootFrameCanvas!=None):
            print("work")
            self.__rootFrameCanvas.configure(scrollregion = self.__rootFrameCanvas.bbox("all"))
            
        return self.__cFrame
    @property
    def name(self):
        return self.__name
    def __init__(self,name):
        self.__hand = Deck.getEmptyDeck();
        self.setName(name)
    def popTwoCards(self,cards):
        if(len(cards)>2):
            return False
        hasJoker = False
        for card in cards:
            hasJoker = hasJoker or (not card.isDropable())
            if(hasJoker):
                break
        if(not hasJoker):
            for card in cards:
                self.__hand.remove(card)
            return True
        return False
        
        
    def popOneCard(self,card):
        for c in self.__hand:
            if(card==c  and card.isDropable()):
                self.__hand.remove(c)
                break
    '''
    def selectPlayerCard(self,player,card,waitMode=False):
        pdeck = player.getDeck()
        responseIdx = 0#impl this
        return pdeck[responseIdx]
    '''
    def exportCard(self,exportingIdx):
        result = self.__hand[exportingIdx].cloneCard()
        del self.__hand[exportingIdx]
        return  result
    def importCard(self,card):
        self.__hand.append(card)

    def setName(self,Name):
        self.__name = Name
        return self
    def getName(self):
        return self.__name
    def setHand(self,hand):
        d = hand
        if(type(hand) == Deck):
            d= d.getCloneDeck()
        else:
            d = Deck.getEmptyDeck()
            d.extend(hand)
        self.__hand = d
    def setDeck(self,hand):
        return self.setHand(hand)
    def pushCards(self,cards):
        self.__hand += cards
        return self.__hand
    def pushCard(self,card):
        self.importCard(card)
        return self.__hand
    def isComputer(self):
        return False
    def getHand(self):
        return self.__hand
    def getDeck(self):
        return self.__hand
    def fromJson(self,Json,returnObject=True): #네트워크 스트림에서 받아온 최신 데이터 파싱 
        data = json.loads()
        handData = data['hand']
        nameData = data['name']
        self.__hand.clear()
        for card in handData:
            self.__hand.append(Card.createFromJson(card))
        self.__name = nameData
        if(returnObject):
            return self
    def toJson(self):#네트워크 스트림에 전송을 위해 로컬 메모리의 변수에서 설정된 데이터를 전송 프로토톨에 맞게  패키징 
        handj = []
        for c in self.__hand:
            handj.add(c.toJson());
        result = {"hand":handj,"name":name}
        result = json.dumps(result)
        return result
class Computer(Player):
    __lstId=0
    @staticmethod
    def getLatestComputerId(isAdd=False):
        if(isAdd):
            Computer.__lstId+=1
        return Computer.__lstId
    def __init__(self,computerId=-1):
        if(computerId==-1):
            computerId=Computer.getLatestComputerId(True)
        super().__init__("Computer"+computerId)
        self.__cId=computerId
    
    
    @property    
    def computerId(self):
        return self.__cId        
    
    def isComputer(self):
        return True
    
    def popTwoCards(self,selectedIndexes):
        card1 = None
        card2 = None
        levelList = Card.Levels()
        for _ in range(len(levelList)-1):
            pass
        while(type(card1) == JokerCard or type(card2) == JokerCard):
             pass
        super().popTwoCards(selectedIndexes)
    
    def selectPlayerCard(self,player,card,waitMode=True):
        
        pdeck = player.getDeck()
        
        idx = random.randrange(0, len(player.getDeck()))
        result = player.getDeck()[idx].clone()
        if(waitMode):
            time.sleep(random.randrange(0,31)/10)
        self.importCard(result)
        player.exportCard(idx)
        return result