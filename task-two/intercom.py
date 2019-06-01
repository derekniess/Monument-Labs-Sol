
import requests
import pymysql


url = "https://api.intercom.io/users"
key = "insert_key"

# database credentials
hostname = "hostname"
username = "username"
password = "password"
database = "database name"

headers = {
    'Authorization': key,
    'Accept': "application/json",
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }

# establish connection with our user database
connection = pymysql.connect(host = hostname, user = username, passwd = password, db = database)

# create database cursor
cursor = connection.cursor()

try:
	# execute SQL command
	cursor.execute("select name, email from user")
	# get all rows in our user database
	data = cursor.fetchall()
except:
	print("Error: unable to fetch data")

# create an account on Intercom for each user
try :
	for record in data:
		name = record[0]
		email = record[1]
		payload = "{\n  \"email\": \""+email+"\",\n  \"name\": \""+name+"\"\n}"
		response = requests.request("POST", url, data=payload, headers=headers)
		response.raise_for_status()
except requests.exceptions.RequestException as err:
	print("Error creating Intercom accounts:")
	print(err)

cursor.close()
connection.close()


