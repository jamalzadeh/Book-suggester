# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 22:28:31 2018

@author: Milad Jamalzadeh
"""
import sqlite3
import StaticStrings as STR
import csv
import re
import operator
import time
import xml.etree.ElementTree as ET
import recomByTag as R
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

CsvFolderPath=STR.CsvFolderPath
SQLFolderPath=STR.SQLFolderPath
XMLFolderPath=STR.XMLFolderPath
NumberofSearchResults=5
users=[] #top users from rating table
bookId=0
FirstMethod=0
SecondMethod=0
ThirdMethod=0
def CsvToList(Filename,HeadersIncluded):
    #Usage Example>> a,b=CsvToList("Students Information.csv",True) 
    Headers=[]
    OutputList=[]
    CsvFilePath=CsvFolderPath+Filename
    CsvFile=open(CsvFilePath,"r",encoding="utf8")
    FileContent=CsvFile.read()
    List=FileContent.splitlines()
    if HeadersIncluded:
        Headers=List[0].split(',')
        for i in range(1,len(List)):
            OutputList.append(List[i])
    else:
        for i in range(0,len(List)):
            OutputList.append(List[i])
    return OutputList,Headers
  
def CsvToList2(Filename,HeadersIncluded):
    #Usage Example>> a,b=CsvToList("Students Information.csv",True) 
    Headers=[]
    data=[]
    CsvFilePath=CsvFolderPath+Filename
    with open(CsvFilePath,"r",encoding="utf8") as f:
        datareader = csv.reader(f, delimiter=',')
        data = []
        for row in datareader:
                data.append(row)
        if HeadersIncluded:
            Headers=data[0]
            data=data[1:]
    return data,Headers
def CreateSQLTable(Filename,TableName,Headers,HeadersType):
    #Usage Example>>   CreateSQLTable("test.db","TAble1",b,["int","float","int","float"])
    SQLFilePath=SQLFolderPath+Filename
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor()
    HeaderString=""
    for i in range(0,len(Headers)):
        HeaderString=HeaderString+Headers[i]+" "+HeadersType[i]+","
    HeaderString=HeaderString[:-1]
    sql_command="CREATE TABLE IF NOT EXISTS "+TableName+"("+HeaderString+");"
    cursor.execute(sql_command)
    connection.commit()
    connection.close()
 
def GetQSLColumnType(FileName,TableName,ColumnName):
    #This function is not working
    SQLFilePath=SQLFolderPath+FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor()
    sql_command="SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "+TableName+" AND "+"COLUMN_NAME = "+ColumnName
    cursor.execute(sql_command)
    res = cursor.fetchone() 
    connection.commit()
    connection.close()
    return res

def InsertSignleRowSQL(FileName,TableName,Columns,data):
    #Usage Example>>   InsertSignleRowSQL("test.db","TAble2",b,[12,123.4,12,"Milad"])
    SQLFilePath=SQLFolderPath+FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor()
    seperator = ', '
    ColumnString=seperator.join(Columns)
    DataString=str(data).strip('[]')
    sql_command="INSERT INTO "+TableName+"("+ColumnString+")"+" VALUES("+DataString+");"
    cursor.execute(sql_command)
    connection.commit()
    connection.close()

def InsertMultipleRowSQL(FileName,TableName,Columns,data):
    #Usage Example>>>    InsertMultipleRowSQL("test.db","TAble2",b,[[12,123.4,12,"omer"],[13,15.6,243,"ozan"]]) 
    SQLFilePath=SQLFolderPath+FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor()
    seperator = ', '
    ColumnString=seperator.join(Columns)
    TypeString=""
    for i in data[0]:
        TypeString=TypeString+"?,"
    TypeString = TypeString[:-1]
    sql_command="INSERT INTO "+TableName+"("+ColumnString+")"+" VALUES("+TypeString+")"
    number_of_rows = cursor.executemany(sql_command, data)
    connection.commit()
    connection.close()

def SuggestBook_tag(goodreads_book_id):
    #goodreads_book_id= best_book_id from books table
    ## read tags of book in descending number
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor()
    sql_command="SELECT "+STR.Tag_Id_Header+" FROM "+STR.Book_Tags_Table+" where "+STR.Tag_Id_Header+"="+str(goodreads_book_id)+" ORDER BY "+STR.Tag_Counter_Header+" DESC"
    cursor.execute(sql_command)
    connection.commit()
    res = cursor.fetchone() 
    #Check to see if 
    if len(res)<STR.Top_Tags_Number:
        TopTags=res[0:len(res)]
    else:
        TopTags=res[0:STR.Top_Tags_Number]
    return TopTags
def TopRating(book_id):
    #book_id should be in number format
    #usage example=   TopRating(9997)
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor()
    sql_command="SELECT "+STR.Rating+" FROM "+STR.Rating_Table+" where "+ STR.Book_Id +"="+str(book_id)+" ORDER BY "+STR.Rating+" DESC"+" LIMIT 10"
    #returns top 10 rating for each book
    cursor.execute(sql_command)
    
    res = cursor.fetchall() #example output=(5,)
    
    connection.close()
    if res== None:
        res=0 #if there isn't any rating for this book it will return zero
    else:
        #return minimume tag in top  10 tag
        res = re.sub('[^0-9]','', str(res[-1]))
    return res

def TopUsersFrom_rating_table(book_id):
    #This function find the users who have given highest rating to one book and sort them according to how many times they have give rating to any book
    #usage example: a=TopUsersFrom_rating_table(1)
    output=[];
    global bookId
    global users
    if book_id!=bookId:
        SQLFilePath=SQLFolderPath+STR.FileName
        connection = sqlite3.connect(SQLFilePath)
        cursor = connection.cursor()
        sql_command="SELECT "+STR.User_Id+" FROM "+STR.Rating_Table+" where "+STR.Rating+">="+str(TopRating(book_id))+" and "+STR.Book_Id+"="+str(book_id) +" order by(select "+STR.User_Id+" FROM "+STR.Rating_Table+" group by "+STR.User_Id+" order by count(*)) desc limit 20"
        #sql_command= "SELECT user_id FROM ratings_table where book_id = 1 AND rating = 5 order by (SELECT user_id FROM ratings_table group by user_id order by count(*) ) desc limit 5"
        cursor.execute(sql_command)
        
        row = cursor.fetchall()
        cursor.close()
        connection.close()
        #import re
        for i in row:
            result = re.sub('[^0-9]','', str(i))
            output.append(int(result))
        bookId=book_id
    else:
        output=users
    users=output
    return output #return a list of userids as integer
def SuggestBooksFrom_toRead_table(book_id):
    users=TopUsersFrom_rating_table(book_id)
    userlist="("
    for i in users:
        userlist=userlist+str(i)+","
    userlist=userlist[:-1]+")"
    #userlist in applicable in sql command for IN
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor()
    sql_command="select "+STR.Book_Id+" FROM "+STR.ToRead_Table+" where "+STR.User_Id +" IN "+userlist
    cursor.execute(sql_command)
    row = cursor.fetchall()
    cursor.close()
    connection.close()
    books={}
    for i in row:
        if i in books.keys():
            books[i]=1+books[i]
        else:
            books[i]=1
    if book_id in books.keys():
        del books[book_id]
    result=sorted(books.items(), key=operator.itemgetter(1), reverse=True)
    result=result[0:10]
    ##get just book ids
    output=[]
    for i in result:
        output.append(i[0])
        
    #convert results to simple integer
    output2=[]
    for i in output:
        output= re.sub('[^0-9]','', str(i))
        output2.append(int(output))
    return output2

def SuggestBooksFrom_rating_table(book_id):
    #sample_usage>>  SuggestBooksFrom_rating_table(1)
    Suggestion=10 #numbesr of books you want to suggest
    global users
    users=TopUsersFrom_rating_table(book_id)
    userlist="("
    for i in users:
        userlist=userlist+str(i)+","
    userlist=userlist[:-1]+")"
    #userlist in applicable in sql command for IN
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor()
    sql_command="select "+STR.Book_Id+" ,"+STR.Rating+" FROM "+STR.Rating_Table+" where "+STR.User_Id +" IN "+userlist
    cursor.execute(sql_command)
    row = cursor.fetchall()
    cursor.close()
    connection.close()
    books={}
    for i in row:
        if i[0] in books.keys():
            books[i[0]]=i[1]+books[i[0]]
        else:
            books[i[0]]=i[1]
    if book_id in books.keys():
        del books[book_id]
    #import operator
    #sort books in descending order according to total points
    result=sorted(books.items(), key=operator.itemgetter(1), reverse=True)
    result=result[0:10]
    
    ##get just book ids
    output=[]
    for i in result:
        output.append(i[0])
    return output

def BookImageUrl(bookid):
    #sample usage>> a=BookImageUrl(1) 
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor() 
    sql_command="select "+STR.Image_URL+" FROM "+STR.Book_Info_Table+" where "+STR.Id+"="+str(bookid)
    
    cursor.execute(sql_command)
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row[0]

def BookTitle(bookid):
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor() 
    sql_command="select "+STR.Book_Title+" FROM "+STR.Book_Info_Table+" where "+STR.Id+"="+str(bookid)
    cursor.execute(sql_command)
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row[0]
def BookAuthors(bookid):
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor() 
    sql_command="select "+STR.Book_Authors+" FROM "+STR.Book_Info_Table+" where "+STR.Id+"="+str(bookid)
    cursor.execute(sql_command)
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row[0]
def SearchWord(word):
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor() 
    sql_command="select "+STR.Id+" FROM "+STR.Book_Info_Table+" where ( "+STR.Book_Original_Title+" Like " +"'%"+word+"%'"+" or "+STR.Book_Title+" Like " +"'%"+word+"%'"+" or "+STR.Book_Authors+" Like " +"'%"+word+"%'"+")"
    
    cursor.execute(sql_command)
    row = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(row)<NumberofSearchResults:
        result=row
    else:
        result=row[0:NumberofSearchResults]
    #convert to int list  
    outputlist=[]
    for i in range(0,len(result)):
        outputlist.append(list(result[i])[0])
        
    return outputlist
def SumMethods(book_id):
    a=SuggestBooksFrom_rating_table(book_id)
    b=SuggestBooksFrom_toRead_table(book_id)
    c=R.TagDeneme(book_id)
    #giving value to each book id
    #first one has higher value
    L=len(a)
    aDict={}
    bDict={}
    cDict={}
    for i in range(0,len(a)):
        aDict[a[i]]=L
        bDict[b[i]]=L
        cDict[c[i]]=L
        L=L-1
    sum = {x: aDict.get(x,0) + bDict.get(x,0) for x in set(bDict)| set(aDict)}
    result=sorted(sum.items(), key=operator.itemgetter(1), reverse=True)
    ##get just book ids
    output=[]
    for i in result:
        output.append(i[0])
    output=output[0:5]
    return output
def GoodreadsToId(goodread_id):
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor() 
    sql_command="select "+STR.Id+" FROM "+STR.Book_Info_Table+" where best_book_id =  "+str(goodread_id)
    cursor.execute(sql_command)
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row[0]

def IdToBook_id(ID):
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor() 
    sql_command="select book_id FROM "+STR.Book_Info_Table+" where id =  "+str(ID)
    cursor.execute(sql_command)
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row[0]
def SumDicts(aDict,bDict):
    sums = {x: aDict.get(x,0) + bDict.get(x,0) for x in set(bDict)| set(aDict)}
    return sums
def BooksFromXml(book_id):
    XMLFilePath=XMLFolderPath+str(IdToBook_id(book_id))+".xml"
    tree = ET.parse(XMLFilePath)
    root = tree.getroot()
    index=0
    book=root[1]
    for i in range(0,len(book)):
        if book[i].tag=='similar_books':
            index=i
            break    
    similars=book[index]
    outputlist=[]
    for book in similars:
        ID=book[0]
        print(ID.text)
        try:
            outputlist.append(GoodreadsToId(int(ID.text)))
        except Exception as e:
            print("type error: " + str(e))
    return outputlist
def GetTagID(TagString):
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor() 
    sql_command="select tag_id FROM tags_table  where tag_name =  '"+TagString+"'"
    cursor.execute(sql_command)
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row[0]
def GetTagNumbers(year):
    SQLFilePath=SQLFolderPath+STR.FileName
    connection = sqlite3.connect(SQLFilePath)
    cursor = connection.cursor() 
    output=[]
    for i in STR.TagIdList:
        sql_command="SELECT COUNT(*) FROM book_tags_table WHERE goodreads_book_id IN (SELECT best_book_id FROM books_table WHERE original_publication_year ="+str(year)+" ) and tag_id="+str(i) 
        cursor.execute(sql_command)
        row = cursor.fetchone()
        if row!=None:
            output.append(row[0])
        else:
            output.append(0)
    cursor.close()
    connection.close()
    return output
def GetTagratios(TagNumbers):
    sum=0
    for i in TagNumbers:
        sum=sum+i
    if sum!=0:
        newList = [x /sum for x in TagNumbers]
    else:
        newList=[0,0,0,0,0]
    return newList




    

    
    
     
            
 

        