import argparse
from faker import Faker
import uuid
import faker_commerce
import decimal
from postgres_con import runSQLStatements
from collections import OrderedDict


faker = Faker()
faker.add_provider(faker_commerce.Provider)
sql_table = 'customer'
print('inital_load: Start')
sqlStatements = []
numberOfRecords = 50

# CREATE TABLE CUSTOMER (
#   ID VARCHAR(255),
#   NAME VARCHAR(255),
#   SIZE INT,
#   DATE DATE,
#   FEEPCT VARCHAR(255),
#   COUNTRY VARCHAR(255)
# );


columns = {
            'ID':'VARCHAR(255)',
            'NAME':'VARCHAR(255)',
            'Size':'INT',
            'Date':'DATE',
            'FEEPCT':'VARCHAR(255)',
            'COUNTRYCODE':'VARCHAR(255)',
            'COUNTRYNAME':'VARCHAR(255)',
            }
countryCodeMapping ={
    '':'US',
    'United Kingdom':'UK',
    'Netherlands':'NL',
    'Holland':'NL',
    'Sweden':'SE'
}
elements = OrderedDict([
    ("US,United States", 0.45),
    ("UK,United Kingdom", 0.30),
    ("ES,Spain", 0.15),
    ("NL,Holland", 0.05),
    ("NL,Netherlands", 0.05) ])



sql_drop = 'DROP TABLE IF EXISTS '+sql_table+' CASCADE;'
sqlStatements.append(sql_drop)

sql_create = 'CREATE TABLE '+sql_table+' ('
for key in columns:
    #print('Key is: '+key +'. Type is '+columns[key])
    sql_create += ' '+(key + ' ' +columns[key]+',')
sql_create = sql_create[:-1] + ');'

sqlStatements.append(sql_create)


for i in range(numberOfRecords):
    sql_insert = "INSERT INTO "+sql_table+" VALUES("
    sql_insert += "'" + str(uuid.uuid1()) +"',"
    sql_insert += "'" + faker.name() +"',"
    sql_insert += str(faker.random_int(min=20, max=90)) +","
    sql_insert += "'" + str(faker.date_between(start_date='-30d', end_date='today')) +"',"
    sql_insert += "'" +str(faker.random_int(min=1, max=100)) +" %',"
    country = faker.random_element(elements)
    sql_insert += "'" + country.split(',')[0] +"',"
    sql_insert += "'" + country.split(',')[1] +"'"
    sql_insert += ")"
    sqlStatements.append(sql_insert)
for line in sqlStatements:
    print(line)
runSQLStatements(sqlStatements)
