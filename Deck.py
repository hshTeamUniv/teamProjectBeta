import random
import json
from Card import *
class Deck(list):
    __jt = False
    #__CardCarrier = []
    def get(self,index):
        if(0<=index<len(self)):
            return self.__CardCarrier[index]
        else:
            return None
    def append(self,x):
        if(type(x) == Card or type(x) == JokerCard):
            super().append(x)
    def insert(self,i,x):
        if(type(x) == Card or type(x) == JokerCard):
            super().insert(i,x)
    def extend(self,v):
        if(v!=[] and ( type(v[0])==Card or type(v[0])==JokerCard)):
            return super().extend(self, v)
    
    @staticmethod
    def getSortedDeck():
        result = Deck()
        return result
    @staticmethod
    def getEmptyDeck():
        result = Deck()
        result.clear()
        return result
   
	
    def getCloneDeck(self):
        result = Deck.getEmptyDeck()
        for card in self:
            result.append(card.cloneCard())
        return result

    def shuffle(self):
        random.shuffle(self)
        return self

    def shuffleWithClone(self):
        result = Deck.getCloneDeck()
        result.shuffle()
        #Collections.shuffle(result)
        return result
    def fromJson(self,Json,returnObject=True):
        self.clear()
        data = json.loads(Json)
        deckData = data['deck']
        for jcard in deckData:
            if(jcard["rawcategory"] == str(len(Card.Categories())-1) and \
               jcard['rawlevel']== str(len(Card.Levels())-1)):
                self.append(JokerCard.createFromJson( jcard))
            else:
                self.append(Card.createFromJson( jcard))
        if(returnObject):
            return self
        
    @staticmethod
    def createFromJson(Json):
        return Deck.getEmptyDeck().fromJson(Json)
    @staticmethod
    def MakeJson(deck):
        ja = []
        for c in deck:
            ja.append(c.toJson())
        result = {"deck":ja}
        result = json.dumps(result)
        return result

    def toJson(self):
        return Deck.MakeJson(self)
	

    def __init__(self,Jt=False):
        super().__init__(self)
        for i in range(0,len(Card.Categories())-1):
            for j in range(0,len(Card.Levels())-1):
                self.append(Card(i,j))
		
        self.__jt = Jt
        for i in range(self.__jt+1):
            self.append(JokerCard())
