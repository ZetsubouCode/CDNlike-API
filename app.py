from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import uuid

app = FastAPI()
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, new_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": "File uploaded successfully", "file_path": new_filename}

@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}, 404
