# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 14:16:41 2018

@author: Milad
"""

import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen
import base64
from io import BytesIO
import Functions as F
import recomByTag as R
from PIL import Image, ImageTk
## window
program=tk.Tk() #new window
program.geometry("1300x680") #window size
program.title("What to read next") #window title

## Label
BookId_label=tk.Label(program, text="Enter key word") #Create label,textview
BookId_label.grid(row=0) #don't use pack and grid together
#BookId_label.pack() #display label

##input
search_entry=tk.Entry(program,width=45)
search_entry.grid(row=1,column=0,columnspan=2,sticky=tk.W)
#search_entry.pack()
## create button

search_button=tk.Button(program,text="search",width=20, command=lambda: Search())
search_button.grid(row=1,column=2)
#search_button.pack()
Suggestion_label=tk.Label(program, text="Suggestions:") #Create label,textview
Suggestion_label.grid(row=1,column=4) #don't use pack and grid together

## Display image
URL = "https://images.gr-assets.com/books/1447303603m/2767052.jpg"
u = urlopen(URL)
raw_data = u.read()
u.close()
    
im = Image.open(BytesIO(raw_data))
photo = ImageTk.PhotoImage(im)
## create default 5 pictures    
label = tk.Label(image=photo)
label.grid(row=3)
label.image = photo
info1=tk.Label(program,text="1",width=45,wraplength=300,justify=tk.CENTER)
info1.grid(row=3,column=1,columnspan=2)

button1=tk.Button(program,text='>',command=lambda: Suggest(IdList[0]))
button1.grid(row=3,column=3)

suggest1Image=tk.Label(image=photo)
suggest1Image.grid(row=3,column=4)
suggest1Image.image = photo

suggest1Title=tk.Label(program,text="1")
suggest1Title.grid(row=3,column=5)

#label.pack()

label2 = tk.Label(image=photo)
label2.grid(row=4)
label2.image = photo
info2=tk.Label(program,text="2",width=45,wraplength=300,justify=tk.CENTER)
info2.grid(row=4,column=1,columnspan=2)

button2=tk.Button(program,text='>',command=lambda: Suggest(IdList[1]))
button2.grid(row=4,column=3)

suggest2Image=tk.Label(image=photo)
suggest2Image.grid(row=4,column=4)
suggest2Image.image = photo

suggest2Title=tk.Label(program,text="1")
suggest2Title.grid(row=4,column=5)


#label2.pack()

label3 = tk.Label(image=photo)
label3.grid(row=5)
label3.image = photo
info3=tk.Label(program,text="3",width=45,wraplength=300,justify=tk.CENTER)
info3.grid(row=5,column=1,columnspan=2)

button3=tk.Button(program,text='>',command=lambda: Suggest(IdList[2]))
button3.grid(row=5,column=3)

suggest3Image=tk.Label(image=photo)
suggest3Image.grid(row=5,column=4)
suggest3Image.image = photo

suggest3Title=tk.Label(program,text="1")
suggest3Title.grid(row=5,column=5)
#label3.pack()

label4 = tk.Label(image=photo)
label4.grid(row=6)
label4.image = photo
info4=tk.Label(program,text="4",width=45,wraplength=300,justify=tk.CENTER)
info4.grid(row=6,column=1,columnspan=2)

button4=tk.Button(program,text='>',command=lambda: Suggest(IdList[3]))
button4.grid(row=6,column=3)

suggest4Image=tk.Label(image=photo)
suggest4Image.grid(row=6,column=4)
suggest4Image.image = photo

suggest4Title=tk.Label(program,text="1")
suggest4Title.grid(row=6,column=5)
#label4.pack()

label5 = tk.Label(image=photo)
label5.grid(row=7)
label5.image = photo
info5=tk.Label(program,text="5",width=45,wraplength=300,justify=tk.CENTER)
info5.grid(row=7,column=1,columnspan=2)

button5=tk.Button(program,text='>',command=lambda: Suggest(IdList[4]))
button5.grid(row=7,column=3)

suggest5Image=tk.Label(image=photo)
suggest5Image.grid(row=7,column=4)
suggest5Image.image = photo

suggest5Title=tk.Label(program,text="1")
suggest5Title.grid(row=7,column=5)
#label5.pack()
g="h"
IdList=[]
SuggestList=[]
ImageLabelList=[label,label2,label3,label4,label5]
TitleLabelList=[info1,info2,info3,info4,info5]
ButtonList=[button1,button2,button3,button4,button5]
SuggestImageList=[suggest1Image,suggest2Image,suggest3Image,suggest4Image,suggest5Image]
SuggestTitleList=[suggest1Title,suggest2Title,suggest3Title,suggest4Title,suggest5Title]
def Suggest(Book_id):
    global SuggestList
    SuggestList=F.SumMethods(Book_id)
    for i in range(0,5):
        url=F.BookImageUrl(SuggestList[i])
        text="Title: "+F.BookTitle(SuggestList[i])+"\nAuthors: "+F.BookAuthors(SuggestList[i]) 
        DisplayTitle(SuggestTitleList[i],text)
        DisplayImage(SuggestImageList[i],url)
    HideSuggestPart()
    ShowSuggestPart(len(SuggestList))
     
def Search():
    global IdList
    IdList=F.SearchWord(search_entry.get())
    
    for i in range(0,len(IdList)):
        url=F.BookImageUrl(IdList[i])
        text="Title: "+F.BookTitle(IdList[i])+"\nAuthors: "+F.BookAuthors(IdList[i]) 
        DisplayImage(ImageLabelList[i],url)
        DisplayTitle(TitleLabelList[i],text)
    HideSearchPart()
    HideSuggestPart()
    ShowSearchPart(len(IdList))
def HideSuggestPart():
    Items=[suggest1Image,suggest2Image,suggest3Image,suggest4Image,suggest5Image,suggest1Title,suggest2Title,suggest3Title,suggest4Title,suggest5Title]
    for i in Items:
        i.grid_forget()
def ShowSuggestPart(n):
    for i in range(0,n):
        SuggestImageList[i].grid(row=i+3,column=4)
        SuggestTitleList[i].grid(row=i+3,column=5)
def HideSearchPart():
    Items=[label,label2,label3,label4,label5,info1,info2,info3,info4,info5,button1,button2,button3,button4,button5]
    for i in Items:
        i.grid_forget()
def ShowSearchPart(n):
    for i in range(0,n):
        ImageLabelList[i].grid(row=i+3,column=0)
        TitleLabelList[i].grid(row=i+3,column=1,columnspan=2)
        ButtonList[i].grid(row=i+3,column=3)
def ReadIdFromInput():
    IntId=int(search_entry.get())
    g=IntId
    DisplayImagebyID(IntId)
    return IntId
    
def DisplayImagebyID(book_id):
    url=F.BookImageUrl(book_id)
    g=url
    try:
        DisplayImage(url)
    except Exception as e:
        print("type error: " + str(e))
    
def DisplayTitle(Label,Text):
    Label.configure(text=Text)
def DisplayImage(Label,URL):
    
    u = urlopen(URL)
    raw_data = u.read()
    u.close()
    
    im = Image.open(BytesIO(raw_data))
    photo = ImageTk.PhotoImage(im)
    Label.configure(image=photo)
    #label = tk.Label(image=photo)
    Label.image = photo
    #label.pack()


HideSuggestPart()
HideSearchPart()
program.bind("<Return>", DisplayImage)
program.mainloop()