from pypresence import Presence
import time
import random

client_id = 'bot client id'
RPC = Presence(client_id) 
RPC.connect()

quotes =[
    "69", "420"
]

while True:
    RPC.update(details="Quote:", state=random.choice(quotes))
    time.sleep(1)