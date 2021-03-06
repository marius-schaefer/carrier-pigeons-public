import sqlite3
import random
import datetime
from twilio.rest import Client
import os

#Twilio Stuff:
account_sid = 'AC7079bc83fc92aa1df930909ad5c7a298'
auth_token = '8402668beb64cc9726cad329f1d3983f'
client = Client(account_sid, auth_token)

#DB Initialization Functions:
def check_for_table(table_name):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    #gets the count of tables with table_name:
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name= ? ''', (table_name,))
    if c.fetchone()[0]==1 :
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False


def create_user_table():
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    #creates user table
    c.execute("""CREATE TABLE user (user_id text, queue_id interger)""")
    
    conn.commit()
    conn.close()


def create_queue_table():
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    #creates queue table
    c.execute("""CREATE TABLE queue (queue_id interger, name text, ticket_prefix text, curr_ticket interger, max_occupancy interger, curr_occupancy interger)""")
    
    conn.commit()
    conn.close()


def create_ticket_table():
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    #creates ticket table
    c.execute("""CREATE TABLE ticket (ticket_id text, queue_id interger, ticket_number interger, date_created text, date_enetered text, phone_number text)""")
    
    conn.commit()
    conn.close()



#User Table Functions:
def get_user(user_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))

    data = c.fetchall()

    conn.commit()
    conn.close()

    return data


def create_user(user_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("INSERT INTO user VALUES (?, 0)", (user_id,))

    conn.commit()
    conn.close()


def delete_user(user_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("DELETE from user WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

def check_for_user(user_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM user")

    data = c.fetchall()

    if user_id in data:
        return False
    else:
        return True



#Queue Table Functions
def generate_queue_id():
    while True:
        queue_id = random.randrange(0,99999)
        
        #Checks if Queue id already exists:
        #creates or connects to an existing db
        conn = sqlite3.connect('viqueue.db')
        #creates cursor
        c = conn.cursor()

        c.execute("SELECT * FROM queue WHERE queue_id = ?", (queue_id,))

        data = c.fetchall()

        if queue_id in data:
            pass
        else:
            break
    
    #Returns queue_id if the queue_id does not exist yet:
    return queue_id


def create_queue(data, name):
    generated_queue_id = generate_queue_id()
    num = 0

    queue_id = generated_queue_id
    ticket_prefix = f"{generated_queue_id}-"
    ticket_init = 0
    max_occupancy = data['max_occupancy']
    user_id = data['user_id']
    
    
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("INSERT INTO queue VALUES (?, ?, ?, ?, ?, 0)", (queue_id, name, ticket_prefix, ticket_init, max_occupancy))
    c.execute("UPDATE user SET queue_id = ? WHERE user_id = ?", (queue_id, user_id))

    conn.commit()
    conn.close()


def get_queue_data(name):    
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM queue WHERE name = ?", (name,))

    data = c.fetchall()

    json_formatted_data = {
        'queue_id' : data[0][0],
        'name' : data[0][1],
        'ticket_prefix' : data[0][2],
        'curr_ticket' : data[0][3],
        'max_occupancy' : data[0][4],
        'curr_occupancy' : data[0][5]
    }

    return_data = {name : json_formatted_data}

    return return_data


def check_queue_name(name):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM queue WHERE name = ?", (name,))

    data = c.fetchall()

    if name in data:
        return False
    else:
        return True


def delete_queue(name, data):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    user_id = data['user_id']

    c.execute("UPDATE user SET queue_id = 0 WHERE user_id = ?", (user_id,))
    c.execute("DELETE from queue WHERE name = ?", (name,))

    conn.commit()
    conn.close()



#Ticket Table Funcitons:
def get_ticket_data(ticket_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM ticket WHERE ticket_id = ?", (ticket_id,))

    data = c.fetchall()

    conn.commit()
    conn.close()

    json_formatted_data = {
        'ticket_id' : data[0][0],
        'queue_id' : data[0][1],
        'ticket_number' : data[0][2],
        'date_created' : data[0][3],
        'date_entered' : data[0][4],
        'phone_number' : data[0][5]
    }

    return_data = {ticket_id : json_formatted_data}

    return json_formatted_data


def create_ticket(queue_id, phone_number):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM queue WHERE queue_id = ?", (queue_id,))
    data = c.fetchall()
    curr_ticket = data[0][3]
    ticket_prefix = data[0][2]
    new_ticket_number = curr_ticket + 1

    conn.commit()
    conn.close()

    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    #new data to insert:
    ticket_id = f"{ticket_prefix}"+ f"{new_ticket_number}" 
    ticket_number = new_ticket_number
    date_created = datetime.datetime.now()

    c.execute("INSERT INTO ticket VALUES (?, ?, ?, ?, 'None', ?)", (ticket_id, queue_id, ticket_number, date_created, phone_number))
    c.execute("UPDATE queue SET curr_ticket = ? WHERE queue_id = ?", (new_ticket_number, queue_id))
    conn.commit()
    conn.close()

    return ticket_id


def delete_ticket(ticket_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("DELETE from ticket WHERE ticket_id = ?", (ticket_id,))

    conn.commit()
    conn.close()


def ticket_entered(queue_id):
    #Deletes upon entry
    
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM ticket WHERE queue_id =? ORDER BY ticket_number ASC", (queue_id,))
    tickets = c.fetchall()
    ticket_number = tickets[0][2]

    c.execute("SELECT * FROM queue WHERE queue_id = ?", (queue_id,))
    queue_data = c.fetchall()
    curr_occupancy = queue_data[0][5]
    new_occupancy = curr_occupancy + 1

    c.execute("UPDATE queue SET curr_occupancy = ? WHERE queue_id = ?", (new_occupancy, queue_id))
    c.execute("DELETE from ticket WHERE ticket_number = ?", (ticket_number,))

    conn.commit()
    conn.close()


def occupant_left_store(queue_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM queue WHERE queue_id = ?", (queue_id,))
    queue_data = c.fetchall()
    curr_occupancy = queue_data[0][5]
    if curr_occupancy == 0:
        pass
    else:
        new_occupancy = curr_occupancy - 1

    c.execute("UPDATE queue SET curr_occupancy = ? WHERE queue_id = ?", (new_occupancy, queue_id))

    conn.commit()
    conn.close()

    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM ticket WHERE queue_id = ? ORDER BY ticket_number ASC", (queue_id,))
    data = c.fetchall()
    phone_number =  data[0][5]

    message = client.messages.create(
        to='+19174854589',
        from_='+18177998317',
        body = 'Hello, you may now enter the store!'
    )
    print(message.sid)



def get_queue_position(ticket_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM ticket WHERE ticket_id = ?", (ticket_id,))

    data = c.fetchall()
    queue_id = data[0][1]
    ticket_number = data[0][2]

    conn.commit()
    conn.close()

    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM ticket WHERE queue_id =? ORDER BY ticket_number ASC", (queue_id,))
    tickets = c.fetchall()
    first_ticket = tickets[0][2] 
    index = ticket_number - first_ticket + 1 

    return index


def get_queue_length(queue_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM ticket WHERE queue_id =?", (queue_id,))
    tickets = c.fetchall()
    queue_length = len(tickets)
    return queue_length


def get_store_occupancy(queue_id):
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM queue WHERE queue_id =?", (queue_id,))
    queue = c.fetchall()

    return queue[0][5]


def get_numbers():
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    c.execute("SELECT * FROM queue")

    queues = c.fetchall()

    numbers = []

    for queue in queues:
        max_occup = queue[4]
        curr_occup = queue[5]
        occup = max_occup - curr_occup

        if occup >=1:
            c.execute("SELECT * FROM ticket WHERE queue_id = ? LIMIT ? ORDER BY ASC", (queue[0], occup))
            tickets = c.fetchall()
            for ticket in tickets:
                numbers.append(ticket[5])
        else:
            pass

        return numbers