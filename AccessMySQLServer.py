#Import Required modules
import base64
from sshtunnel import SSHTunnelForwarder
import pymysql

#Password encryption/decryption for accessing Database server
#EncodedServerPass = base64.b64encode("ServerPass".encode("utf-8"))
#EncodedMySQLPass = base64.b64encode("MySQLPass".encode("utf-8"))
with open("EncodedPasswords.txt", "r") as filestream:
    for line in filestream:
            EncServerPass, EncMySQLPass = line.split(",")


ServerPass = base64.b64decode(EncServerPass)
MySQLPass = base64.b64decode(EncMySQLPass)

# Initializing required variables
ServerAdress = '66.76.242.194'
ServerUserName = 'ambekarakhil'
MySQLUserName = 'ambekarakhil'
DatabaseName = 'ambekarakhil'

# SSH linux server
server = SSHTunnelForwarder(
    ServerAdress,
    ssh_username= ServerUserName,
    ssh_password= ServerPass,
    remote_bind_address=('127.0.0.1', 3306)
)
server.start()

#Make a database connection
cnx = pymysql.connect(
    host='127.0.0.1',
    port=server.local_bind_port,
    user= MySQLUserName,
    password= MySQLPass,
    db= DatabaseName
)

print("Connected to the following MySQL Server: " + cnx.get_server_info())

#Execute SQL Commands
with cnx.cursor() as cur:
    
    cur.execute('use ambekarakhil;')
    cur.execute('Select * from verus0302c;')
    rows = cur.fetchall()
    for row in rows:
        print(f'{row[0]} {row[1]} {row[2]}')


# Close all connections
cnx.close()
server.stop()
