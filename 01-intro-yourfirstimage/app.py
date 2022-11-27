import subprocess
import os
import requests

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
   req_path = request.path

   try:
       answer = subprocess.check_output("cat /data/"+req_path+"/greeting.txt", shell=True)
       return answer.decode('utf-8').strip()+" - From "+os.getenv('GREETER')
   except ValueError:
       return 'Oops! Invalid. Try again...'

