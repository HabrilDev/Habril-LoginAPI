import mysql.connector
from cryptography.fernet import Fernet

def load_key():
    return open("secret.key", "rb").read()

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    print(decrypted_message.decode())

connection = mysql.connector.connect(host='ip',
                                     database='db',
                                     user='uname',
                                     password='pwd')

sql_select_Query = "select Password from LoginSystem where Username = 'ting'"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()
records = records[0][0].encode()

print(records)
print(decrypt_message(records))


if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

