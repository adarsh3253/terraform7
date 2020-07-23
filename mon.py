
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property


from flask import Flask ,jsonify, request, make_response,json
from flask_restx import Api, Resource, fields
from flask_pymongo import PyMongo
from bson.json_util import dumps
import string
from random import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)


api = Api(app, version='1.0', title='Candidate Details API',
    description='A simple login API',
  
     
)
jwt = JWTManager(app)


app.config['MONGO_URI'] = ('mongodb+srv://admin:admin@dev-bcone-blackhack-q7ws7.mongodb.net/blackhack?retryWrites=true&w=majority')
app.config['JWT_SECRET_KEY'] = 'secret'

model = api.model('User', {'name' : fields.String('name') , 'email_id' : fields.String('email_id'),'dateofbirth' : fields.String('dateofbirth'),
'phoneno' : fields.String('phoneno'), 'location' : fields.String('location')  }) 

mongo = PyMongo(app)

model_login = api.model('login',{'username' : fields.String('username'), 'password' : fields.String('password') })

@api.route('/all')
class getdata(Resource):

   
    def get(self):

        user = mongo.db.Candidate.find()
        resp = dumps(user)
        return resp        
        
@api.route('/registration')
class postdata(Resource):
    @api.expect(model)
    def post(self):
        json = request.json
        name = json['name']
        email_id = json['email_id']
        dateofbirth = json['dateofbirth']
        phoneno = json['phoneno']
        location = json['location']
        
        if name and email_id  and dateofbirth and phoneno and  location and request.method == 'POST':
            new_user = mongo.db.Candidate.insert_one({'name': name, 'email_id': email_id,
              'dateofbirth': dateofbirth,
             'phoneno': phoneno, 'location': location, '_loginid' :str(self.login(name))  })
            

            resp = jsonify("user added successfully")
            resp.status_code = 200

       
        return resp
        
    def login(self,name):
        characters = string.ascii_letters + string.digits 
        password = "".join(choice(characters) for x in range(randint(8,16)))
       
     
        user_name =  name[0:6]
        import random
        numb = '{}'.format(random.randint(1000, 9999))
       
        username = ''.join(user_name+numb) 
       
       
        inserting_Username_password = mongo.db.credentials.insert_one({'username': username, 'password': password})
        return inserting_Username_password.inserted_id

@api.route('/1user/<string:name>')
class getdataone(Resource):
    def get(self,name):
            resp = {}
            user_name = mongo.db.Candidate.find({'name' : name}, {'_id':0})
            for data in user_name:
                resp.update(response= data)
            return resp
   
@api.route('/user_Login')
class logindata(Resource):
    @api.expect(model_login)
    def post(self):
        credentials = mongo.db.credentials
        username = request.get_json()['username']
        password = request.get_json()['password']
        result = ""

        response = credentials.find_one({'username': username , 'password': password})
     
        if response:
            
            if (response['password'], password):
                access_token = create_access_token(identity = {
                'username': response['username'],
                'password': response['password'],
                
               
            })

            
            result = jsonify({'token':access_token})
        else:
            result = jsonify({"error":"Invalid username and password"})

        return result 

@api.route('/credentials ')
class getcredentilas(Resource):

   
    def get(self):
        users = mongo.db.credentials.find()
        resp = dumps(users)
        return resp           

@api.route('/delete/<string:name>')
class deletedata(Resource):
    def delete(self,name):
        mongo.db.Candidate.find_one_and_delete({'name' : name})
        resp = jsonify("user deleted succesfully")

        resp.status_code = 200
        return resp
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'not found' + request.url
    }

    resp = jsonify(message)

    resp.status_code = 404

      
if __name__ == '__main__':
    app.run(debug=True)