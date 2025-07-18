from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import uuid

app = FastAPI()

# Enable CORS for your frontend running on Vite (default is http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for latest stats (replace this with DB in production)
latest_stats = {
    "total_errors": 0,
    "most_common_error": "",
    "last_uploaded_file": ""
}

# GET route to fetch stats
@app.get("/latest-stats")
def get_latest_stats():
    return latest_stats

# POST route to handle file upload
@app.post("/upload-log")
async def upload_log(file: UploadFile = File(...)):
    if not file.filename.endswith((".log", ".txt", ".csv", ".json")):
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    contents = await file.read()
    decoded = contents.decode("utf-8")

    # Simple analysis: count lines with "error" or "fail"
    error_lines = [line for line in decoded.splitlines() if "error" in line.lower() or "fail" in line.lower()]
    total_errors = len(error_lines)

    # Naive most common error message
    from collections import Counter
    error_counts = Counter(error_lines)
    most_common_error = error_counts.most_common(1)[0][0] if error_counts else ""

    # Update global stats
    latest_stats["total_errors"] = total_errors
    latest_stats["most_common_error"] = most_common_error
    latest_stats["last_uploaded_file"] = file.filename

    # Optional: save file locally
    upload_dir = "uploaded_logs"
    os.makedirs(upload_dir, exist_ok=True)
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    with open(os.path.join(upload_dir, unique_filename), "wb") as f:
        f.write(contents)

    return {"message": "Log file processed", "total_errors": total_errors, "most_common_error": most_common_error}
