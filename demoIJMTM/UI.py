from Tkinter import *
import association
import matplotlib.pyplot as plt
import tkFont

class Application(Frame):
            
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
      
        
    def createWidgets(self):


        cv=Canvas(master,bd=0, highlightthickness=0, relief='ridge')
        cv.create_line(680,90,680,225)
        cv.create_line(595,245,300,360)
        cv.create_line(775,245,1050,360)
        

        ### Space Rows/Columns ###
        self.label1=Label(cv)
        self.label1["text"] = ""
        self.label1.grid(row=0,column=0,columnspan=9)
        self.label1["font"] = 16

        self.label2=Label(cv)
        self.label2["text"] = ""
        self.label2.grid(row=1,column=0,columnspan=9)
        self.label2["font"] = 16

        self.label3=Label(cv)
        self.label3["text"] = ""
        self.label3.grid(row=3,column=0)
        self.label3["font"] = 16

        self.label4=Label(cv)
        self.label4["text"] = ""
        self.label4.grid(row=4,column=0)
        self.label4["font"] = 16

        self.label5=Label(cv)
        self.label5["text"] = ""
        self.label5.grid(row=5,column=0)
        self.label5["font"] = 16

        self.label6=Label(cv)
        self.label6["text"] = ""
        self.label6.grid(row=6,column=0)
        self.label6["font"] = 16

        self.label7=Label(cv)
        self.label7["text"] = ""
        self.label7.grid(row=8,column=0)
        self.label7["font"] = 16

        self.label8=Label(cv)
        self.label8["text"] = ""
        self.label8.grid(row=9,column=0)
        self.label8["font"] = 16

        self.label9=Label(cv)
        self.label9["text"] = ""
        self.label9.grid(row=10,column=0)
        self.label9["font"] = 16

        self.label10=Label(cv)
        self.label10["text"] = ""
        self.label10.grid(row=12,column=0)
        self.label10["font"] = 16

        self.label11=Label(cv)
        self.label11["text"] = ""
        self.label11.grid(row=14,column=0)
        self.label11["font"] = 16

        self.label12=Label(cv)
        self.label12["text"] = ""
        self.label12.grid(row=16,column=0)
        self.label12["font"] = 16

        self.label13=Label(cv)
        self.label13["text"] = ""
        self.label13.grid(row=18,column=0)
        self.label13["font"] = 16


        # make instance of association, keywords data='kw_acme_ijmtm', relation data ='combine_acme_ijmtm'
        ba=association.Association('kw_acme_ijmtm_ijms_20150715','p2p_acme_ijmtm_ijms_20150715',3)





        ### functions  ###

        
        def Ass_mid():
            ba.make_associations(InputText.get())

            InputText.set(ba.step[0])
            cbmid['text']=ba.step[0]


            labelText1.set(ba.step[1])
            cbtop['text']=ba.step[1]
            labelText2.set(ba.step[2])
            cbleft['text']=ba.step[2]
            labelText3.set(ba.step[3])
            cbright['text']=ba.step[3]
            return

        def Ass_top():
            ba.make_associations(labelText1.get())


            InputText.set(ba.step[0])
            cbmid['text']=ba.step[0]

            labelText1.set(ba.step[1])
            cbtop['text']=ba.step[1]
            labelText2.set(ba.step[2])
            cbleft['text']=ba.step[2]
            labelText3.set(ba.step[3])
            cbright['text']=ba.step[3]
            return

        def Ass_right():
            ba.make_associations(labelText3.get())

            InputText.set(ba.step[0])
            cbmid['text']=ba.step[0]

            labelText1.set(ba.step[1])
            cbtop['text']=ba.step[1]
            labelText2.set(ba.step[2])
            cbleft['text']=ba.step[2]
            labelText3.set(ba.step[3])
            cbright['text']=ba.step[3]
            return

        def Ass_left():

            ba.make_associations(labelText2.get())

            InputText.set(ba.step[0])
            cbmid['text']=ba.step[0]

            labelText1.set(ba.step[1])
            cbtop['text']=ba.step[1]
            labelText2.set(ba.step[2])
            cbleft['text']=ba.step[2]
            labelText3.set(ba.step[3])
            cbright['text']=ba.step[3]
            return

        def f_back():
            ba.go_back()
            InputText.set(ba.step[0])
            cbmid['text']=ba.step[0]

            labelText1.set(ba.step[1])
            cbtop['text']=ba.step[1]
            labelText2.set(ba.step[2])
            cbleft['text']=ba.step[2]
            labelText3.set(ba.step[3])
            cbright['text']=ba.step[3]
            return

        def f_restart():
            ba.restart()
            InputText.set(ba.step[0])
            cbmid['text']=ba.step[0]

            labelText1.set(ba.step[1])
            cbtop['text']=ba.step[1]
            labelText2.set(ba.step[2])
            cbleft['text']=ba.step[2]
            labelText3.set(ba.step[3])
            cbright['text']=ba.step[3]
            return

        def checktoH():
            ba.H_V=0
            return

        def showimage():
            plt.ion()
            checkbox=[cbmidvar.get(),cbtopvar.get(),cbleftvar.get(),cbrightvar.get()]
            words=[]
            for i,n in enumerate(checkbox):
                if n==1:
                    words.append(ba.step[i])

            ba.GetImage(words)
            return


        ##font##
        helv36b = tkFont.Font(family='Courier ',size=16,slant='italic')
        helv36 = tkFont.Font(family='Helvetica',size=16)

        ### Label Box Out Put ###
        #top lable
        labelText1=StringVar()
        labelText1.set(' ')
        label1=Label(cv,textvariable=labelText1,bg="White",width=35,height=2,font=helv36b)
        label1.grid(row=2, column=1)

        #left label

        labelText2=StringVar()
        labelText2.set(' ')
        label2=Label(cv,textvariable=labelText2,bg="White",width=35,height=2,font=helv36b)
        label2.grid(row=13, column=0)

        #right label

        labelText3=StringVar()
        labelText3.set(' ')
        label3=Label(cv,textvariable=labelText3,bg="White",width=35,height=2,font=helv36b)
        label3.grid(row=13, column=2)



        ### User Input ###
        InputText = StringVar()
        InputText.set('input your enquiry here')
        Input = Entry(cv,textvariable = InputText, bg='White', width=40, font=helv36,justify=CENTER,)
        Input.grid(row=7,column=1)



        ### Buttons ###

        
        button1 =Button(cv)
        button1["text"] = "   Associate top   "
        button1["fg"]= "Black"
        button1["bg"]= "White"
        button1["command"]= Ass_top
        button1.place(x=895,y=50)
        button1["font"] = helv36

        button2 =Button(cv)
        button2["text"] = "   Associate left   "
        button2["fg"]= "Black"
        button2["bg"]= "White"
        button2["command"]= Ass_left
        button2.place(x=150,y=425)
        button2["font"] = helv36

        button3 =Button(cv)
        button3["text"] = "    Associate right    "
        button3["fg"]= "Black"
        button3["bg"]= "White"
        button3["command"]= Ass_right
        button3.place(x=1000,y=425)
        button3["font"] = helv36

        
        buttoninput =Button(cv)
        buttoninput["text"] = "   Associate mid   "
        buttoninput["fg"]= "Black"
        buttoninput["bg"]= "White"
        buttoninput["command"]= Ass_mid
        buttoninput.place(x=575,y=275)
        buttoninput["font"] = helv36

        buttonback =Button(cv)
        buttonback["text"] = "    Back    "
        buttonback["fg"]= "Black"
        buttonback["bg"]= "White"
        buttonback["command"]= f_back
        buttonback.grid(row=3,column=0)
        buttonback["font"] = helv36

        buttonrestart =Button(cv)
        buttonrestart["text"] = "    Restart    "
        buttonrestart["fg"]= "Black"
        buttonrestart["bg"]= "White"
        buttonrestart["command"]= f_restart
        buttonrestart.grid(row=5,column=0)
        buttonrestart["font"] = helv36


        buttonimage =Button(cv)
        buttonimage["text"] = "    Show\Combine image    "
        buttonimage["fg"]= "Black"
        buttonimage["bg"]= "White"
        buttonimage["command"]= showimage
        #buttonimage.grid(row=4,column=8)
        buttonimage.grid(row=4,column=4)
        buttonimage["font"] = 12



        cbtopvar=IntVar()
        cbtop = Checkbutton(cv, text='top word',
            variable=cbtopvar, command=checktoH)
        cbtop.select()
        cbtop.place(x=1380, y=190)


        cbmidvar=IntVar()
        cbmid = Checkbutton(cv, text='mid word',
            variable=cbmidvar, command=checktoH)
        cbmid.select()
        cbmid.place(x=1380, y=160)


        cbleftvar=IntVar()
        cbleft = Checkbutton(cv, text='left word',
            variable=cbleftvar, command=checktoH)
        cbleft.select()
        cbleft.place(x=1380, y=220)


        cbrightvar=IntVar()
        cbright = Checkbutton(cv, text='right word',
            variable=cbrightvar, command=checktoH)
        cbright.select()
        cbright.place(x=1380, y=250)





        cv.pack()

       
        
master = Tk()
master.title("Keywords network")
master.minsize(1300,485)
master.maxsize(1300,485)
app = Application(master)
app.mainloop()
master.destroy()

