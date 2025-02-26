from fastapi import FastAPI, HTTPException, Body
import requests
import mysql.connector
from pydantic import BaseModel
from typing import Dict,Any
from fastapi.middleware.cors import CORSMiddleware
import time


app = FastAPI()
table_name = "tags"

class regAirtag(BaseModel):
    id: int
    name: str

class Coords(BaseModel):
    id: int
    lon: float
    lat: float



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Für Entwicklung, im Produktivbetrieb einschränken
    allow_methods=["POST"],
)


#==========================================Database======================================================

conn = mysql.connector.connect(
    host="mysql",
    user="root",
    password="root",
    database="airtags",
    port="3306"
)

#==========================================WebService====================================================

@app.post("/checkregister")
async def checkregister(airtag: dict = Body(...)):
    try:
        cursor = conn.cursor()
        id = airtag["id"]
        query = "SELECT * FROM tags WHERE id = %s;"
        cursor.execute(query, (id,))
        result = cursor.fetchall()
        
        if len(result) > 0:
            return 200
        else:
            return 400
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()



#==========================================Registration==================================================
@app.post("/register")
async def register(dict : dict = Body(...)):
    conn.connect()

    id = dict["id"]
    print(id)
    cursor = conn.cursor()

    # SQL-Query mit Platzhaltern für Werte
    id_query = "INSERT INTO airtags.tags (id) VALUES (%s);"
    id_data = (id, )

    if isinstance(id, int):
        try:
            cursor.execute(id_query, id_data)
            conn.commit()
            conn.close()
            print("ID registered, proceed with coords")
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
async def getCoords(coords: Coords):
    print("Getting Coords")
    try:
        conn.connect()
        id = coords.id
        lon = coords.lon
        lat = coords.lat

        # Validate and convert lon/lat
        try:
            lon = float(lon)
            lat = float(lat)
        except ValueError:
            return {"error": "Invalid coordinates"}, 400

        cursor = conn.cursor()

        query = "UPDATE tags SET lon = %s, lat = %s WHERE id = %s;"
        query_data = (lon, lat, id)

        print("Inserting into database")
        cursor.execute(query, query_data)
        conn.commit()

        print("Committed Coordinates")
        return {"message": "Success"}, 200

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Internal server error"}, 500

    finally:
        conn.close()

#===============================================Tags=====================================================

@app.get("/tags")
def updateTags():

    conn.connect()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name};"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

#=================================================Change Airtag Nsme=====================================
#TODO Datentyp Prüfung
@app.post("/tags/changeName")
def changeName(body : dict = Body(...)):
    conn.connect()
    id = body["id"]
    name = body["name"]
    cursor = conn.cursor()
    query = "UPDATE tags SET name = %s WHERE id = %s;"
    data = (name, id)
    cursor.execute(query,data)
    conn.commit()
    conn.close()
    return 200


@app.post("/tags/delete")
def deleteTag(body : dict = Body(...)):
    conn.connect()
    id = body["id"]
    cursor = conn.cursor()
    query = "DELETE FROM tags WHERE id = %s;"
    cursor.execute(query,(id,))
    conn.commit()
    conn.close()
    return 200

#==========================================Tone===========================================================

#TODO: Implement tone
@app.get("/tone")
def play_sound(dict : dict = Body(...)):
    id = dict["id"]
    url = f"http://airtag:{id}/tone"  
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