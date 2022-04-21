
from asyncio import subprocess
from posixpath import dirname
from re import T
from fastapi import FastAPI , UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import aiofiles
from typing import List
import os
import shutil
from pydantic import BaseModel
from devtools import debug
from pathlib import Path

app = FastAPI()

class Files(BaseModel):
    folder: str
    name: str

class Text(BaseModel):
    text: str

@app.post("/read_txt")
async def test(file: Files):
    debug(file)
    try:
        with open('files/'+file.folder+'/'+file.name) as f:
            lines = f.readlines()
    except: 
        lines = None
    return lines

@app.get("/folder_size")
async def folder_size():
    
    def get_size(folder: str) -> int:
        return sum(p.stat().st_size for p in Path(folder).rglob('*'))

    def filesize(size: int) -> str:
        for unit in ("B", "K", "M", "G", "T"):
            if size < 1024:
                break
            size /= 1024
        return f"{size:.1f}{unit}"

    path = 'files/'
    
    return filesize(get_size(path))

@app.post("/upload-text")
async def create_upload_text(text: Text):
    now = datetime.now()
    date = now.strftime("%m%d%Y_%H%M%S")
    dirs = "files/"
    path = os.path.join(dirs, date)
    os.mkdir(path)
    n_d = now.strftime("%d.%m.%Y_%H:%M:%S")

    with open(path+'/'+n_d+'.txt', 'w') as f:
        f.write(text.text)

    return {"Result": "OK"}



@app.post("/upload-files")
async def create_upload_files(files: List[UploadFile] = File(...)):
    
    now = datetime.now()

    date = now.strftime("%m%d%Y_%H%M%S")
    dirs = "files/"
    path = os.path.join(dirs, date)
    os.mkdir(path)

    for file in files:
        debug(file.filename, file.content_type)
        if file.content_type == 'application/octet-stream':
            destination_file_path = "files/"+now.strftime("%m%d%Y_%H%M%S")+"/"+file.filename+'.txt' 
        else:
            destination_file_path = "files/"+now.strftime("%m%d%Y_%H%M%S")+"/"+file.filename

        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await file.read(1024):  
                await out_file.write(content)  
    return {"Result": "OK", "filenames": [file.filename for file in files]}

@app.get("/get_all_folder")
async def get_all_name():
    
    folder = os.listdir('files')
    names = [{f_name: os.listdir('files/'+f_name), 'size': os.path.getsize('files/'+f_name)} for f_name in folder]
    return names if names else None

@app.get("/delete_file")
async def delete_folder(name_folder: str):
    return shutil.rmtree('files/'+name_folder)

@app.post("/download-files")
async def download(file_path: Files):
    path = 'files/'+file_path.folder+"/"+file_path.name
    return FileResponse(path=path, media_type="application/json", filename=file_path.name)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Content-Type"
    ]
)