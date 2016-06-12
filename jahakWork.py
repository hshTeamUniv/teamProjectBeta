from tkinter import *
import time
import random 
class ChoosePlayDirection(Frame):
    def __init__(self,master,playerNames):
        super().__init__(master)
        self.pack(padx=10, pady=10)
        self.button1_clicks = 0
        self.button2_clicks = 0
        self.end_button = 0
        self.people = playerNames
        self.peopleCount = len(playerNames)
        self.create_widgets()
    
    
    def create_widgets(self):
        initName = "none"
        if(len(self.people)!=0):
            initName = self.people[0]
            
        self.display = Label(self, text="'"+initName+"'순서방향을 정해주십시오")
        self.display.grid(row=0, column=1)
        Label(self, text=' ').grid(row=1,column=1)
        self.button1 = Button(self)
        self.button1["text"] = "순방향"
        self.button1["command"] = self.update_count1
        self.button1.grid(row=2, column=0)
        self.button2 = Button(self)
        self.button2['text'] = '역방향'
        self.button2['command'] = self.update_count2
        self.button2.grid(row=2, column=2)
        #Button(self, text="quit", command=self.quit).grid(row=4, column=2)
    def nextPlayer(self):
        if(self.people==[] or len(self.people)==1):
            self.end_sequence()
        else:
            self.people = self.people[1:]
            txt = self.display['text']
            after = txt[txt.index("'",1):]
            self.display['text'] = "'"+self.people[0]+after
    def update_count1(self):
        self.button1_clicks += 1
        self.nextPlayer()
    def update_count2(self):
        self.button2_clicks += 1
        self.nextPlayer()
    def end_sequence(self):
        print("es")
        self.end_button = self.button1_clicks + self.button2_clicks
        if self.end_button == self.peopleCount : 
            if self.button1_clicks > self.button2_clicks :
                Label(self, text='순방향으로 정하셨습니다').grid(row=3, column=1)
            elif self.button1_clicks < self.button2_clicks : 
                Label(self, text='역방향으로 정하셨습니다').grid(row=3, column=1)
            else : 
                la = [1,2]
                random.shuffle(la)
                if la[0] == 1 : 
                    Label(self, text='순방향으로 정하셨습니다').grid(row=3, column=1)
                else : 
                    Label(self, text='역방향으로 정하셨습니다').grid(row=3, column=1)

'''
root = Tk()
root.title('ckeck')
root.geometry("400x300")
app = App(root,["asf","124"])
root.mainloop()
'''

