from demoIJMTM.Save_Mysql import functions


def create_journal_logtable(schma_to_write):
    cnx,cursor=functions.creatCursor(schma_to_write,"W")

    Qy=("""create table `log_journals`
            (`id` int UNSIGNED not null auto_increment,
            `Jurl` varchar(300) not null,
            `Jtitle` varchar(300) null,
             primary key (`Jurl`(200)),
             unique key(`id`))""")
    cursor.execute(Qy)

    cnx.commit()
    cursor.close()
    cnx.close()
    return


def Sql_savejnl(Wcursor,url,Jtitle,tablename): # OK no problem!!!

    Jurl='sitemap/page/sitemap/serial/journals/{}/{}'.format(Jtitle[0].lower(),url.split('/')[-1][1:9])

    add_jn=('INSERT ignore into `{}` (`Jurl`,`Jtitle`) values ("{}","{}")'.format(tablename,Jurl,Jtitle))
    Wcursor.execute(add_jn)
    return



#return UTF-8 list of URL
def Reject_Exsting_Journals(schema_to_write):
    cnx,cursor=functions.creatCursor(schema_to_write,'W')
    Qy="select `Jurl` from {}.{} order by `id`".format(schema_to_write,'log_journals')
    cursor.execute(Qy)
    existing_journals=[]
    for n in cursor:
        existing_journals.append("http://api.elsevier.com/{}.html".format(n[0].encode('utf-8')))

    cnx.commit()
    cursor.close()
    cnx.close()

    return existing_journals