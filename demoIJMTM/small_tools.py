# these are some  useful small functions
from Save_Mysql import functions
from Save_Neo4j import myneofun
from py2neo.packages.httpstream import http



def CheckConsistency_neo4jmysql(mysqlschema):
    cnx,cursor=functions.creatCursor(mysqlschema,'W')
    graph=myneofun.Getconnected()
    #count mysql
    mysqltables={'all_keywords':0,'all_authors':0,'whole':0,'all_a2p':0,'all_a2w':0,'all_p2w':0,'all_w2w':0}
    for table in mysqltables.keys():
        Qy=("select count(*) from {}.{}".format(mysqlschema,table))
        cursor.execute(Qy)
        mysqltables[table]=cursor.fetchone()[0]
        print "{}:{}".format(table,mysqltables[table])
    #count neo4j
    cypher=graph.cypher
    neonode={'Word':0,'Author':0,'Paper':0}
    for node in neonode.keys():
        statement='match (n:{}) return count(n)'.format(node)
        neonode[node]=cypher.execute(statement)[0][0]
        print "{}:{}".format(node,neonode[node])
    neorel={'Wrote':0,'Study':0,'Contain':0,'Link':0}
    for rel in neorel.keys():
        statement='match ()-[r:{}]->() return count(r)'.format(rel)
        neorel[rel]=cypher.execute(statement)[0][0]
        print '{}:{}'.format(rel,neorel[rel])

    #compare
    if mysqltables['all_keywords']==neonode['Word']:
        print 'Word OK'
    if mysqltables['all_authors']==neonode['Author']:
        print 'Author OK'
    if mysqltables['whole']==neonode['Paper']:
        print 'Paper OK'
    if mysqltables['all_a2p']==neorel['Wrote']:
        print 'Wrote OK'
    if mysqltables['all_a2w']==neorel['Study']:
        print 'Study OK'
    if mysqltables['all_p2w']==neorel['Contain']:
        print 'Contain OK'
    if mysqltables['all_w2w']==neorel['Link']:
        print 'Link OK'

    return


if __name__=="__main__":
    http.socket_timeout = 9999
    CheckConsistency_neo4jmysql('total_v3_csvneo4j')




