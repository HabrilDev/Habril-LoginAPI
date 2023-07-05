import mysql.connector


connection = mysql.connector.connect(host='ip',
                                     database='db',
                                     user='uname',
                                     password='pwd')

sql_select_Query = "select Username from LoginSystem"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()
print("Total number of rows in table: ", cursor.rowcount)
print("\nPrinting each row")
for row in records:
    if row[0] == "habril":
        print("yes")


if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

