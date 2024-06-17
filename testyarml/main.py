from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
import yaml
import kglab
from src.config.constant import *
from datetime import datetime
import os
import pandas as pd
from io import StringIO
import logging
from src.work.json_process import FlexibleData
from fastapi import FastAPI
import json
from src.work.utils import upload_graph_db

app = FastAPI()

logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


@app.post("/process/")
async def receive_flexible_json(data: FlexibleData):
    return {"message": "Data received successfully", "data": data}


@app.post("/process-yaml/")
async def process_yaml_data(file: UploadFile = File(...)):
    """
    Upload yaml file to execute r2rml extraction
    :param file:
    :return:
    """
    if not file.filename.endswith('.yaml') and not file.filename.endswith('.yml'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .yaml or .yml files are accepted.")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = f"{PATH_MAPPING}{timestamp}.yaml"
    os.makedirs(os.path.dirname(PATH_MAPPING), exist_ok=True)

    with open(file_path, 'wb') as out_file:
        content = file.file.read()

        out_file.write(content)

    return {"filename": file.filename, "location": file_path}


@app.post("/upload-file/")
async def upload_file(file_input: UploadFile = File(...)):
    """


    :param file_input: csv file with the data to be converted
    :return:
    """
    logging.info(f"Working on {file_input.filename}")
    if file_input.filename.endswith('.csv'):
        logging.info(f"Data saved in folder {file_input.filename}")
        # Read the content of the file
        content = await file_input.read()
        # Use StringIO to convert bytes to a file-like string object for pandas
        content_str = StringIO(content.decode("utf-8"))
        df = pd.read_csv(content_str, sep=";")

        os.makedirs(os.path.dirname(PATH_DATA), exist_ok=True)
        os.makedirs(os.path.dirname(PATH_TRANSFER), exist_ok=True)

        file_path = f"{PATH_DATA}{file_input.filename}"
        logging.info(f"Data saved in folder {file_path}")
        df.to_csv(file_path)
        return {"Saved": True,}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .csv is accepted.")


@app.post("/conversion/")
async def generate_rdf(string_input: str = Form(...)):
    """

    :param string_input: name of the yaml file to be used for the r2rml generation.
    :return:
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    config = f"""
                                    [CONFIGURATION]
                                    udfs: {PATH_PROCESSING_F}
                                    [GTFS_CSV]
                                    mappings:{PATH_MAPPING}{string_input}
                                 """

    kg = kglab.KnowledgeGraph(
    )
    kg.materialize(config)
    save_loc = f"{PATH_TRANSFER}{timestamp}output.ttl"
    kg.save_rdf(save_loc)
    logging.info(f"Saved in temp location {save_loc}")
    # return FileResponse(save_loc, filename="output.ttl", media_type='text/turtle')
    return {"item_name": f"{timestamp}output.ttl", "name": "Item name"}


@app.post("/load_gdb/")
async def generate_rdf(graph_address: str = Form(...), repo_name: str = Form(...),
                       file_name: str = Form(...)):
    """

    :param repo_name: name repository in GraphDB
    :param file_name: name of the file with the rdf graph
    :param graph_address: address to the GraphDb instance
    :return:
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    status = upload_graph_db(graph_address, repo_name,
                    PATH_TRANSFER + file_name,
                    "application/x-turtle")
    return {"Complete": status}
