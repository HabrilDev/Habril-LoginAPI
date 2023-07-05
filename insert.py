import mysql.connector


def insert_varibles_into_table(rollNo, name, address, city):
    connection = mysql.connector.connect(host='cryotec.boldmoon.in',
                                         database='db',
                                         user='uname',
                                         password='pwd')
    cursor = connection.cursor()
    mySql_insert_query = """INSERT INTO LoginSystem (UserID, Username, Password, Name) 
                            VALUES (%s, %s, %s, %s) """

    record = (rollNo, name, address, city)
    cursor.execute(mySql_insert_query, record)
    connection.commit()
    print("Record inserted successfully into Pytest table")
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


insert_varibles_into_table(3, 'ting', 'gAAAAABiiOaW1K0ZQVCUBgTz434w4rlkAh-f2hHJfLSATkOY-y5HAgoveGnelfpCgUXKkcYBa8XmRK-Af677UeVZa18DfCqRxQ==', 'Tong')
