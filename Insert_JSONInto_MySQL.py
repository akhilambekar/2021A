#Import required modules
import requests
import json
import base64
from sshtunnel import SSHTunnelForwarder
import pymysql
from pymysql.converters import escape_string


# Get json results for the required input 

InputString = "kobe is a basketball player"

headers = {
    'Content-type': 'application/json',
}

data = '{"text":InputString = '+ InputString + '}'

response = requests.post('http://66.76.242.198:9888/', data=data).json()


#print(json.dumps(response, indent=4, sort_keys=True))

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
    db = DatabaseName
)

print("Connected to the following MySQL Server: " + cnx.get_server_info())

# Add escape string (\\") for double quotes present in the json data, removes any conflict with insert statement
json_data = json.dumps(response)

CountVal = 3
TeacherVal = "dummyTeacher"
AssertionVal= "dummyAssertion"
LinkageVal = "dummyLinkage"

#Execute SQL Commands
with cnx.cursor() as cur:
    
    cur.execute('use ambekarakhil;')
    sql_command = """INSERT INTO verus0302c(count, teacher, assertion, nlp, linkages) VALUES (%s, %s, %s, %s, %s)""" 
    cur.execute(sql_command, (CountVal, TeacherVal, AssertionVal, json_data, LinkageVal))

cnx.commit()

"""
#Retrieve data from MySQL
with cnx.cursor() as cur:
    
    cur.execute('use ambekarakhil;')
    cur.execute('Select * from verus0302c;')
    rows = cur.fetchall()
    for row in rows:
        print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}')
"""

# Close all connections
cnx.close()
server.stop()

