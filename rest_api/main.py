from flask import Flask, request, redirect
from flask_restful import Api, Resource, reqparse
from db_utils import *
from flask_cors import CORS

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
CORS(app)
api = Api(app)




#User API:
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
        
        return f"user {user_id} deleted"


#Queue Argument Parsing:
queue_put_args = reqparse.RequestParser()
queue_put_args.add_argument("max_occupancy", type=int, help="The max_occupancy value (interger) is required")
queue_put_args.add_argument("user_id", type=str, help="The User who owns this queue")


#Queue API:
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
        data = queue_put_args.parse_args()
        delete_queue(name, data)
        return f"queue {name} deleted"


#Ticket Argument Parsing:
ticket_args = reqparse.RequestParser()
ticket_args.add_argument("ticket_id", type=str, help="ticket_id : (string)")
ticket_args.add_argument("queue_id", type=int, help="queue_id : (interger)")
ticket_args.add_argument("phone_number", type=str, help="phone_number : str")

ticket_delete_args = reqparse.RequestParser()
ticket_delete_args.add_argument("ticket_id", type=str, help="ticket_id : (string)")


#Ticket API:
class Ticket(Resource):
    def get(self):
        args = ticket_args.parse_args()
        ticket_id = args['ticket_id']
        data = get_ticket_data(ticket_id)
        return data

    def post(self):
        args = ticket_args.parse_args()
        queue_id = args['queue_id']
        phone_number = args['phone_number']
        ticket_id = create_ticket(queue_id, phone_number)
        data = get_ticket_data(ticket_id)
        return data


class Ticket_Delete(Resource):
    def get(self):
        args = ticket_delete_args.parse_args()
        ticket_id = args['ticket_id']
        delete_ticket(ticket_id)
        return f"{ticket_id} deleted"


ticket_action_args = reqparse.RequestParser()
ticket_action_args.add_argument("queue_id", type=int, help="queue_id : int")
ticket_action_args.add_argument("ticket_id", type=str, help="ticket_id : str")

class Ticket_Actions(Resource):
    #Entry
    def get(self):
        args = ticket_args.parse_args()
        queue_id = args['queue_id']
        ticket_entered(queue_id)
        occupancy = get_store_occupancy(queue_id)

        return {"curr_occupancy" : occupancy}


    
    #Get Queue_position
    def post(self):
        args = ticket_args.parse_args()
        ticket_id = args['ticket_id']
        index = get_queue_position(ticket_id)
        
        return index


class Occupancy(Resource):
    #Get Store Occupation
    def get(self, queue_id):
        occupancy = get_store_occupancy(queue_id)
        return occupancy
    #Get Queue Length
    def post(self, queue_id):
        length = get_queue_length(queue_id)
        return length

class Notif(Resource):
    #Exit
    def delete(self, queue_id):
        occupant_left_store(queue_id)
        occupancy = get_store_occupancy(queue_id)

        return {"curr_occupancy" : occupancy}


#Adding Resources:
api.add_resource(User, "/user/<string:user_id>")
api.add_resource(Queue, "/queue/<string:name>")
api.add_resource(Ticket, "/ticket")
api.add_resource(Ticket_Delete, "/ticket-delete")
api.add_resource(Ticket_Actions, "/ticket-actions")
api.add_resource(Occupancy, "/occupancy/<int:queue_id>")
api.add_resource(Notif, "/notif/<int:queue_id>")

#Runs the Flask App
if __name__ == "__main__":
    #note to self remove the debug when done developing
    app.run(debug=True)