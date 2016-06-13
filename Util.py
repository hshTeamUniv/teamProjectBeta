from Deck import *
from Player import *

class Util:
    @staticmethod
    def moveListOrder(listv):
        if(type(listv) == list and listv!=[]):
            listv = listv[1:]+[listv[0]]
        return listv
    @staticmethod
    def chooseDirection(playerNameList,dir=True):
        if(len(playerNameList)>2 and dir == False):
            temp = playerNameList[1:]
            temp.reverse()
            playerNameList=[playerNameList[0]]+temp
            return playerNameList
        else:
            return playerNameList
    @staticmethod
    def distributeCardToPlayers(players,deck):
        deck.shuffle()
        idx = 0
        playercount = len(players)
        while(deck!=[]):
            idx %=playercount
            players[idx].importCard(deck[0])
            idx += 1
            deck = deck[1:]
        
        return players