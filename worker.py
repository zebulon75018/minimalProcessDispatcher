import threading
import time
import os
import subprocess
import uvicorn
from fastapi import FastAPI

import sqliteprocess

app = FastAPI()

@app.get("/")
async def home():
    return {"Hello": "FastAPI"}


def DBwatcher():
    sp = sqliteprocess.SqliteProcess()
    while(True):
        process = sp.getNextProcess()
        print(process)
        if process is None or len(process) == 0:
            time.sleep(1)
        else:
            sp.reserveProcess(process[0])  # field id
            sysprocess = subprocess.Popen(process[1], shell=True,
                                          stdout=subprocess.PIPE,
                                          universal_newlines=True)
            print(sysprocess.pid) 

       	    os.system(process[1])          # field processcmd
            sp.processIsDone(process[0])   # field id
        print("watching")

if __name__ == "__main__":
     thread_fastapi = threading.Thread(name='Web App FastApi', daemon=True, target=DBwatcher)

     print("star thread FastApi")
     thread_fastapi.start()
     uvicorn.run("worker:app", host="0.0.0.0", port=5001, debug=True,log_level="info")

