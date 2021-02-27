from flask import Flask
from flask_restful import Api, Resource
from db_utils import *


#Initializing the DB, if this is the first time the main.py has been run

user_table_exist = check_for_table('user')
if not user_table_exist:
    create_user_table()

queue_table_exist = check_for_table('queue')
if not queue_table_exist:
    create_queue_table()

ticket_table_exist = check_for_table('ticket')
if not ticket_table_exist:
    create_ticket_table()


#API:
app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, user_id):
        data = get_user(user_id)
        user_id = data[0]
        queue_id = data[1]

        return {"user_id" : user_id, "queue_id" : queue_id}

    def put(self, user_id):
        if check_for_user(user_id):
            create_user(user_id)

            data = get_user(user_id)
            user_id = data[0]
            queue_id = data[1]

            return {"user_id" : user_id, "queue_id" : queue_id}
        else:
            return "User Already Exists"

    def delete(self, user_id):
        delete_user(user_id):
        
        return f"{user_id} deleted"

#Adding Resources:
api.add_resource(User, "/user/<string:user_id>" )



#Runs the Flask App
if __name__ == "__main__":
    #note to self remove the debug when done developing
    app.run(debug=True)