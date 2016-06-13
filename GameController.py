from tkinter import *
from WaitingRoom import *
from Card import *
class PlayerManager(list):
    def __init__(self):
        
    def append(self, val):
        if(type(val)==Card or type(val)==JokerCard):
            return super().append(val)
    def insert(self,i,x):
        if(type(x)==Card or type(x)==JokerCard):
            return super().insert(i,x)
class MainMenu(Frame,controller):
    def __init__(self,master):
        super().__init__(master)
        master.pack()
        self.__mController = controller
        
    def getController():
        return self.__mController    
    def create_widgets(self):
        pass
        
    

class Controller:
    def __init__(self,playerNames):
        self.__players = [Player(name) for name in playerNames["user_name"]]
        deck = Deck()
        playerCount = len(self.__players)
        idx = 0
        while( deck != []):
            idx %= playerCount
            self.__players[idx].getHand().append(deck[0])
            deck = deck[1:]
            idx+=1
        
    @staticmethod
    def getPlayerNameList():
        playerNameList = {}
        playerNameList = InputView.getPlayerNameList()
        while(playerNameList["user_name"] == [] or not ( 2<=len(playerNameList["user_name"])<=8)):
            playerNameList = InputView.getPlayerNameList(playerNameList)
        return playerNameList
    def play(self):
        window = Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window.geometry(str(screen_width)+"+"+str(screen_height))
        MainMenu(window,self)
        window.mainLoop()
        
        
        
def main():
    playerList = []
    playerNameList = {}
    playerNameList = InputView.getPlayerNameList()
    while(playerNameList["user_name"] == [] or not ( 2<=len(playerNameList["user_name"])<=8)):
        playerNameList = InputView.getPlayerNameList(playerNameList)
    print(playerList)
    
    
main()