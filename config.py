import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user='root',
                                  password='1234',
                                  host='127.0.0.1')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
cursor = cnx.cursor()

DB_NAME = 'MarketStockSystem'
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


########## Tables ###########
TABLES = {}
TABLES['user'] = (
    "CREATE TABLE `user` ("
    "  `id_number` int(10) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(20),"
    "  `surname` varchar(20),"
    "  `marketname` varchar(20),"
    "  `phone` varchar(20),"
    "  `email` varchar(50),"
    "  `password` varchar(20),"
    "  `job` varchar(20),"
    "  `salary` varchar(20),"
    "  `gender` enum('Owner','Employee'),"
    "  PRIMARY KEY (`id_number`,`email`)"
    ") ENGINE=InnoDB")

TABLES['market'] = (
    "CREATE TABLE `market` ("
    "  `name` varchar(20),"
    "  `phone` varchar(20),"
    "  `address` varchar(100),"
    "  PRIMARY KEY (`name`,`phone`)"
    ") ENGINE=InnoDB")

TABLES['product'] = (
    "CREATE TABLE `product` ("
    "  `product_id` int (6) NOT NULL AUTO_INCREMENT,"
    "  `kind` varchar(20),"
    "  `brand` varchar(20),"
    "  `name` varchar(20),"
    "  `Ex_date` varchar(10),"
    "  `price` varchar(10),"
    "  `weight` varchar(10),"
    "  `amount` varchar(20),"
    "  `marketname` varchar(20),"
    "  PRIMARY KEY (`product_id`)"
    ") ENGINE=InnoDB")

TABLES['retailer'] = (
    "CREATE TABLE `retailer` ("
    "  `name` varchar(20),"
    "  `phone` varchar(20),"
    "  `address` varchar(100),"
    "  PRIMARY KEY (`name`,`phone`)"
    ") ENGINE=InnoDB")


TABLES['record'] = (
    "CREATE TABLE `record` ("
    "  `id` int (6) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(20),"
    "  `amount` varchar(10),"
    "  `price` varchar(10),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

######### Insert tables ############
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")



########## Data ###########
product_insert_query = """INSERT INTO product (product_id,kind, brand, name, Ex_date, price, weight, amount, marketname) 
                           VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s) """

product_list = [('1','Dairy', 'BiliBili','Egg','2021-07-13', '20', '100','1000','market1'),
                   ('2','Dairy', 'Sek','Milk','2021-07-15', '10', '1000','1000','market1'),
                   ('3','Groceries', 'RetailerPazari','Tomato','2021-08-13', '5', '1000','1000','market1'),
                   ('4','Groceries', 'RetailerPazari', 'Orange', '2021-09-06', '4', '1000','1000', 'market1'),
                   ('5','Groceries', 'RetailerPazari', 'Banana', '2021-11-21', '8', '1000','1000', 'market1'),
                   ('6','Snacks', 'Nestle', 'Kitkat', '2022-27-4', '3', '80','1000', 'market1'),
                   ('7','Snacks', 'mnm', 'M&M', '2022-18-12', '5', '60','1000', 'market1'),
                   ('8','Beverage', 'CocaCola', 'CocaCola', '2022-12-02', '6', '1000' ,'1000', 'market1'),
                   ('9','Beverage', 'CocaCola', 'Fanta', '2022-1-09', '6', '1000', '1000', 'market1'),
                   ('10','Animal', 'Whiskas', 'Whiskas', '2021-12-29', '6', '1000', '1000', 'market1'),
                   ('11','Personal Care', 'Clear', 'Shampoo', '2023-12-12', '15', '250', '1000', 'market1'),
                   ('12','Personal Care', 'Colgate', 'Toothbrush', '', '10', '50', '1000', 'market1')]

record_insert_query = """INSERT INTO record (id,name,amount,price) VALUES (%s, %s, %s, %s) """

record_list = [('1','Tomato','20','5'),
               ('2','Whiskas','30','6'),
               ('3','CocaCola','50','6'),
               ('4','Kitkat','80','3'),
               ('5','Egg','25','20')]

retailer_insert_query = """INSERT INTO retailer (name,phone,address) VALUES (%s, %s, %s) """

retailer_list = [('Coca Cola','202-555-0174 ','4258 Benson Park Drive'),
               ('Amazon','202-555-0191','2964 Randall Drive'),
               ('Walmart','202-555-0162','2457 Jerry Toth Drive'),
               ('Costco','202-555-0190','1891 Timbercrest Road'),
               ('Starbucks','202-555-0178','75 Winding Way')]

user_insert_query = """INSERT INTO user (name,surname,marketname,phone,email,password) VALUES (%s, %s, %s, %s, %s, %s) """

user_list = [('Berk','A','market1','212-555-0130','test1@gmail.com','123'),
               ('Bedirhan','G','market2','252-154-1151','test2@gmail.com','123')]

try:
    cursor.executemany(product_insert_query, product_list)
    cnx.commit()
    print(cursor.rowcount, "Product list inserted successfully into Product table")

    cursor.executemany(record_insert_query, record_list)
    cnx.commit()
    print(cursor.rowcount, "Record list inserted successfully into Record table")

    cursor.executemany(retailer_insert_query, retailer_list)
    cnx.commit()
    print(cursor.rowcount, "Retailer list inserted successfully into Retailer table")

    cursor.executemany(user_insert_query, user_list)
    cnx.commit()
    print(cursor.rowcount, "User list inserted successfully into User table")
except Exception as error:
    print(error)



cnx.close()