# API Documentation
This is a rest api, the link is: https://99bac19acf0e.ngrok.io/
## Class User:
User is a store owner
### What data does User contain?:
User contains a user_id (string) and a queue_id
When a user is first created they do not have a queue_id, they have to create a queue first

### How to use User:
*All user requests are sent to base_url/user/(user_id)*
#### Put Request to base_url/user/(user_id)  CREATES A USER IN THE DB:
A put request to this url will create a User in the DB and return the current data on that user. It is required that you provide the user_id as a variable during the request
as can be seen in the request url. The User_id must also be unique.
#### Get Request to base_url/user/(user_id) GETS USER DATA:
A get request will return the data on the user that you requested data for.
Data is returned in json format:
{"user_id" : user_id(string), "queue_id" : queue_id(interger)}
#### Delete Request to base_url/user/(user_id) DELETES A USER:
A delete request will delete the user.

## Class Queue:
A queue is a queue and is owned by a User(store owner).
### What data does a queue contain?:
{
        'queue_id' : interger(a random number),
        'name' : string(name of store),
        'ticket_prefix' : string(queue_id-),
        'curr_ticket' : interger(The current ticket, if one hundered people have used a queue in total than the curr_ticket = 100),
        'max_occupancy' : interger(maximum amount of people allowed in a store),
        'curr_occupancy' : interger(current amount of people inside a store
    }

#### URL: base_url/queue/(name(string)
#### Get Request to base_url/queue/(name(string) GETS QUEUE DATA:
Will get queue data for the queue where name = the name variable in the url, and returns it in json format as above
#### Put Request to base_url/queue/(name(string) CREATES A QUEUE:
*Note when doing a put request you must also provide an argument for maximum occupancy, Example: base_url/queue/(name(string), {'max_occupancy' : interger}* |
If the name provided is not unique the API will return "Queue Name Already Exists", else it will return the data in json format for the created queue.
#### Delete Request to base_url/queue/(name(string) DELETES A QUEUE:
Will delete the queue if it exists (make sure it does exist as it will crash your programm if not, sry for me being lazy)


## Class Ticket:
Ticket connected to a queue and contains the data for one user(in this case not store owner or the Class User but rather a customer)
### What data does a ticket contain?:
{
        'ticket_id' : string(queue_id-curr_ticket),
        'queue_id' : interger(queue_id to which the ticket belongs),
        'ticket_number' : interger(same as curr_ticket just when teh ticket was created),
        'date_created' : string(time at which the ticket was created),
        'date_entered' : string(time at which the ticket entered a store),
        'phone_number' : string(phone_number of the ticket owner)
    }
### URL: base_url/ticket
### Get Request to base_url/ticket GETS TICKET DATA:
For this get request it is also neccesary to provide an argument: {'ticket_id' : ticket_id}, Example: base_url/ticket, {'ticket_id' : ticket_id} |
This get request will return the data in json format as shown above.
### Put Request to base_url/ticket CREATES A TICKET:
For this put request it is required to provide two arguments: {''queue_id' : queue_id, 'phone_number' : phone_number}, Example: base_url/ticket, {''queue_id' : queue_id, 'phone_number' : phone_number} |
This put request will return the data for the created Ticket

## Class Ticket_Delete:
### URL: base_url/ticket-delete
### Get Request to base_url/ticket-delete DELETES A TICKET:
This Get Request requires an argument: {'ticket_id' : ticket_id}, Example: base_url/ticket-delete, {'ticket_id' : ticket_id} |
This get request will delete the ticket specified.

## Class Ticket_actions:
### URL: base_url/ticket-actions/string(ticket_id)
### Get Request to base_url/ticket-actions/string(ticket_id) UPDATES TICKET DATA TO SHOW THAT THE TICKET HAS ENTERED THE STORE:
You must provide a ticket_id in the url as shown above. This get request will also return json data about the ticket as shown previously in Class Ticket.
### Delete Request to base_url/ticket-actions/string(ticket_id) DELETES TICKET AND UPDATES STORE OCCUPANCY:
Works the same as the delete request in Class Ticket but will also update the store occupancy.
### Notes for Classt Ticket_actions:
Basically use the get request when someone enters the store and the delete request from here when someone leaves the store.
Use the requests from Class Ticket to create a ticket, get data from a ticket, and delete a ticket if a user leaves a queue or something before they enter the store.

If you have any questions ask Marius S., sry if the docs are hard to read, I am kind of very sleep deprived atm...


# Frequently used requests:
### Creating a User:
request = PUT https://99bac19acf0e.ngrok.io/user/(put user_id here)
### Creating a Queue:
request = PUT https://99bac19acf0e.ngrok.io/queue/(put queue/store name here), {"max_occupancy" : interger, "user_id" : string}
### Creating a Ticket:
request = PUT https://99bac19acf0e.ngrok.io/ticket, {"queue_id" : interger, "phone_number" : string}
### Updating a Ticket upon entrance to the store:
request = GET https://99bac19acf0e.ngrok.io/ticket-actions/(put ticket_id here)
### Deleting a Ticket upon exit of the customer:
request = DELETE https://99bac19acf0e.ngrok.io/ticket-actions/(put ticket_id here)

# Frequently user GET Requests:
### Getting data of a User:
request = GET https://99bac19acf0e.ngrok.io/user/(put user_id here)
### Getting data of a Queue:
request = GET https://99bac19acf0e.ngrok.io/queue/(put queue name(not queue_id) here)
### Getting data of a Ticket:
request = GET https://99bac19acf0e.ngrok.io/ticket, {"ticket_id" : string(ticket_id)}
