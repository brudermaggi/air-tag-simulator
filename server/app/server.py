from fastapi import FastAPI
from fastapi.params import Body
import requests
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
    conn.connect()

    id = reg["id"]
    cursor = conn.cursor()
    query = f"INSERT INTO airtags.tags (id) VALUES ({id})"

    if isinstance(id, int):
        try:
            cursor.execute(query)
            conn.commit()
            conn.close()
            return 200
        except mysql.connector.errors.IntegrityError:
            conn.close()
            print("ID already registered, proceed with coords")
            conn.close()
            return 200
        
    else:
        conn.close()
        return 400



#============================================Coords======================================================
@app.post("/coords")
async def getCoords(coords : dict = Body(...)):
    conn.connect()
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
        conn.close()
        return 200
    else:
        conn.close()
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




#==========================================Debug functions================================================
@app.post("/disconnect")
def disconnect():
    conn.close()
    return {"MySQL":"Disconnected"}