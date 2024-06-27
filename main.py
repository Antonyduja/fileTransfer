from fastapi import FastAPI, HTTPException, Query, Form, UploadFile, File
from typing import List
from datetime import datetime
import os
import json
from fastapi.responses import FileResponse

app = FastAPI()

# Function to read config file
def read_config_file():
    current_directory = os.getcwd()
    config_file = None
    
    for file in os.listdir(current_directory):
        if file.endswith(".json"):
            config_file = file
            break
    
    if not config_file:
        raise FileNotFoundError("No configuration file found in the current directory.")
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

# Endpoint to list files with metadata for the folder path given in the json file
@app.get("/rootFileList")
def get_root_files_metadata():
    try:
        config = read_config_file()
        folder_location = config['folder_location']
        files_metadata = []
        for filename in os.listdir(folder_location):
            file_path = os.path.join(folder_location, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                # download_url = f"/download/filename?={file_path}"
                metadata = {
                    'filename': filename,
                    'type': os.path.splitext(filename)[1][1:],
                    'size': file_stat.st_size,
                    'last_modified': datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'downloadUrl': file_path
                }
            elif os.path.isdir(file_path):
                # list_url = f"/getFileList?folder={file_path}"
                metadata = {
                    'filename': filename,
                    'type': 'folder',
                    'size': None,
                    'last_modified': None,
                    'file_Path': file_path
                }
            files_metadata.append(metadata)
        file_details = {
            'fileCount': len(files_metadata),
            'files' : files_metadata 
            }
        if file_details:
            return file_details
        else:
            raise HTTPException(status_code=404, detail="No files found in the directory")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to fetch metadata of the files in a specific folder
@app.get("/getFileList")
def get_folder_files_metadata(folder: str = Query(..., description="path of the file to fetch metadata")):
    try:
        files_metadata = []
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                # download_url = f"/download/filename?={file_path}"
                metadata = {
                    'filename': filename,
                    'type': os.path.splitext(filename)[1][1:],
                    'size': file_stat.st_size,
                    'last_modified': datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'downloadUrl': file_path
                }
            elif os.path.isdir(file_path):
                list_url = f"/getFileList?folder={file_path}"
                metadata = {
                    'filename': filename,
                    'type': 'folder',
                    'size': None,
                    'last_modified': None,
                    'file_Path':list_url
                }
            files_metadata.append(metadata)
        file_details = {
            'fileCount': len(files_metadata),
            'files' : files_metadata 
            }
        if file_details:
            return file_details
        else:
            raise HTTPException(status_code=404, detail="No files found in the directory")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to download content of all files from the folder given in the json file
@app.get("/downloadAllFiles")
def save_all_files_to_current_directory():
    try:
        config = read_config_file()
        folder_location = config['folder_location']
        # files_content = []
        current_directory = os.getcwd()

        for filename in os.listdir(folder_location):
            file_path = os.path.join(folder_location, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                # files_content.append({"filename": filename, "content": file_content})
                new_file_path = os.path.join(current_directory, filename)
                with open(new_file_path, 'wb') as new_file:
                    new_file.write(file_content)
        
        return {"message": "content of the files have been saved in the current directory."}


        # if files_content:
        #     return files_content
        # else:
        #     raise HTTPException(status_code=404, detail="No files found in the directory")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to download a specific file from the folder given in the json file
@app.get("/downloadFile")
def save_file_to_current_directory(filename: str = Query(..., description="path of the file to save it in the current directory")):
    try:
        config = read_config_file()
        folder_location = config['folder_location']
        current_directory = os.getcwd()
        
        file_path = os.path.join(folder_location, filename)
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        with open(file_path, 'rb') as file:
            file_content = file.read()
        
        new_file_path = os.path.join(current_directory, filename)
        with open(new_file_path, 'wb') as new_file:
            new_file.write(file_content)
        
        return {
                "message": f"Content of the file '{filename}' has been saved in the current directory.",
                "downloadedPath": new_file_path
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to 
@app.get("/getContent")
def get_file_metadata(filename: str = Query(..., description="path of the file to get the metadata")):
    try:
        config = read_config_file()
        folder_location = config['folder_location']
        
        file_path = os.path.join(folder_location, filename)
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        file_path = os.path.join(folder_location, filename)
        if os.path.isfile(file_path):
            file_stat = os.stat(file_path)
            metadata = {
                'filename': filename,
                'file_extension': os.path.splitext(filename)[1][1:],
                'size': file_stat.st_size,
                'last_modified': datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'file_Path': file_path
            }
        # download_url = f"/download/filename={filename}"
        return {
                "fileDetail": metadata
                # "downloadUrl": download_url
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def download(filename: str = Query(..., description="path of the file to download")):
    # print("Hello")
    # config = read_config_file()
    # folder_location = config['folder_location']
    # file_path = os.path.join(folder_location, filename)
    file_path=filename
    # print(file_path) # /Users/arshiya/api/api-client-programming.ipynb
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    file_extension = os.path.splitext(filename)[1][1:].lower()
    media_type = 'application/octet-stream'
    if file_extension == 'pdf':
        media_type = 'application/pdf'
    return FileResponse(file_path, media_type=media_type, filename=filename)
# Run the FastAPI application with uvicorn

@app.post("/creatDocument")
async def upload_file(folder_location: str = Form(...), file_name: str = Form(...), file: UploadFile = File(...)):
    try:
        # Ensure folder_location is a valid path or handle accordingly
        # For example:
        # if not os.path.exists(folder_location):
        #     os.makedirs(folder_location)

        # Construct the file path
        config = read_config_file()
        root_folder = config['target_folder']
        file_path = os.path.join(root_folder,folder_location, file_name)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            while True:
                data = await file.read(1024)  # Read in chunks of 1KB
                if not data:
                    break
                buffer.write(data)

        return {"filename": file_name, "message": "File uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
