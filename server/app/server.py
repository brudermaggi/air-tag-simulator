from fastapi import FastAPI
from fastapi.params import Body
import requests
import uvicorn
from pydantic import BaseModel
import Airtag
import mysql.connector

app = FastAPI()
table_name = "tags"



#==========================================Database======================================================

conn = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root",
    database="airtags",
    port="3306"
)

#==========================================WebService====================================================


#==========================================Registration==================================================
@app.post("/register")
async def register(reg: dict = Body(...)):
    id = reg["id"]
    cursor = conn.cursor()
    query = f"INSERT INTO airtags.tags (id) VALUES ({id})"

    if isinstance(id, int):
        print("Inserting into database")
        cursor.execute(query)
        print(f"Inserted into database {query}")
        conn.commit()
        print("Committed")
        

        return 200
    else:
        return 400



#=========================================================================================================
@app.post("/coords")
async def getCoords(coords : dict = Body(...)):
    id = coords["id"]
    lon = coords["lon"]
    lat = coords["lat"]
    cursor = conn.cursor()
    query = f"UPDATE {table_name} SET lon = {lon}, lat = {lat} WHERE id = {id};"

    if isinstance(lon, float) and isinstance(lat, float):
        print("Inserting into database")
        cursor.execute(query)
        conn.commit()
        
        print("Committed Coordinates")
        return 200
    else:
        return 400




#==========================================Tone===========================================================
@app.get("/tone")
def play_sound():
    url = "http://airtag:8001/tone"  # Adjust if hosted elsewhere
    payload = {"action": "play_sound"}  # JSON payload
    response = requests.post(url, json=payload)  # Sending request
    print(response.json())  # Print server response













#==========================================StatusCheck for AirTag=========================================
@app.post("/health")
def health():
    return 200   

@app.post("/disconnect")
def disconnect():
    conn.close()
    return {"MySQL":"Disconnected"}