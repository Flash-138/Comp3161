from flask import Flask, request, make_response, jsonify
import mysql.connector
from mysql.connector import Error
import json
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required,get_jwt_identity, get_jwt)
from datetime import timedelta

with open('Configs\\db_config.json', 'r') as f:
    db_config = json.load(f)


app = Flask(__name__)

def assign_role(user_id):
    if user_id//10000000 == 62 and user_id >= 620000000 and user_id < 630000000:
        return 3
    elif user_id//10000 == 100 and user_id >= 1000000 and user_id <= 1009999:
        return 2 
    elif user_id//100000 == 999 and user_id >= 99900000 and user_id <= 99999999:
        return 1
    else:
        raise ValueError
    
    
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
        Password = content["password"]

        Role = assign_role(User_id)
        cursor.execute("INSERT INTO User(user_id,role) VALUES(%s,%s,%s,%s)",(User_id,Role))
        cursor.execute("INSERT INTO Logins(user_id,user_password) VALUES(%s,%s)" , (User_id,Password))
        
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(f"User {User_id} was sucessfully created", 200)
    except ValueError:
        return make_response(f"Invalid user id", 410)
    except mysql.connector.Error as err:
        return make_response({"error": str(err)}, 405)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
    



@app.route('/User_login', methods=['Post'])
def User_login():

    try:
        cnx = mysql.connector.connect(user=db_config["user"], 
                                      password= db_config["password"],
                                      host= db_config["host"],
                                      database= db_config["database"]
                                      )
        cursor = cnx.cursor()
        content = request.json

        User_id = int(content['user_id'])
        Password = content["password"]

        cursor.execute("Select * from Logins where (user_id) = (%s)",(User_id,))
        user = cursor.fetchone()

        cnx.commit()
        cursor.close()
        cnx.close()

        if user is None:
            return make_response(f"Incorrect User ID/Password", 404)
        
        if user[1] == Password:
            return make_response(f"User {User_id} was logged in", 200)
        else:
            return make_response(f"Incorrect User ID/Password", 404)

    except mysql.connector.Error as err:
        return make_response({"error": str(err)}, 405)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/Create_Course', methods=['Post'])
def Create_Course():
    try:
        cnx = mysql.connector.connect(user=db_config["user"], 
                                      password= db_config["password"],
                                      host= db_config["host"],
                                      database= db_config["database"]
                                      )
        cursor = cnx.cursor()
        content = request.json

        User_id = int(content['user_id'])
        course_id = int(content['course_id'])
        course_name = content['course_name']
        course_code = content["course_code"]


        cursor.execute("Select Role from User where (user_id) = (%s)",(User_id,))
        Role = cursor.fetchone()

        if Role is None:
            return make_response(f"Invalid User ID", 404)
        
        elif Role[0] == "admin" or Role[0] == 1:
            cursor.execute("Select course_id,course_code from Course where (course_id) = (%s)",(course_id,))
            course_exist = cursor.fetchone()
            
            if course_exist is None:
                cursor.execute("INSERT INTO Course(course_id,course_name,course_code) VALUES(%s,%s,%s)" , (course_id,course_name,course_code))

            else:
                return make_response(f'The Course {course_exist[1]} is already assigned to {course_exist[0]}', 450)
            
        else:
            raise PermissionError
        
        cnx.commit()
        cursor.close()
        cnx.close()

        
    
        return make_response(f"Course {course_code} was created", 200)


    except mysql.connector.Error as err:
        return make_response({"error": str(err)}, 405)
    except PermissionError as e:
        return make_response('You dont have permission to create a Course', 410)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/View_Courses', methods=['Get'])
def View_Courses():

    pass

@app.route('/View_Courses/<User_id>', methods=['Get'])
def View_Courses_id(User_id):

    content = request.json
    
    if ex.Stud_id_check(User_id):
        return ex.View_Courses_by_Student(User_id)
    
    elif ex.Lec_id_check(User_id):
        return  ex.View_Courses_by_Lecturer(User_id)




if __name__ == '__main__':
    app.run(port=10000)
