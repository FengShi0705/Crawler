# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import os.path

import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem
import codecs
from Private import functions
#############################from Save_Neo4j import myneofun
from Save_Neo4j import myneofuncollate
from Save_Log import logfun
from py2neo.server import GraphServer


class index_Pipeline(object):
    def __init__(self):
        # server = GraphServer(home="D:/neo4jzip")
        mysqlschema='total_v3_csvneo4j'
        # self.graph=myneofuncollate.Getconnected()
        # print self.graph.neo4j_version
        self.Wcnx,self.Wcursor = functions.creatCursor(mysqlschema,'W')

        assert mysqlschema=='total_v3_csvneo4j',"mysql database location wrong"
        #assert server.conf.get("neo4j-server", "org.neo4j.server.database.location")==u'D:/KeywordsLink/database/neo4j/total_v3_csvneo4j.db', "neo4j database location wrong"

    def process_item(self, item, spider):

        # ckeck whether the item is empty:
        if item.get('keywords')==None:
            raise DropItem('Empty. item count: %d' % item['count'])
        else:
            #check existence of this paper
            if functions.checkextc('Whole',self.Wcursor,item['URL']):
                raise DropItem('Duplicated paper: {}'.format(item['URL']))
            else:
                #save information to Mysql and Neo4j
                aids,wids,pid = functions.Allsql_onepaper('Whole',self.Wcursor,item)
                #save neo4j
                #myneofuncollate.Allneo_onepaper(self.graph,aids,wids,pid,item)
                #log journals
                logfun.Sql_savejnl(self.Wcursor,item['URL'],item['journal'],'log_journals')

                self.Wcnx.commit()
                return item


