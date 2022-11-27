import subprocess
import os
import requests

from flask import Flask
from flask import request
from flask_httpauth import HTTPBasicAuth
from flask_mysqldb import MySQL

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@auth.verify_password
def verify_password(username, password):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user FROM users where user='"+username+"' and password='"+password+"'")
    userresult = cursor.fetchall()
    cursor.close
    for x in userresult:
      return x;

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@auth.login_required
def hello_world(path):
   req_path = request.path

   try:
       answer = subprocess.check_output("cat /data/"+req_path+"/greeting.txt", shell=True)
       return answer.decode('utf-8').strip()+" - To "+format(auth.username())+" - From "+os.getenv('GREETER')
   except ValueError:
       return 'Oops! Invalid. Try again...'

