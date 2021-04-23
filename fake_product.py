import argparse
from faker import Faker
import uuid
import faker_commerce
import decimal
from postgres_con import runSQLStatements


faker = Faker()
faker.add_provider(faker_commerce.Provider)

sql_table = 'PRODUCT'

def inital_load():
    print('inital_load: Start')
    sqlStatements = []
    numberOfRecords = 100
    columns = {
                'ProductID':'VARCHAR(255)',
                'ProductName':'VARCHAR(255)',
                'ProductCategory':'VARCHAR(255)',
                'Size':'INT',
                'Weight':'NUMERIC',
                'PurchasePrice':'NUMERIC',
                'SellingPrice':'NUMERIC',
                'AmountInStock':'INT',
                'Manufacturer':'VARCHAR(255)',
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
        sql_insert += "'" + faker.ecommerce_name() +"',"
        sql_insert += "'" + faker.ecommerce_category() +"',"
        sql_insert += str(faker.random_int(min=1, max=100)) +","
        sql_insert += str(faker.pydecimal(min_value=2, max_value=50, right_digits=2)) +","
        purchasePrice =  faker.pydecimal(min_value=20, max_value=600, right_digits=2)
        sellingPrice = round(purchasePrice * decimal.Decimal(1.2), 2)
        sql_insert += str(purchasePrice) +","
        sql_insert += str(sellingPrice) +","
        sql_insert += str(faker.random_int(min=50, max=200)) +","
        sql_insert += "'" + faker.company() + "'"
        sql_insert += ")"
        sqlStatements.append(sql_insert)
    runSQLStatements(sqlStatements)


def decrease_stock():
    print('decrease-stock')
    numberOfRecords = 40
    sqlStatements = []
    for i in range(numberOfRecords):
        sql_insert = "INSERT INTO "+sql_table+" VALUES("
        sql_insert += "'" + str(uuid.uuid1()) +"',"
        sql_insert += "'" + faker.ecommerce_name() +"',"
        sql_insert += "'" + faker.ecommerce_category() +"',"
        sql_insert += str(faker.random_int(min=1, max=100)) +","
        sql_insert += str(faker.pydecimal(min_value=2, max_value=50, right_digits=2)) +","
        purchasePrice =  faker.pydecimal(min_value=20, max_value=600, right_digits=2)
        sellingPrice = round(purchasePrice * decimal.Decimal(1.2), 2)
        sql_insert += str(purchasePrice) +","
        sql_insert += str(sellingPrice) +","
        sql_insert += str(faker.random_int(min=0, max=15)) +","
        sql_insert += "'" + faker.company() + "'"
        sql_insert += ")"
        sqlStatements.append(sql_insert)
    runSQLStatements(sqlStatements)
def missing_category():
    print('missing_category-stock')
    numberOfRecords = 14
    sqlStatements = []
    for i in range(numberOfRecords):
        sql_insert = "INSERT INTO "+sql_table+" VALUES("
        sql_insert += "'" + str(uuid.uuid1()) +"',"
        sql_insert += "'Electric Guitar',"
        sql_insert += "NULL,"
        sql_insert += str(faker.random_int(min=1, max=100)) +","
        sql_insert += str(faker.pydecimal(min_value=2, max_value=50, right_digits=2)) +","
        purchasePrice =  faker.pydecimal(min_value=20, max_value=600, right_digits=2)
        sellingPrice = round(purchasePrice * decimal.Decimal(1.2), 2)
        sql_insert += str(purchasePrice) +","
        sql_insert += str(sellingPrice) +","
        sql_insert += str(faker.random_int(min=0, max=15)) +","
        sql_insert += "'" + faker.company() + "'"
        sql_insert += ")"
        sqlStatements.append(sql_insert)
    runSQLStatements(sqlStatements)
def invalid_price():
    print('invalid_price')
    numberOfRecords = 5
    sqlStatements = []
    for i in range(numberOfRecords):
        sql_insert = "INSERT INTO "+sql_table+" VALUES("
        sql_insert += "'" + str(uuid.uuid1()) +"',"
        sql_insert += "'" + faker.ecommerce_name() +"',"
        sql_insert += "'Grocery',"
        sql_insert += str(faker.random_int(min=1, max=100)) +","
        sql_insert += str(faker.pydecimal(min_value=2, max_value=50, right_digits=2)) +","
        purchasePrice =  faker.pydecimal(min_value=20, max_value=600, right_digits=2)
        sellingPrice = round(purchasePrice * decimal.Decimal(0.2), 2)
        sql_insert += str(purchasePrice) +","
        sql_insert += str(sellingPrice) +","
        sql_insert += str(faker.random_int(min=0, max=15)) +","
        sql_insert += "'" + faker.company() + "'"
        sql_insert += ")"
        sqlStatements.append(sql_insert)
    runSQLStatements(sqlStatements)


FUNCTION_MAP = {'inital_load' : inital_load,
                'decrease_stock' : decrease_stock,
                'missing_category' : missing_category,
                'invalid_price' : invalid_price
                }


parser = argparse.ArgumentParser("fake_command")
parser.add_argument("command", help="Use inital_load to load the db and decrease_stock to feed", type=str)
args = parser.parse_args()
func = FUNCTION_MAP[args.command]
func()
