    # this function provides recommendation with respect to tags of the given book id.
import sqlite3
import os
from collections import Counter
import operator
import re
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        #print("connection with the database is established")
        return conn
    except Error as e:
        print(e)
        #print("we have just failed to connect to the database")

    return None
def TagDeneme(id):



   




    


    # first we have to find related tags of read book.

    # simdilik silme === sql_command = "SELECT tag_id FROM book_tags_table WHERE goodreads_book_id = ?"

    database_loc = os.getcwd() + "/Data/SQL" + "/test.db"
    database = database_loc
    # create a database connection
    conn = create_connection(database)

    sql_command_relate_id2book_id = "SELECT best_book_id FROM books_table WHERE id = " + str(id)



    # priority = 1
    # cur = conn.cursor()
    # cur.execute("SELECT tag_id FROM book_tags_table WHERE goodreads_book_id = ? order by count desc limit ?", (priority, 5))
    # rows = cur.fetchall()

    cur = conn.cursor()
    cur.execute(sql_command_relate_id2book_id)
    rows = cur.fetchall()



    #print("most rated 5 tags are = %d" %((for i in range(len(rows))): rows[i]))
    #print("most rated 5 tags are = %d" %     (       (for i in range(len(rows))):(rows[i])                     )                               )



    # now we have 5 most rated tags for the given book. Next thing to do is, find ANOTHER books whose tags are the same.
    # Those books should be the most preferable ones.
    # print('milad')
    # print(rows[0][0])
    # print(type(rows[0][0]))
    # goodreads_book_id = []


    # for i in range(len(rows)):
    #     goodreads_book_id.append(int(rows[i]))

    # goodreads_book_id = goodreads_book_id.append(int(rows[0]))
    #
    # print(goodreads_book_id)
    # print(type(goodreads_book_id))
    goodreads_book_id = rows[0][0]

    sql_command_get_tag_id = "SELECT tag_id FROM book_tags_table WHERE goodreads_book_id = " + str(goodreads_book_id) +  " order by count desc limit 5"

    cur.execute(sql_command_get_tag_id)
    rows_2 = cur.fetchall()


    myTags = []
    for i in range(len(rows_2)):
        myTags.append(rows_2[i][0])

    #myTags = rows_2[0][0]



    #recomBooks = []
    recomBooks = [{} for i in range(len(myTags))]

    for i in range(len(myTags)):
        sql_command_recom_book = "SELECT goodreads_book_id FROM book_tags_table WHERE tag_id = "+ str(myTags[i])+ " order by count desc limit 20"

        cur.execute(sql_command_recom_book)
        rows_3 = cur.fetchall()

        #print(rows_3)

        n = dict(list(enumerate(reversed(rows_3))))
        nn = dict((v,k) for k,v in n.items())

        #recomBooks = recomBooks.append(nn.copy())
        recomBooks[i] = nn

    # for i in range(5):
    #
    #     print(i)
    #     print(recomBooks[i])


    finalDict = recomBooks[0]
    for i in range(len(recomBooks) - 1):
        finalDict = SumDicts(finalDict, recomBooks[i + 1])

    # print('myFinalDict')
    # print(finalDict)

    allDictValues = finalDict.values()
    # print(allDictValues)

    allDictValues = sorted(allDictValues, reverse = True)
    
# print mydict.keys()[mydict.values().index(16)]
    returnList = []

    result=sorted(finalDict.items(), key=operator.itemgetter(1), reverse=True)
    ##get just book ids
    output=[]
    for i in result:
        output.append(i[0])
        
    #convert results to simple integer
    output2=[]
    for i in output:
        output= re.sub('[^0-9]','', str(i))
        output2.append(int(output))
    return output2[0:10]

    #print(returnList)


    #finalDict = {}
    #print(recomBooks[0])
    #print(recomBooks[0].get(28187))
    #finalDict = {x: recomBooks[0].get(x) + recomBooks[1].get(x) for x in set(recomBooks[0]).union(recomBooks[1])}
    # for i in range(len(recomBooks)-3):
    #     finalDict = {x: finalDict.get(x) + recomBooks[i + 2].get(x) for x in set(finalDict).union(recomBooks[i + 2])}

    #c = {x: oo.get(x) + nn.get(x) for x in set(nn).union(oo)}




    #                                                                     cur = conn.cursor()
    #                                                                     cur.execute("SELECT goodreads_book_id FROM book_tags_table WHERE tag_id = ? order by count desc limit ?", (goodreads_book_id, 20))
    #                                                                     rows_2 = cur.fetchall()
    #                                                                     print(rows_2)
                                                                # n = dict(list(enumerate(reversed(rows_2))))
                                                                # o = dict(list(enumerate(reversed(rows_2))))
                                                                #
                                                                # nn = dict((v,k) for k,v in n.items())
                                                                # oo = dict((v,k) for k,v in o.items())
                                                                #
                                                                # print(nn)
                                                                # c = {x: oo.get(x) + nn.get(x) for x in set(nn).union(oo)}
                                                                #
                                                                # print(n)
                                                                # print("this should be the one")
                                                                # print(c)
                                                                #
                                                                #
                                                                # A = {'a':1, 'b':2, 'c':3}
                                                                # B = {'b':3, 'c':4, 'd':5}
                                                                # c = {x: A.get(x, 0) + B.get(x, 0) for x in set(A).union(B)}
                                                                # print(c)
    #
    # print(combine_dicts(new_dict, old_dict, op=operator.add))

    # new_counter = Counter(new_dict)
    # old_counter = Counter(new_dict)

    # print(new_counter + old_counter)
    #print(new_dict)

    # values = ['ali', 'veli', 'deli']
    # new_dict = Counter(dict(list(enumerate(reversed(values)))))
    # old_dict = new_dict
    # print (new_dict)




    # def select_task_by_priority(conn, priority, limit_num):
    #     """
    #     Query tasks by priority
    #     :param conn: the Connection object
    #     :param priority:
    #     :return:
    #     """
    #     cur = conn.cursor()
    #     #cur.execute("SELECT * FROM book_tags_table [bt], tags_table [t]  WHERE bt.tag_id = t.tag_id AND bt.tag_id=?", (priority,))
    #     #cur.execute("SELECT goodreads_book_id FROM book_tags_table WHERE tag_id = ? GROUP BY tag_id ORDER BY count desc limit 3", (priority,))
    #     cur.execute("SELECT goodreads_book_id FROM book_tags_table WHERE tag_id = ? order by count desc limit ?", (priority,limit_num))
    #
    #     rows = cur.fetchall()
    #     print("program is about to start")
    #
    #     for row in rows:
    #         print(row)
    #     return(rows)
    #     print("program should have been finished")
def SumDicts(aDict,bDict):
    sums = {x: aDict.get(x,0) + bDict.get(x,0) for x in set(bDict)| set(aDict)}
    return sums    
a=TagDeneme(1)