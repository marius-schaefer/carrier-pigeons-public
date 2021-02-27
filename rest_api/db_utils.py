import sqlite3


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
    c.execute("""CREATE TABLE user (user_id text, queue_id text)""")
    
    conn.commit()
    conn.close()


def create_queue_table():
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    #creates queue table
    c.execute("""CREATE TABLE queue (queue_id text, name text, tickets text, curr_ticket text, max_occupancy interger, curr_occupancy interger)""")
    
    conn.commit()
    conn.close()


def create_ticket_table():
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    #creates ticket table
    c.execute("""CREATE TABLE ticket (ticket_id text, number interger, date_created text, date_enetered text, phone_number text)""")
    
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

    c.execute("INSERT INTO user VALUES (?, 'None')", (user_id,))

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