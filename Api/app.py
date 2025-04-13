from flask import Flask, request, make_response, jsonify
from helper.py import assign_role
import mysql.connector
import json
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required,get_jwt_identity, get_jwt)
from datetime import timedelta

with open('Configs\db_config.json', 'r') as f:
    db_config = json.load(f)


app = Flask(__name__)

    
@app.route('/', methods=['GET'])
def hello_world():
    return "hello world"


@app.route('/register_user', methods=['Post'])
def register_user():
    try:
        cnx = mysql.connector.connect(user=db_config["user"], 
                                      password= db_config["password"],
                                      host= db_config["host"],
                                      database= db_config["database"]
                                      )
        cursor = cnx.cursor()
        content = request.json

        User_id = int(content['user_id'])
        Name = content["name"]
        Email = content["email"]
        Password = content["password"]

        Role = assign_role(User_id)

        cursor.execute(f"INSERT INTO User(user_id,name,email,password,role) VALUES({User_id},'{Name}',{Email},{Password},{Role})")
        
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(f"User {User_id} was sucessfully created", 200)
    except ValueError:
        return make_response(f"Invalid user id", 400)
    except Exception as e:
        return make_response({'error': str(e)}, 400)



@app.route('/User_login', methods=['Get'])
def User_login():

    content = request.json
    User_id = content['User_ID']
    print(User_id,content['Password'])

    if ex.Stud_id_check(User_id):
        return ("Student")
    
    elif ex.Lec_id_check(User_id):
        return ("Lecturer")
    
    elif ex.Admin_id_check(User_id):
        return ("Admin")
    
    else:
        return "Invalid User ID"

"""The body for the request is 
{
    "User_id": "620123456",
    "Course_Name" : "#####",
}
"""
#This function allows a user to login into one of three login pages based on the user id type.

@app.route('/Create_Course', methods=['Post'])
def Create_Course():

    content = request.json
    User_id = content['User_ID']
    print(User_id,content['Password'])
    
    
    if ex.Admin_id_check(User_id):
        return ("Admin")
    
    else:
        return "Invalid User type"

@app.route('/View_Courses', methods=['Get'])
def View_Courses():

    pass

@app.route('/View_Courses/<User_id>', methods=['Get'])
def View_Courses(User_id):

    content = request.json
    
    if ex.Stud_id_check(User_id):
        return ex.View_Courses_by_Student(User_id)
    
    elif ex.Lec_id_check(User_id):
        return  ex.View_Courses_by_Lecturer(User_id)




if __name__ == '__main__':
    app.run(port=10000)
