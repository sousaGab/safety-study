# Python 3 server
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from os import name, putenv
import pymysql
import json
import hashlib
import bcrypt


# open connection to database
db = pymysql.connect(
                    host="localhost",
                    user='#DB_USER', 
                    password='#DB_PASSWORD',
                    database='#DB_NAME')

# prepare a cursor object using cursor() method
cursor = db.cursor()

def get_user(username) :
    querySelect = ''
    # prepare SQL query to INSERT a record into the database.
    querySelect = "SELECT * FROM users \
            WHERE username ='%s'" % username
        
    print('querySelected', querySelect)
    user = {}

    try:
        cursor.execute(querySelect)
        # fetch all the rows in a list of lists.
        USER_DB = cursor.fetchall()
        user = USER_DB[0]

    except:
        print("Error: unable to fetch data")
    
    if user :
        return {
            'id': user[0],
            'username':user[1],
            'password': user[2]
        }
    else :
        return user       


def insert_in_db(username, password) : 
    
    queryInsert = ''
    queryInsert = "INSERT INTO users ("
    queryInsert += "`username`, `password`"
    queryInsert += ") VALUES ("
    
    queryInsert += "'" + username + "'"
    queryInsert += ", "
    queryInsert += "'" + password + "'"
    queryInsert += ");"

    try:
        # Execute the SQL command
        cursor.execute(queryInsert)
        # Commit your changes in the database
        db.commit()
        print("Successfuly inserted")
        
        return True
    except:
        # Rollback in case there is any error
        print("Insert Error")
        db.rollback()
        return False

def create_user(username,password, type) :
    
    if type == 'clear':
        return insert_in_db(username, password)
    
    elif type == 'hash':
        
        password_hashed = hashlib.md5(password.encode())
        print('The byte equivalent of hash is: ', password_hashed.hexdigest())
        
        return insert_in_db(username, str(password_hashed.hexdigest()))
    
    elif type == 'hash+salt':
        
        password_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print('The byte equivalent of hash is: ', password_hashed.decode("utf-8"))

        return insert_in_db(username, password_hashed.decode("utf-8"))


def authenticate_user(username, password, type):
    
    user = get_user(username)
    
    if user :

        if type == 'clear':     
            if user['username'] == username and user['password'] == password :
                return True

        elif type == 'hash':
            password_hashed = hashlib.md5(password.encode()).hexdigest()

            if user['username'] == username and password_hashed == user['password'] :
                return True

        elif type == 'hash+salt':
            password_match = bcrypt.hashpw(password.encode(), user['password'].encode()) == user['password'].encode()
           
            if user['username'] == username and password_match:
                return True
    
    return False

class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'login.html'
            return SimpleHTTPRequestHandler.do_GET(self)

        if self.path == '/create/':
            self.path = 'create.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/':
            js_data = self.rfile.read(int(self.headers.get('Content-Length'))).decode()
            data = json.loads(js_data)
            if authenticate_user(data['username'], data['password'], data['type']):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'LOGGED IN\n')
                return
        
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'ERROR\n')

        if self.path == '/create/':
            js_data = self.rfile.read(int(self.headers.get('Content-Length'))).decode()
            data = json.loads(js_data)
            if create_user(data['username'],data['password'], data['type']) :
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'CREATED USER\n')
                return

            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'ERROR\n')


def main():
    PORT = 8080
    server = HTTPServer(('', PORT), MyHttpRequestHandler)
    print('Server running on port', PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()
