import os
import psycopg2

class Db_connection:
    CONNECTION = None

    def __init__(self):
         if Db_connection.CONNECTION is None :
            try:
                Db_connection.CONNECTION = psycopg2.connect(
                    host="localhost",
                    database="AGOGO",
                    user="postgres",
                    password="postgres")
                print('connecting')
            except Exception as error:
                print("Error: Connection not established {}".format(error))
            else:
                print("Connection established")

    @staticmethod   
    def closeConnection(conn):
            conn.close();

    @staticmethod
    def getConnection():
         if Db_connection.CONNECTION is None:
            Db_connection();
            return Db_connection.CONNECTION
    
         return Db_connection.CONNECTION

    @staticmethod
    def commit():
        Db_connection.CONNECTION.commit();

# Open a cursor to perform database operations
# cur = conn.cursor()

# cur.close()
# conn.close()
# # Execute a command: this creates a new table
# cur.execute('DROP TABLE IF EXISTS books;')
# cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
#                                  'title varchar (150) NOT NULL,'
#                                  'author varchar (50) NOT NULL,'
#                                  'pages_num integer NOT NULL,'
#                                  'review text,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP);'
#                                  )

# Insert data into the table

# cur.execute('INSERT INTO books (title, author, pages_num, review)'
#             'VALUES (%s, %s, %s, %s)',
#             ('A Tale of Two Cities',
#              'Charles Dickens',
#              489,
#              'A great classic!')
#             )
# cur.execute('INSERT INTO books (title, author, pages_num, review)'
#             'VALUES (%s, %s, %s, %s)',
#             ('Anna Karenina',
#              'Leo Tolstoy',
#              864,
#              'Another great classic!')
#             )
# conn.commit()



    # @staticmethod
    # def getConnection():
    #      __conn = psycopg2.connect(
    #             host="localhost",
    #             database="AGOGO",
    #             user="postgres",
    #             password="postgres")
    #     print('connecting')
    #     return __conn