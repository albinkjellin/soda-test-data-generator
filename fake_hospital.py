import argparse
from faker import Faker
import uuid
import faker_commerce
import decimal
from collections import OrderedDict
from postgres_con import runSQLStatements


faker = Faker()
faker.add_provider(faker_commerce.Provider)

sql_table = 'HOSPITALS'
elements = OrderedDict([
    ("Sacred Heart", 0.45),
    ("County General Hospital", 0.30),
    ("Princeton–Plainsboro Teaching Hospital", 0.15)])

def inital_load():
    print('inital_load: Start')
    sqlStatements = []
    numberOfRecords = 30
    columns = {
                'PatientID':'VARCHAR(255)',
                'Hospital':'VARCHAR(255)',
                'Week':'INT',
                'ClaimAmount':'NUMERIC',
                }



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
        sql_insert += "'" + faker.random_element(elements) +"',"
        sql_insert += "1,"
        sql_insert += str(faker.pydecimal(min_value=100, max_value=4000, right_digits=2))
        sql_insert += ");"
        sqlStatements.append(sql_insert)
    for i in sqlStatements:
        print(i)
    runSQLStatements(sqlStatements)


def increase_claims_sacred_heart():
    print('increase_claims_sacred_heart')
    numberOfRecords = 30
    sqlStatements = []
    for i in range(numberOfRecords):
        sql_insert = "INSERT INTO "+sql_table+" VALUES("
        sql_insert += "'" + str(uuid.uuid1()) +"',"
        hospital = faker.random_element(elements)
        sql_insert += "'" +hospital+"',"
        sql_insert += "2,"
        if hospital == 'Sacred Heart':
            sql_insert += str(faker.pydecimal(min_value=1000, max_value=4000, right_digits=2))
        else:
            sql_insert += str(faker.pydecimal(min_value=100, max_value=400, right_digits=2))
        sql_insert += ")"
        sqlStatements.append(sql_insert)
    for i in sqlStatements:
        print(i)
    runSQLStatements(sqlStatements)


FUNCTION_MAP = {'inital_load' : inital_load,
                'increase_claims_sacred_heart' : increase_claims_sacred_heart,
                }


parser = argparse.ArgumentParser("fake_command")
parser.add_argument("command", help="Use inital_load to load the db and decrease_stock to feed", type=str)
args = parser.parse_args()
func = FUNCTION_MAP[args.command]
func()
