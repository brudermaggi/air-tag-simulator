import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import time


FASTAPI_SERVER = "http://server:8000"


app = FastAPI()


class Airtag:
    def __init__(self, id: int, long: float, lat: float):
        self.id = id
        self.long = long
        self.lat = lat




    def check_server_connection(self):
        response = requests.post(f"{FASTAPI_SERVER}/health")
        print(response.status_code)
        try:
            if response.status_code == 200:
                print(" FastAPI server is reachable.")
                return True
        except requests.exceptions.RequestException:
            print(" FastAPI server is unreachable. Retrying in 5 seconds...")
        return False




    def register(self):

        if not self.check_server_connection():
            print(" Cannot register")
            return False
        response = requests.post(f"{FASTAPI_SERVER}/register", json={"id": self.id})
        print(response)
        if response.status_code == 200:
            print("Successfully registered")
            return True
        else:
            print(" Error during registration")
            return False




    def sendCoords(self):
        if not self.register():
            print("Registration failed. Stopping process.")
            return


        for i in range(4):
            data = {"lon": self.long, "lat": self.lat}

            try:

                response = requests.post(f"{FASTAPI_SERVER}/coords", json=data)

                if response.status_code == 200:
                    print(f"Sent coordinates {i + 1}/4 successfully.")
                else:
                    print(f"Failed to send coordinates {i + 1}/4. Status Code: {response.status_code}")

            except Exception as e:
                print(f"Error occurred while sending coordinates {i + 1}/4: {e}")


            time.sleep(10)
            print(f"Sent coordinates {i + 1}/4")


            time.sleep(10)




    def playSound(self):

        print(" Playing sound!")

p1 = Airtag(8001, 0, 0)



class Command(BaseModel):
    action: str



@app.get("/start")
def start():
    p1.sendCoords()
    return {"status": "Started"}






@app.post("/tone")
async def execute_command(command: Command):
    if command.action == "play_sound":
        p1.playSound()
        return {"status": "Sound played"}
    return {"status": "Unknown command"}


if __name__ == "__main__":
    p1.sendCoords()
    uvicorn.run(app, host="0.0.0.0", port=8001)
