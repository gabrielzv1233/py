import shelve

# Open the database file
# The text after the last / is the filename of the database, otherwise its the folder
# Folders are not created automatically but the database file is
db = shelve.open('databases/database/mydatabase')

# Set a key-value pair
db['string'] = 'value'
db['num'] = 123
db['bool'] = True
db['list'] = ["text", True, 0]
# Get a value by key
string = db['string']
num = db['num']
bool = db['bool']
list = db['list']
print(f"{string}, {num}, {bool}, {list}")

# Delete a key
del db['string'] 
del db['num']
del db['bool']
del db['list']

# Close the database
db.close()