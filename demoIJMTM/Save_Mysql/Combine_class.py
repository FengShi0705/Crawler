# This script does:
#First, lemmatize the existing data of all tables in one schema, and then save these data into a new database in mysql


import mysql.connector
from functions import *
import re
import datetime
import codecs
from scrapy.loader.processors import Join


# do jobs like combine, copy, process and lemmatize for existing data
class mysql_csv_neo4j:



    #create tables
    def create_tables(self,schma_to_write): #OK, no problem !!!
        #load cursor
        cnx,cursor=creatCursor(schma_to_write,"W")

        #create table for allkeywords, give primary index on `word`.
        #Since autoincrement need to be index, give `id` unique index
        Qy=("""create table `all_keywords`
               (`id` bigint UNSIGNED not null auto_increment,
                `word` varchar(300) not null,
                primary key (`word`(200)),
                unique key(`id`))
                """)
        cursor.execute(Qy)


        #create allauthors, give primary index on `author`.
        #Since autoincrement need to be index, give `id` unique index
        Qy=("""create table `all_authors`
               (`id` bigint UNSIGNED not null auto_increment,
                `author` varchar(300) not null,
                primary key (`author`(200)),
                unique key(`id`))
                """)
        cursor.execute(Qy)





        #create table for all w2w, and reference allw2w(id) to allkeywords(id)
        Qy=("create table `all_w2w` "
            "("
            "`rowid` bigint unsigned not null, "
            "`colid` bigint unsigned not null, "
            "`value` int default 0 not null, "
            "`journals` longtext not null, "
            "primary key (`rowid`,`colid`), "
            "index(`colid`), "
            "Foreign Key (`rowid`) REFERENCES `all_keywords`(`id`), "
            "Foreign Key (`colid`) REFERENCES `all_keywords`(`id`)"
            ")")
        cursor.execute(Qy)


        #create table for all a2w, and reference wid back to words in allkeywords(id)
        Qy=("""create table `all_a2w`
               (`aid` bigint unsigned not null,
               `wid` bigint UNSIGNED not null,
               `value` int default 0 not null,
               primary key (`aid`,`wid`),
               index(`wid`),
               Foreign Key (`aid`) References `all_authors`(`id`),
               Foreign Key (`wid`) References `all_keywords`(`id`))""")
        cursor.execute(Qy)





        #create table for whole information
        Qy=("""CREATE TABLE `Whole`
               (`id` bigint unsigned not null auto_increment,
               `URL` varchar(200) not null,
               `title` varchar(1000) null,
               `Author` varchar(2000) null,
               `Journal` varchar(1000) null,
               `date` date null,
               `Keytext` varchar(3000) not null,
               PRIMARY KEY (`URL`),
               Unique Key(`id`))""")
        cursor.execute(Qy)


        #create all_p2w table
        Qy=("""create table `all_p2w`
               (`pid` bigint unsigned not null,
               `wid` bigint UNSIGNED not null,
               primary key (`pid`,`wid`),
               index(`wid`),
               Foreign Key (`pid`) References `Whole`(`id`),
               Foreign Key (`wid`) References `all_keywords`(`id`))""")
        cursor.execute(Qy)


        #create all_a2p table
        Qy=("""create table `all_a2p`
               (`aid` bigint unsigned not null,
               `pid` bigint UNSIGNED not null,
               primary key (`aid`,`pid`),
               index(`pid`),
               Foreign Key (`aid`) References `all_authors`(`id`),
               Foreign Key (`pid`) References `Whole`(`id`))""")
        cursor.execute(Qy)






        cnx.commit()
        cursor.close()
        cnx.close()

        return





#deal with all tables in a schema
    #ReadSchema is the schema to deal with
    #WriteSchema is the schema to write in
    def wholeprocess(self,ReadSchema,WriteSchema,Begin_id):# OK no problem

        #load cursor
        Rcnx,Rcursor = creatCursor(ReadSchema,"R")
        Wcnx,Wcursor = creatCursor(WriteSchema,"W")

        #get information from Begin_id
        RQy=("select * from `whole` where `id`>={} order by `id`".format(Begin_id))
        Rcursor.execute(RQy)

        print "BEGIN from old pid:{}- {}".format(Begin_id,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        #fetch
        piece=Rcursor.fetchone()

        while piece is not None:
            URL=piece[1].encode('utf-8') #string utf-8
            title=piece[2].encode('utf-8').replace(';','').replace('\n','') #string utf-8

            authortext=piece[3].encode('utf-8').replace(';','').replace('\n','') #string utf-8
            authors=filter(None,authortext.split('<>')) #list utf-8

            journal=piece[4].encode('utf-8') #string utf-8
            date=piece[5] #date time
            keytext=piece[6].encode('utf-8').replace('\n','') #string utf-8

            keywords=lemma_listwords(keytext.decode('utf-8').split('<>')) #list utf-8 lemmatized
            keywords=[wd for wd in keywords if len(wd)<100] #filter long words


            print "Not commit. Accessed old pid: {}     - {}".format(piece[0],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            handle_alltable ( 'Whole',Wcursor, URL, title, authortext, journal, date, keytext,keywords,authors)



            if piece[0]%2000==0:
                Wcnx.commit()
                print "Already COMMIT {} <=old pids <= {}".format(Begin_id,piece[0])

            #next information of paper
            piece=Rcursor.fetchone()


        Wcnx.commit()
        Wcursor.close()
        Wcnx.close()

        print "FINISHED!!! Commit all {} <=old pid - {}".format(Begin_id,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


        Rcnx.commit()
        Rcursor.close()
        Rcnx.close()


        return


#this whole script finished no problem!!!