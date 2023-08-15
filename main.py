import configparser # pip install configparser
from telethon import TelegramClient, events # pip install telethon
from datetime import datetime
import MySQLdb # pip install mysqlclient
import mysql.connector
import requests

url = "https://smsplus.sslwireless.com/api/v3/send-sms"
response = requests.get(url)

### Initializing Configuration
print("Initializing configuration...")
config = configparser.ConfigParser()
config.read('config.ini')


API_ID = config.get('default','api_id') 
API_HASH = config.get('default','api_hash')
BOT_TOKEN = config.get('default','bot_token')
session_name = "sessions/Bot"


# Read values for MySQLdb
HOSTNAME = config.get('default','hostname')
USERNAME = config.get('default','username')
PASSWORD = config.get('default','password')
DATABASE = config.get('default','database')
 

# Start the Client (telethon)
client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token=BOT_TOKEN)

### START COMMAND
@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id
    
    # set text and send message
    text = "Hello i am a bot that can do CRUD operations inside a MySQL database"
    await client.send_message(SENDER, text)


@client.on(events.NewMessage(pattern="(?i)/api"))
async def start(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id
    
    # set text and send message
    if response.status_code == 200:
        data = response.json()
        data = str(data)
    await client.send_message(SENDER, data)








   




def create_message_select_query(ans):
    text = ""
    for i in ans:
        id = i[0]
        name = i[1]
        dob = i[2]
        is_graduated = i[3]
        
        text += "<b>"+ str(id) +"</b> | " + "<b>"+ str(name) +"</b> | " + "<b>"+ str(dob)+"</b> | " + "<b>"+ str(is_graduated)+"</b>\n"
    message = "<b>Received :</b> Information about students:\n\n"+text
    return message


### SELECT COMMAND
@client.on(events.NewMessage(pattern="(?i)/select"))
async def select(event):
    try:
        # Get the sender
        sender = await event.get_sender()
        SENDER = sender.id

        # Get the text of the user AFTER the /update command and convert it to a list (we are splitting by the SPACE " " simbol)
        list_of_words = event.message.text.split(" ")
        sid = list_of_words[1] # second (1) item is the id
        #print(sid)

        # create the tuple/list with all the params interted by the user
        params = [sid]

        # Create the UPDATE query, we are updating the product with a specific id so we must put the WHERE clause
        sql_command="SELECT * FROM student WHERE sid= %s"
        crsr_mysql.execute(sql_command, params) # Execute the query
        #conn.commit() # Commit the changes
        res = crsr_mysql.fetchall()
        if(res):
            text = create_message_select_query(res)
            await client.send_message(SENDER, text, parse_mode='html')
        # Otherwhise, print a default text
        else:
            text = "No student found inside the database."
            await client.send_message(SENDER, text, parse_mode='html')

    except Exception as e: 
        print(e)
        await client.send_message(SENDER, "Something Wrong happened... Check your code!", parse_mode='html')
        return
   
    
    
    '''
    try:
        
        # Get the sender of the message
        sender = await event.get_sender()
        SENDER = sender.id
        # Execute the query and get all (*) the oders
        query = "SELECT * FROM student"
        crsr_mysql.execute(query)
        #crsr_mysql.execute(" SELECT * FROM student ")
        #print("yo")
        res = crsr_mysql.fetchall() # fetch all the results
        # If there is at least 1 row selected, print a message with the list of all the oders
        # The message is created using the function defined above
        print(res)
        if(res):
            text = create_message_select_query(res)
            await client.send_message(SENDER, text, parse_mode='html')
        # Otherwhise, print a default text
        else:
            text = "No student found inside the database."
            await client.send_message(SENDER, text, parse_mode='html')

    except Exception as e: 
        print(e)
        await client.send_message(SENDER, "Something Wrong happened... Check your code!", parse_mode='html')
        return
        '''



##### MAIN
if __name__ == '__main__':
    try:
        print("Initializing Database...")
        #conn_mysql = MySQLdb.connect( host=HOSTNAME, user=USERNAME, passwd=PASSWORD, database= DATABASE  )
        #crsr_mysql = conn_mysql.cursor()
        connection = mysql.connector.connect(
        host=HOSTNAME, 
        user=USERNAME, 
        passwd=PASSWORD, 
        database= DATABASE )
        if connection.is_connected():
            print("Connected to MySQL database")
            crsr_mysql = connection.cursor()    

            print("Bot Started...")
            client.run_until_disconnected()

    except Exception as error:
        print('Cause: {}'.format(error))