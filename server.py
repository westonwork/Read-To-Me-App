from flask_app import app 
from flask_app.controllers import user_controller
#import the routes..aka all the controllers

if __name__=="__main__":
        app.run(debug=True)