from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
import subprocess
from src.config.constant import *
from src.config.Initialization import initialization_folders, save_yaml_in_dir, save_tabular_in_folder, \
    generate_graph, generate_config, check_format_save_file, check_format_config_yaml, data_check_format_init
from datetime import datetime
from typing import Optional
import logging
from src.work.json_process import FlexibleData
from fastapi import FastAPI
from src.work.utils import upload_graph_db

app = FastAPI()

logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


@app.post("/generate-r2rml/")
async def generate_r2rml_mapping(yarrrml_file: UploadFile = File(...)):
    """
    Upload yaml file to execute r2rml extraction
    The function will generate the r2rml mapping file only from the yaml
    :param yarrrml_file:

    :return:
    """
    await initialization_folders()
    yaml_path = f"{PATH_MAPPING}mapping.yaml"
    await save_yaml_in_dir(yaml_path, yarrrml_file)
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


@app.post("/generate-r2rml/")
async def upload_rdf(graph_address: str = Form(...), repo_name: str = Form(...),
                       file_name: str = Form(...)):
    """
    Function upload specified ttl file to the GraphDB repo

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


@app.post("/rdf_generation/")
async def generate_rdf_(yaml_config: Optional[UploadFile] = File(...),
                               data_tabular: UploadFile = File(...),
                               DB: bool = Form(False),
                               db_str: Optional[str] = Form(None)
                               ):
    """
    Upload yaml file to execute r2rml extraction
    :param DB:
    :param db_str:
    :param data_tabular:
    :param yaml_config:
    :return:
    """
    await initialization_folders()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    check_format_config_yaml(yaml_config)
    yaml_path = check_format_save_file(yaml_config)
    logging.info(f"DB is {DB} and string is {db_str}")
    await save_yaml_in_dir(yaml_path, yaml_config)
    logging.info(f"Mapping successfully saved in {yaml_path}")

    if DB is True:
        logging.info("DB specified setting up process")
        config = generate_config(db=DB, db_str=db_str, yaml_path=yaml_path)
        logging.info(f"Config generated...{config}")
    else:

        logging.info("No db in use ..trying using file ")
        await data_check_format_init(data_tabular)
        logging.info(f"Config defined with {PATH_PROCESSING_F} nad {yaml_path}")

        config = generate_config(yaml_path=yaml_path)
        logging.info(f"Config generated...{config}")

    save_loc = f"{PATH_TRANSFER}{timestamp}output.ttl"
    await generate_graph(config, save_loc)
    logging.info(f"Config defined with {PATH_PROCESSING_F} nad {yaml_path}")

    return {"Filename": f"{timestamp}output.ttl"}, FileResponse(save_loc, filename="output.ttl",
                                                                media_type='text/turtle')


