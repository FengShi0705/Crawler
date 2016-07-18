from Combine_class import mysql_csv_neo4j

Tonew=mysql_csv_neo4j()

#create tables
Tonew.create_tables('total_v3_csvneo4j')

Tonew.wholeprocess('total','total_v3_csvneo4j',1)

print 'DONE !!!!!!!!!!!!!!!!!!!!'
