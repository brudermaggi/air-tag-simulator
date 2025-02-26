import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import time
import random
import os

FASTAPI_SERVER = "http://server:8000"

app = FastAPI()


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
            print("FastAPI server is unreachable. Retrying in 5 seconds...")
            time.sleep(5)
        return False
# ========================== Register if connection is 👌 ===========================

    def register(self):   
        print("Registering...")
        while not self.check_server_connection():
            print("Server is down. Cannot register. Retrying...")


        
        while True:
            try:
                response = requests.post(f"{FASTAPI_SERVER}/checkregister", json={"id": self.id})
                if response.status_code == 200:
                    print("Successfully registered.")
                    break
                else:
                    print(f"Error during registration: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Registration request failed: {e}")

            print("Retrying registration in 5 seconds...")
            time.sleep(5)

# ======================= send coords =====================================================
    def sendCoords(self):
        print("Starting to send coordinates...")
        self.register()
        

        print("Registration successful. Starting to send coordinates...")

        #while True:
        if not self.check_server_connection():
            print("Server is unreachable. Waiting for connection...")
            time.sleep(5)
            #continue  

            
        self.long = generate_random_longitude()
        self.lat = generate_random_latitude()

        data = {"id": self.id, "lon": self.long, "lat": self.lat}

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

        #time.sleep(20)

# ===================================== play sound =========================================

    def playSound(self):

        print("Playing sound!")

# ====================================== Coord generation ===================================
def generate_random_longitude(): 
    return round(random.uniform(47.2701, 55.0584), 6)  # West-East range

def generate_random_latitude():
    return round(random.uniform(5.8663, 15.0419), 6)  # North-South range


# ====================================== Creating Airtag ====================================
p1 = Airtag(8001,generate_random_longitude(), generate_random_latitude())



class Command(BaseModel):
    action: str

# ====================================== fast api ============================================

@app.get("/start")
def start():
    p1.sendCoords()
    return 200

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
async def execute_command(command: Command):
    if command.action == "play_sound":
        p1.playSound()
        return {"status": "Sound played"}
    return {"status": "Unknown command"}

# ====================== main runenr ===================================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
