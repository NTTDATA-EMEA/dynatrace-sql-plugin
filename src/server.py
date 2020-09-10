import connexion
import job
import auth
from flask import render_template
#from flask_httpauth import HTTPTokenAuth
from scheduler import Scheduler
import config
from mongodb import MongoDB

from connexion.exceptions import OAuthProblem

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yaml')

mDB = MongoDB()



# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return "Hello World"

x = Scheduler()
x.startEngine()
x.addDTAPI()
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT, debug=True)