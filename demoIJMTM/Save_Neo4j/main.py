#OK no problem!!!


import myneofun

#graph
graph=myneofun.Getconnected()
#index
try:
    myneofun.Create_index(graph)
except:
    print "Already create index and constraint"
else:
    print "Create index and constraint"





cnx,cursor=myneofun.cursor_mysql('total')

for i in xrange(6,7):#1288379):
    URL,title,journal,date,authors,keytext,keywords = myneofun.info_onepaper_mysql(cursor,'whole',i)
    num=len(list(graph.find("Paper","URL",URL)))

    assert num<=1, "{} same URLs exist: {}".format(num,URL)

    if num==0:
        WNs=myneofun.CreateUnique_Node_Word(graph,keywords)
        PN=myneofun.CreateUnique_Node_Paper(graph,URL,title,journal,date,keytext)
        ANs=myneofun.CreateUnique_Node_Author(graph,authors)

        myneofun.create_wholerel(graph,ANs,WNs,PN)

    else:
        raise TypeError("The URLs saved in mysql are unique. Get the same URL from mysql twice: {}".format(URL))

    print "finished: {}".format(i)



