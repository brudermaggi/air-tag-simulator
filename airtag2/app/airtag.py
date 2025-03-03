import requests
import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel
import time
import random
import os
import docker
import threading

FASTAPI_SERVER = "http://server:8000"

app = FastAPI()

class Coord(BaseModel):
    id: int
    lon: float
    lat: float


# ============================ Class Airtag =======================================
class Airtag:
    def __init__(self, id: int, long: float, lat: float):
        self.id = id
        self.long = long
        self.lat = lat

# ============================ Checking server connection ==========================

    def check_server_connection(self):
        try:
            response = requests.post(f"{FASTAPI_SERVER}/health")
            print(response.status_code)
            if response.status_code == 200:
                print("FastAPI server is reachable.")
                return True
        except requests.exceptions.RequestException:
            print("FastAPI server is unreachable. Retrying in 1 seconds...")
            time.sleep(1)
        return False
    
# ========================== Register if connection is 👌 ===========================

    def register(self):   

        print("Registering...")
        while True:
            try:
                response = requests.post(f"{FASTAPI_SERVER}/register", json={"id": self.id})
                if response.status_code == 200:
                    print("Successfully registered.")
                    # Start sendCoords in a new thread
                    threading.Thread(target=self.sendCoords, daemon=True).start()
                    break
                else:
                    print(f"Error during registration: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Registration request failed: {e}")


# ======================= send coords =====================================================
    def sendCoords(self):
        print("Starting to send coordinates...")
        while True:
            self.long = generate_random_longitude()
            self.lat = generate_random_latitude()

            coords = Coord(id=self.id, lon=self.long, lat=self.lat)
            data = coords.model_dump()
            print(data)
            try:
                response = requests.post(f"{FASTAPI_SERVER}/coords", json=data)

                if response.status_code == 200:
                    print(f"Sent new coordinates successfully: ({self.long}, {self.lat})")
                else:
                    print(f"Failed to send coordinates. Status Code: {response.status_code}")
                    print("Retrying in 5 seconds...")
                    time.sleep(5)

            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                print("Retrying in 5 seconds...")
                time.sleep(5)

            time.sleep(20)
#===========================================================================================


    def regloop(self):
        while not self.register():
            print("retrying")


# ===================================== play sound =========================================

    def playSound(self):
        print("Playing sound!")

# ====================================== Coord generation ===================================
def generate_random_longitude(): 
    return round(random.uniform(47.2701, 55.0584), 6)  # West-East range

def generate_random_latitude():
    return round(random.uniform(5.8663, 15.0419), 6)  # North-South range


# ====================================== Creating Airtag ====================================
p1 = Airtag(8003,generate_random_longitude(), generate_random_latitude())
p1.register()


class Command(BaseModel):
    action: str

# ====================================== fast api ============================================



@app.post("/stop")
def stop_container():
    client = docker.from_env()
    container_id = os.environ.get("HOSTNAME")  

    try:
        container = client.containers.get(container_id)
        print(f"Stopping container: {container_id}")
        container.stop()
        return {"status": "Container stopped successfully."}
    except Exception as e:
        print(f"Error stopping container: {e}")
        return {"status": f"Error: {e}"}


@app.post("/tone")
def execute_command(command : Command):	
    if command.action == "play_sound":
        p1.playSound()
        return {"status": "Playing sound"}

# ====================== main runenr ===================================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
