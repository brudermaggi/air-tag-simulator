from fastapi import FastAPI
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
async def register(id: int):
    cursor = conn.cursor()
    query = f"INSERT INTO airtags.tags (id) VALUES ({id})"

    if isinstance(id, int):
        print("Inserting into database")
        cursor.execute(query)
        print(f"Inserted into database {query}")
        conn.commit()
        print("Committed")
        conn.close()

        return 200
    else:
        return 400





@app.post("/health")
async def health():
    return 200   