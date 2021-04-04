from pypresence import Presence
import time
import os
import json
import psutil

appdata = os.getenv('APPDATA')
launcher_data_fullpath = appdata + "\.minecraft\launcher_profiles.json"
logs_fullpath = appdata + "\.minecraft\logs\latest.log"

start_time = None

mc = "javaw.exe"

with open(logs_fullpath,'r') as f:
    lines = f.readlines()
    for item in lines:
        if "Connecting to play.cubecraft.net., 25565" in item:
            if start_time == None:
                start_time = time.time()
            print(":)")

def getUserName():
    with open(launcher_data_fullpath, 'r') as f:
        launcher_data = json.load(f)

        database = launcher_data['authenticationDatabase']
        profiles = database[list(database.keys())[0]]['profiles']
        profile = profiles[list(profiles.keys())[0]]

        return profile["displayName"]

def checkCube():
    with open(logs_fullpath,'r') as f:
        lines = f.readlines()
        for line in lines:
            if "Connecting to play.cubecraft.net., 25565" in line:
                return True

def updatePresence():
    state = "Minigame - "
    details = f"Username  - {getUserName()}"
    large_image = "cclogo_lq"
    small_image = None
    large_text = "cubecraft.net"
    
    RPC.update(state=state, details=details, large_image=large_image, small_image=small_image, large_text=large_text, start=start_time, buttons=[{"label": "Website", "url": "https://cubecraft.net"}])

client_id = '827982404350115890' 
RPC = Presence(client_id) 
RPC.connect()

while True:
    
    if mc in (p.name() for p in psutil.process_iter()):

        if checkCube() == True:
            updatePresence()
        else:
            RPC.clear()
        
    else:
        start_time = None
        RPC.clear()

    time.sleep(15)
