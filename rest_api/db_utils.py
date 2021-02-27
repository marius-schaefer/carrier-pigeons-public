import sqlite3


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
    c.execute("""CREATE TABLE user (
            user_id text,
            queue_id text,
    )""")
    
    conn.commit()
    conn.close()


def create_queue_table():
    #creates or connects to an existing db
    conn = sqlite3.connect('viqueue.db')
    #creates cursor
    c = conn.cursor()

    #creates queue table
    c.execute("""CREATE TABLE queue (
            queue_id text,
            name text,
            tickets text,
            curr_ticket,
            max_occupancy,
            curr_occupancy,
    )""")
    
    conn.commit()
    conn.close()