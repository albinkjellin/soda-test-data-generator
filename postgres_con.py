import psycopg2



def runSQLStatements(sqlStatements):
    conn = psycopg2.connect(
    	user='user', 
    	password='pw', 
    	host='localhost', 
    	port='5432', 
    	database='sodademo1')
    cur = conn.cursor()
    for statement in sqlStatements:
        cur.execute(statement)
    conn.commit()
    cur.close()
    conn.close()


# conn = psycopg2.connect(user='albin', password='soda', host='localhost', port='5432', database='sodademo1')
# cur = conn.cursor()




# conn.commit()
# cur.close()
# conn.close()
