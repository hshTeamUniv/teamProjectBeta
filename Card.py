import json
from tkinter import PhotoImage

class Card:
    __Categories = ["spade","diamond","club","heart","joker"]
    __CategoriesAsArt = ["♠","♦","♣","♥","☢"] 
    __Levels = [ "2","3","4","5","6","7","8","9","10","J","Q","K","A","Jk1" ]
    __LevelsName = __Levels[:9]+ ["jack","queen","king","ace","joker"] # [ "2","3","4","5","6","7","8","9","10","J","Q","K","A","Jk1" ]
    __category=0
    __level=0
    __image=None
    def getButtonTextFormat(self):
        cate = self.CategoriesAsArt()[self.getCategoryAsIndex()]
        lv = self.getLevelAsString()
        a = lv
        b = cate.rjust( len(cate)+len(lv)+2)
        c = lv.rjust( len(b)*2+len(a)*2+3)
        result = a.ljust(max(len(c),len(b)))+"\n\n"
        result += b+"\n\n"
        result+=c
        return result
    def getConsoleTextFormat(self):
        cardSideVertical = '|'
        cardSideHorizontal = '-'
        cate = self.getCategoryAsString()
        lv = self.getLevelAsString()
        line2 = cardSideVertical.ljust(2)+cate.rjust( len(cate)+len(lv)+1)+cardSideVertical.rjust(2)
        line3 = cardSideVertical.ljust(2) +lv.rjust( len(cate)+len(lv)*2+2)+cardSideVertical.rjust(2)
        lineVoid = cardSideVertical+"".ljust(len(line3)-2)+cardSideVertical
        lineTB = cardSideHorizontal*len(line3)
        line1 = cardSideVertical+lv.ljust(len(line3)-2)+ cardSideVertical
        lv = self.getLevelAsString()
        result = lineTB+"\n"
        result += line1+"\n"
        result += lineVoid+"\n"
        result += line2+"\n"
        result += lineVoid+"\n"
        result += line3 +"\n"
        result += lineTB
        return result
    @staticmethod
    def Categories():
        return Card.__Categories[:]
    @staticmethod
    def CategoriesAsArt():
        return Card.__CategoriesAsArt[:]
    @property
    def ImageFileName(self):
        return str(self.__fileName)
    def setCardImage(self):
        self.__fileName = Card.LevelsName()[self.getRawLevel()]+"_of_"+self.Categories()[self.getRawCategory()]+"s.gif"
        print(self.__fileName)
        img = PhotoImage(file=self.__fileName) #Card.LevelsName()[self.getRawLevel()]+"_of_"+self.Categories()[self.getRawCategory()]+"s.gif")
        self.__image = img
        
    def getImage(self):
        self.setCardImage()
        return self.__image
    @staticmethod
    def LevelsName():
        return Card.__LevelsName[:]
    def cloneCard(self):
        result = Card(self.__category,self.__level)
        return result
    @staticmethod
    def Levels():
        return Card.__Levels[:]
    def flipImage(self):
        self.__flipImage
    def cardImage(self):
        self.__cardImage
    def __str__(self):
        return self.__CategoriesAsArt[self.__category]+ " "  +self.getLevelAsString()
    def __init__(self,Category=0,Level=0):
        self.setCardAttribute(Category,Level)
        #self.setCardImage()
    def setCardAttribute(self,Category,Level):
        self.setCategory(Category)
        self.setLevel(Level)
        return self
    def setCategory(self,Category):
        self.__category = Category
        return self
    def getRawCategory(self):
        return self.__category
    
    @property
    def level(self):
        return self.__level
    def getRawLevel(self):
        return self.__level

    def getRawCategoryAsString(self):
        return str(self.getRawCategory())

        
    def getRawLevelAsString(self):
        return str(self.getRawLevel())
    @staticmethod
    def createFromJson(Json):
        return Card().fromJson(Json)

    def fromJson(self,Json):
        data = json.loads(Json)
        self.setCategory(int(data["rawcategory"]))
        self.setLevel(int(data["rawlevel"]))
        return self
    
    def toJson(self):
        result = {"rawcategory":self.getRawCategoryAsString(),"rawlevel":self.getRawLevelAsString()}
        result = json.dumps(result)
        return result
	
    def getCategoryAsIndex(self):
        return self.getRawCategory()
	
    def getLevelAsIndex(self):
        return self.getRawLevel()
	
    def getCategoryAsString(self):
        return Card.Categories()[self.getCategoryAsIndex()]
	
    def getLevelAsString(self):
        return Card.Levels()[self.__level]
	
    def setLevel(self, Level):
        self.__level = Level
        return self
    def isDropable(self):
        return True
class JokerCard(Card):
    def getThisAsParent(self):
        return super()
    def __init__(self):
        super().__init__(len(Card.Categories())-1,len(Card.Levels())-1)
    
    @staticmethod
    def createFromJson(Json):
        return JokerCard().fromJson(Json)
    def cloneCard(self):
        result = JokerCard()
        return result
    def isDropable(self):
        return False 