#include functions for neo4j
from py2neo.schema import SchemaResource
from py2neo import authenticate, Graph
from py2neo import Node, Relationship
import mysql.connector
import string
from scrapy.loader.processors import Join
from nltk.stem import WordNetLemmatizer
import nltk



#get connection to server
#return a connected graph
def Getconnected(): #OK no problem!!!
    authenticate("localhost:7474", "neo4j", "Lostyourface123")
    graph = Graph("http://localhost:7474/db/data/")

    return graph




#create indexes and unique_constraints on the graph
#input a graph
def Create_index(graph): #OK no problem!!!
    graph.schema.create_uniqueness_constraint("Word","wid")
    graph.schema.create_uniqueness_constraint("Word","name")
    graph.schema.create_uniqueness_constraint("Paper","pid")
    graph.schema.create_uniqueness_constraint("Paper","URL")
    graph.schema.create_uniqueness_constraint("Author","aid")
    graph.schema.create_uniqueness_constraint("Author","name")



# Create words nodes
# input words is a list, UTF-8 string, input wids is a int list
# return a list of words nodes objects
def CreateUnique_Node_Word(graph,words,wids): #OK no problem!!!

    nodes=[]
    for i,word in enumerate(words):
        node=graph.merge_one("Word","name",word)
        node.properties["wid"]=wids[i]
        node.push()
        nodes.append(node)

    return nodes




# Create a paper node
# input information of a paper are UTF-8. pid is int
# return the paper node object
def CreateUnique_Node_Paper(graph,pid,URL,title,Journal,date,Keytexts): #OK no problem!!!

    paper=graph.merge_one("Paper","URL",URL)
    paper.properties["pid"]=pid
    paper.properties["title"]=title
    paper.properties["Journal"]=Journal
    paper.properties["date"]=date
    paper.properties["Keytexts"]=Keytexts

    paper.push()

    return paper



# create authors nodes
# input authors is a list, UTF-8 string. input aids is a int list
# return a list of Authors nodes objects
def CreateUnique_Node_Author(graph,authors,aids): # OK no problem!!!

    nodes=[]

    for i,author in enumerate(authors):
        node=graph.merge_one("Author","name",author)
        node.properties["aid"]=aids[i]
        node.push()
        nodes.append(node)

    return nodes



# create relationship between two words
# paper,start,end are the nodes objects
def Two_nodes_words(graph,paper,start,end): # OK no problem!!!

    link="Link"
    ijournal=paper.properties["Journal"]

    rel=list(graph.match(start_node=start,end_node=end,bidirectional=True))
    assert len(rel)<=1, "More than one relations between word:{} and word:{}".format(start.properties["name"],end.properties["name"])

    #if no relationship
    if len(rel)==0:
        newR=graph.create_unique(Relationship(start,link,end))[0]
        newR.properties["Journals"]=[ijournal]
        newR.properties["weight"]=1
        newR.push()
    else: #have relationship
        if ijournal not in rel[0].properties["Journals"]:
            rel[0].properties["Journals"].append(ijournal)
        rel[0].properties["weight"]+=1
        rel[0].push()

    return



#create relationship from start author object to end word object
def Two_nodes_AW(graph,start,end): # OK no problem!!!

    link="Study"

    rel=list(graph.match(start_node=start,end_node=end,bidirectional=False))
    assert len(rel)<=1, "More than one relation between author:{} and word:{}".format(start.properties["name"],end.properties["name"])

    #if no relationship
    if len(rel)==0:
        newR=graph.create_unique(Relationship(start,link,end))[0]
        newR.properties["weight"]=1
        newR.push()
    else: #have relationship
        rel[0].properties["weight"]+=1
        rel[0].push()

    return



#create the relationships between all the objects of a single paper
#authors,words,paper are nodes objects
def create_wholerel(graph,authors,words,paper): #OK no problem!!!

    #P2W
    for word in words:
        graph.create_unique(Relationship(paper,"Contain",word))

    #A2P
    for author in authors:
        graph.create_unique(Relationship(author,"Wrote",paper))

    #A2W
    for author in authors:
        for word in words:
            Two_nodes_AW(graph,author,word)

    #W2W
    x=len(words)
    sort_words=sorted(words,key=lambda s: s.properties['wid'])
    for i in xrange(0,x-1):
        for j in xrange(i+1,x):
            Two_nodes_words(graph,paper,sort_words[i],sort_words[j])

    return



# save all the nodes and relationships of one paper into neo4j
# all input are UTF-8
def Allneo_onepaper(graph,aids,wids,pid,item):
    WNs=CreateUnique_Node_Word(graph,item['keywords'],wids)
    ANs=CreateUnique_Node_Author(graph,item['authors'],aids)
    PN=CreateUnique_Node_Paper(graph,pid,item['URL'],item['title'],item['journal'],item['date'],item['neoKeytexts'])

    create_wholerel(graph,ANs,WNs,PN)

    return













