from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
import subprocess
from src.config.constant import *
from src.config.Initialization import initialization_folders, save_yaml_in_dir, save_tabular_in_folder, \
    generate_graph, generate_config
from datetime import datetime

import logging
from src.work.json_process import FlexibleData
from fastapi import FastAPI
from src.work.utils import upload_graph_db

app = FastAPI()

logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


@app.post("/process/")
async def receive_flexible_json(data: FlexibleData):
    return {"message": "Data received successfully", "data": data}


@app.post("/generate-r2rml/")
async def generate_yaml_r2rml(yarrrml_file: UploadFile = File(...)):
    """
    Upload yaml file to execute r2rml extraction
    The function will generate the r2rml mapping file only from the yaml
    :param yarrrml_file:

    :return:
    """
    initialization_folders()
    yaml_path = f"{PATH_MAPPING}mapping.yaml"
    save_yaml_in_dir(yaml_path, yarrrml_file)
    logging.info(f"Mapping successfully saved in {yaml_path}")
    try:
        subprocess.run(
            ['yarrrml-parser', '-i', yaml_path, '-o', f"{PATH_R2RLM}file.ttl"],
            check=True
        )
        print(f"Successfully converted {yaml_path} to {PATH_R2RLM}file.ttl")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    return FileResponse(f"{PATH_R2RLM}file.ttl", filename="file.ttl", media_type='text/turtle')


@app.post("/load_gdb/")
async def generate_rdf(graph_address: str = Form(...), repo_name: str = Form(...),
                       file_name: str = Form(...)):
    """

    :param repo_name: name repository in GraphDB
    :param file_name: name of the file with the rdf graph
    :param graph_address: address to the GraphDb instance
    :return:
    """
    status = upload_graph_db(graph_address, repo_name,
                             PATH_TRANSFER + file_name,
                             "application/x-turtle")
    logging.info(f"Data successfully uploaded to GB repo{repo_name}")
    return {"Complete": status}


@app.post("/rdf_tabular/")
async def generate_rdf_tabular(yaml_config: UploadFile = File(...), data_tabular: UploadFile = File(...)):
    """
    Upload yaml file to execute r2rml extraction
    :param data_tabular:
    :param yaml_config:
    :return:
    """
    initialization_folders()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    if not yaml_config.filename.endswith('.yaml') and not yaml_config.filename.endswith('.yml'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .yaml or .yml files are accepted.")

    yaml_path = f"{PATH_MAPPING}mapping.yaml"
    await save_yaml_in_dir(yaml_path, yaml_config)
    logging.info(f"Mapping successfully saved in {yaml_path}")

    if data_tabular.filename.endswith('.csv'):
        await save_tabular_in_folder(data_tabular)
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .csv is accepted.")

    logging.info(f"Config defined with {PATH_PROCESSING_F} nad {yaml_path}")
    config = generate_config(yaml_path=yaml_path)
    save_loc = f"{PATH_TRANSFER}{timestamp}output.ttl"
    generate_graph(config, save_loc)
    logging.info(f"Config defined with {PATH_PROCESSING_F} nad {yaml_path}")
    return {"Filename": f"{timestamp}output.ttl"}, FileResponse(save_loc, filename="output.ttl",
                                                                media_type='text/turtle')
