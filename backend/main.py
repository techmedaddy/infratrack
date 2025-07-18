from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

latest_stats = {}

@app.post("/stats")
async def receive_stats(request: Request):
    global latest_stats
    data = await request.json()
    latest_stats = data
    print("Received stats:", data)
    return {"message": "Stats received!"}

@app.get("/latest-stats")
def get_latest_stats():
    return latest_stats or {"message": "No stats yet"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
