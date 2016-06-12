from tkinter import *
class FailFrame(Frame) :
    def __init__(self, master,name) :
        super().__init__(master)
        self.__master=master
        self.__result=False
        self.setName(name,False)
        self.grid(row=0,column=0,sticky="news")
        self.widgetStore=[]
        self.create_widgets()
        gs = self.grid_size()
        
        for i in range(gs[1]):
            self.grid_rowconfigure(i, weight=1)
        for i in range(gs[0]):
            self.grid_columnconfigure(i, weight=1)
        self.bind("<Configure>",self.configEvent)
        
        
        
    def doPack(self):
        self.pack(fill=BOTH,padx=20, pady=20,expand=True)
    def tkraise(self):
        self.update()
        print("tkraise wordk")
        maxLen = 0
        for widget in  self.widgetStore:
            maxLen = max(maxLen,len(widget['text']))
        for widget in  self.widgetStore:
            self.refreshTextSize(widget,maxLen+2,self.grid_bbox()[3],True)
        super().tkraise()
        self.doPack()
    def setName(self,name,returnObject=True):
        self.__name = name
        if(bool(returnObject)):
            return self
    def configEvent(self,event):
        maxLen = 0
        for widget in  self.widgetStore:
            maxLen = max(maxLen,len(widget['text']))
        for widget in  self.widgetStore:
            self.refreshTextSize(widget,maxLen+2,event.width,True)
    def refreshTextSize(self,widget,maxLen,width,expandMode=False):
        if(widget):
            #self.update()
            if(expandMode):
                text = str(widget['text'])
                maxWid = width//maxLen
                fsz =int(maxWid*0.75)
                widget['font']=("TkDefaultFont",max(10,fsz))
            else:
                widget['font']= LARGE_FONT#("TkDefaultFont",30)
        return widget
        
    def create_widgets(self) :
        
        lb1=Label(self, text="'"+self.__name+"' 님이 게임에서 패배하셨습니다.")
        lb1.pack(expand=True)
        lb1.grid(row=0, column=0,columnspan=2,sticky="news")
        lb2=Label(self, text="계속하시겠습니까?")
        lb2.grid(row=1, column=0,sticky="news")

        yesbtn = Button(self, text="O", command= lambda: self.proceed(True))
        yesbtn.grid(row=2, column=0)
        nobtn = Button(self, text="X", command= lambda: self.proceed(False))
        nobtn.grid(row=2, column=1)
        self.widgetStore.append(lb1)
        self.widgetStore.append(lb2)
        self.widgetStore.append(yesbtn)
        self.widgetStore.append(nobtn)
        self.update()
        
    def proceed(self,value) :
        self.setResult(value)
        self.__master.destroy()
    def setResult(self,value):
        self.__result=value
    def getResult(self):
        return self.__result
'''
tk = Tk()
topframe = Frame(tk)
topframe.pack(fill="both")
ff =FailFrame(topframe)
f2 = Frame(topframe)
#f2.grid(row=0,column=0,sticky='news')
ff.doPack()
f2.pack()
f2.place(x=0,y=0)
f2.pack_forget()
Label(f2,text="asdasd").pack()
ff.tkraise()
tk.mainloop()
print(ff.getResult())
'''
