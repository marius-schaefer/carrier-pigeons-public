from flask import Flask
from flask_restful import Api, Resource, reqparse
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
        user_id = data[0][0]
        queue_id = data[0][1]

        return {"user_id" : user_id, "queue_id" : queue_id}

    def put(self, user_id):
        if check_for_user(user_id) == True:
            create_user(user_id)

            data = get_user(user_id)
            user_id = data[0][0]
            queue_id = data[0][1]

            return {"user_id" : user_id, "queue_id" : queue_id}
        else:
            return "User Already Exists"

    def delete(self, user_id):
        delete_user(user_id)
        
        return f"{user_id} deleted"


#Queue Argument Parsing:
queue_put_args = reqparse.RequestParser()
queue_put_args.add_argument("max_occupancy", type=int, help="The max_occupancy value (interger) is required", required=True)


class Queue(Resource):
    def get(self, name):
        data = get_queue_data(name)
        return data

    def put(self, name):
        if check_queue_name(name):
            data = queue_put_args.parse_args()
            create_queue(data, name)
            data = get_queue_data(name)
            
            return data
        else:
            return "Queue Name Already Exists"

    def delete(self, name):
        delete_queue(name)
        return f"{name} deleted"


#Adding Resources:
api.add_resource(User, "/user/<string:user_id>")
api.add_resource(Queue, "/queue/<string:name>")



#Runs the Flask App
if __name__ == "__main__":
    #note to self remove the debug when done developing
    app.run(debug=True)