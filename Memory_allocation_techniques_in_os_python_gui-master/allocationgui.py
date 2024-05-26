import tkinter 
import customtkinter
from tkinter import messagebox
import win32gui
import sys
import os


class App(customtkinter.CTk):
    def __init__(self):
        customtkinter.CTk.__init__(self)
        self.title("Memory allocation techniques")
        self.originalblocksizes=[]
        self.originalprocesses=[]
        self.indx=0

        # Creating elements
        self.label1=customtkinter.CTkLabel(self,text="Enter the number of partition:")
        self.enter1=customtkinter.CTkEntry(self)        
        self.label2=customtkinter.CTkLabel(self,text="Enter the number of process:")        
        self.enter2=customtkinter.CTkEntry(self)              
        self.ok = customtkinter.CTkButton(self, text = "Ok ", command= self.getvalues)

        self.ok.grid(columnspan=4, row=2, column=0, padx=0, pady=15)
        self.label1.grid(row=0,column=0,padx=20)
        self.label2.grid(row=1,column=0,padx=20)
        self.enter1.grid(row=0,column=1,pady=10,padx=20)
        self.enter2.grid(row=1,column=1,pady=10,padx=20)


    def getvalues(self):
        self.ok.destroy()
        self.label1.destroy()
        self.label2.destroy()

        for i in range(int(self.enter1.get())):
            strr="Enter the size of "+str(i+1)+" partition: "
            lab=customtkinter.CTkLabel(self,text=strr,anchor='w')
            lab.grid(row=i,column=0,pady=2,padx=20)
            par=customtkinter.CTkEntry(self)
            par.grid(row=i,column=1,pady=2,padx=20)
            self.indx=i+1
            self.originalblocksizes.append(par)

        for i in range(int(self.enter2.get())):
            strr="Enter the size of "+str(i+1)+" process: "
            lab=customtkinter.CTkLabel(self,text=strr,anchor='w')
            lab.grid(row=self.indx,column=0,pady=2,padx=20)
            par=customtkinter.CTkEntry(self)
            par.grid(row=self.indx,column=1,pady=2,padx=20)
            self.indx+=1
            self.originalprocesses.append(par)

        self.enter1.destroy()
        self.enter2.destroy()
        self.ok2 = customtkinter.CTkButton(self, text = "Ok ", command= self.define)
        self.ok2.grid(row=self.indx, column=0, pady=15, columnspan=4)
        


    def define(self):
        m=len(self.originalblocksizes)
        n=len(self.originalprocesses)
        for i in range(m):
            self.originalblocksizes[i]=int(self.originalblocksizes[i].get())

        for i in range(n):
            self.originalprocesses[i]=int(self.originalprocesses[i].get())

        customtkinter.CTkLabel(self,text="Choose method").grid(row=0,column=3,pady=2)
        self.ok2.destroy()
        self.firstfitbutton= customtkinter.CTkButton(self,text = "First Fit", command = (lambda index=self.indx: self.firstFit(index))).grid(row=1, column=3, pady=2)
        self.bestfitbutton = customtkinter.CTkButton(self, text = "Best Fit", command = (lambda index=self.indx: self.bestFit(index))).grid(row=2, column=3, pady=2)
        self.worstfitbutton = customtkinter.CTkButton(self, text = "Worst Fit", command= (lambda index=self.indx: self.worstFit(index))).grid(row=3, column=3, pady=2)


    def bestFit(self,indx):
        m=len(self.originalblocksizes)
        n=len(self.originalprocesses)
        blocksizes=self.originalblocksizes.copy()
        processes=self.originalprocesses.copy()
        allocation = [-1] * n
        for i in range(n): 
            bestIdx = -1
            for j in range(m): 
                if blocksizes[j] >= processes[i]: 
                    if bestIdx == -1:  
                        bestIdx = j  
                    elif blocksizes[bestIdx] > blocksizes[j]:  
                        bestIdx = j

            if bestIdx != -1: 
                allocation[i] = bestIdx 
                blocksizes[bestIdx] -= processes[i] 
        indx+=1
        final=""
        for i in range(n): 
            strr=""
            if allocation[i] != -1:  
                strr=str(allocation[i] + 1)  
            else: 
                strr="Not Allocated"
            indx+=1
            final+='Process No. '+str(i+1)+' of size '+str(processes[i])+' allocated to block no. '+strr+'\n'
        
        messagebox.showinfo('Best Fit Output', final)

        self.done = customtkinter.CTkButton(self, text ="Done", command = self.restart).grid(row=indx+1, column=0, pady=15, columnspan=4)



    def firstFit(self,indx): 
        m=len(self.originalblocksizes)
        n=len(self.originalprocesses)
        blocksizes=self.originalblocksizes.copy()
        processes=self.originalprocesses.copy()

        allocation = [-1] * n  
        for i in range(n): 
            for j in range(m): 
                if blocksizes[j] >= processes[i]:
                    allocation[i] = j 
                    blocksizes[j] -= processes[i]         
                    break
        indx+=1
        final=""
        for i in range(n): 
            strr=""
            if allocation[i] != -1:  
                strr=str(allocation[i] + 1)  
            else: 
                strr="Not Allocated"
            indx+=1
            final+='Process No. '+str(i+1)+' of size '+str(processes[i])+' allocated to block no. '+strr+'\n'

        messagebox.showinfo('First Fit Output', final)

        self.done = customtkinter.CTkButton(self, text = "Done", command = self.restart).grid(row=indx+1, column=0, pady=15, columnspan=4)


    def worstFit(self,indx):
        m=len(self.originalblocksizes)
        n=len(self.originalprocesses)
        blocksizes=self.originalblocksizes.copy()
        processes=self.originalprocesses.copy()

        allocation = [-1] * n 
        for i in range(n): 
            wstIdx = -1
            for j in range(m): 
                if blocksizes[j] >= processes[i]: 
                    if wstIdx == -1:  
                        wstIdx = j  
                    elif blocksizes[wstIdx] < blocksizes[j]:  
                        wstIdx = j  
            if wstIdx != -1: 
                allocation[i] = wstIdx  
                blocksizes[wstIdx] -= processes[i] 
        indx+=1
        final="" 
        for i in range(n): 
            strr=""
            if allocation[i] != -1:  
                strr=str(allocation[i] + 1)  
            else: 
                strr="Not Allocated"
            indx+=1
            final+='Process No. '+str(i+1)+' of size '+str(processes[i])+' allocated to block no. '+strr+'\n'

        messagebox.showinfo('Worst Fit Output', final)        

        self.done = customtkinter.CTkButton(self, text = "Done", command = self.restart).grid(row=indx+1, column=0, pady=15, columnspan=4)


    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
            

app = App()
app.mainloop()