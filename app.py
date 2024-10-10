from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import json

app = FastAPI()

# Path to the folder where images will be stored
FILE_STORAGE_PATH = "file-storage"
METADATA_FILE = "file_metadata.json"


# Load metadata from JSON file
def load_metadata():
    if not os.path.exists(METADATA_FILE):
        return {}
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)


# Save metadata back to JSON file
def save_metadata(metadata):
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)

@app.post("/upload-file/")
async def upload_file(file: UploadFile, code: str):
    # Ensure the storage folder exists
    code_dir = os.path.join(FILE_STORAGE_PATH, code)
    if not os.path.exists(code_dir):
        os.makedirs(code_dir)

    # Save the uploaded file to the folder
    file_path = os.path.join(code_dir, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    # Update the metadata JSON
    metadata = load_metadata()

    # Append new file metadata to the given code
    if code not in metadata:
        metadata[code] = []

    metadata[code].append({
        "filename": file.filename,
        "path": file_path,
        "upload_date": "2024-10-06",  # Here you can replace this with current date dynamically
        "size": os.path.getsize(file_path),
        "file_type": file.content_type
    })

    save_metadata(metadata)

    return {"message": "File uploaded successfully", "path": file_path}

@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}, 404
