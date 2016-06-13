from Card import *
from Deck import *

from Player import *
deck = Deck()
import random
random.shuffle(deck)
players = [Player("player"+str(i)) for i in range(1,9)]
playerCount = len(players)
idx = 0
while( deck != []):
    idx %= playerCount
    players[idx].getHand().append(deck[0])
    deck = deck[1:]
    idx+=1
del idx
for player in players:
    hand = player.getHand()
    sameList = {}
    for i in range(len(Card.Levels())-1):
        if(not (i in sameList)):
            sameList[i] = []
        for card in hand:
            if(card.getRawLevel() == i):
                sameList[i].append(card)
        if(sameList[i]==[] or len(sameList[i])==1):
            del sameList[i]

            
    for i in sameList:
        if(sameList[i] !=[] and len(sameList[i])>1):
            print(i,sameList[i])
            while(not(len(sameList[i])==0 or len(sameList[i])==1)):
                import random
                a= random.sample(range(len(sameList[i])),2)
                b = [sameList[i][j]  for j in a]
                for v in b:
                    player.getHand().remove(v)
                    sameList[i].remove(v)
        #else:
            #del sameList[i]
    print("-------------")            
    print(sameList)
            
    print("=========")