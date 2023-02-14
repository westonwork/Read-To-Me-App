#the code that runs by default when anyone access this package 
#add global variables to the __init__

from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhh"

DATABASE = "read_to_yourself_python_project_schema" 