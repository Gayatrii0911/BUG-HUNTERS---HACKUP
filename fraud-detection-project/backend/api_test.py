from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def run():
    print("API Test")
    print(client.get("/").json())

if __name__ == "__main__":
    run()
