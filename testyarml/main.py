from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
import subprocess
from src.config.constant import *
from src.config.Initialization import initialization_folders, save_yaml_in_dir, save_tabular_in_folder, \
    generate_graph, generate_config, check_format_save_file, check_format_config_yaml, data_check_format_init
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging
import os
from src.work.utils import upload_graph_db

app = FastAPI()

logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


@app.post("/generate-r2rml/", tags=["R2RML Mapping"], summary="Generate R2RML Mapping")
async def generate_r2rml_mapping(yarrrml_file: UploadFile = File(...)):
    """
    Upload a YARRRML file to generate an R2RML mapping file.

    - **yarrrml_file**: The YARRRML file to be uploaded.
    - Generates the R2RML mapping file from the provided YARRRML file.

    Returns:
    - A `.ttl` file containing the generated R2RML mapping.
    """
    try:
        await initialization_folders()
        yaml_path = f"{PATH_MAPPING}mapping.yaml"
        await save_yaml_in_dir(yaml_path, yarrrml_file)
        logging.info(f"Mapping successfully saved in {yaml_path}")

        subprocess.run(
            ['yarrrml-parser', '-i', yaml_path, '-o', f"{PATH_R2RLM}file.ttl"],
            check=True,
            timeout=60
        )
        print(f"Successfully converted {yaml_path} to {PATH_R2RLM}file.ttl")
        return FileResponse(f"{PATH_R2RLM}file.ttl", filename="file.ttl", media_type='text/turtle')
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during YARRRML parsing: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate R2RML mapping.")
    except subprocess.TimeoutExpired as e:
        logging.error(f"Timeout during YARRRML parsing: {e}")
        raise HTTPException(status_code=504, detail="YARRRML parsing timed out.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.post("/load_gdb/", tags=["GraphDB Operations"], summary="Upload RDF to GraphDB")
async def upload_rdf(graph_address: str = Form(...), repo_name: str = Form(...),
                     file_name: str = Form(...)):
    """
    Upload an RDF file to a specified GraphDB repository.

    - **graph_address**: The address of the GraphDB instance.
    - **repo_name**: The name of the GraphDB repository.
    - **file_name**: The name of the RDF file to be uploaded.

    Returns:
    - A confirmation message indicating the status of the upload.
    """
    safe_filename = os.path.basename(file_name)
    if safe_filename != file_name:
        raise HTTPException(status_code=400, detail="Invalid file name.")
    transfer_root = Path(PATH_TRANSFER).resolve()
    file_path = (transfer_root / safe_filename).resolve()
    if file_path.parent != transfer_root:
        raise HTTPException(status_code=400, detail="Invalid file path.")
    status = upload_graph_db(graph_address, repo_name,
                             str(file_path),
                             "application/x-turtle")
    if not status:
        raise HTTPException(status_code=502, detail="Failed to upload data to GraphDB.")
    logging.info(f"Data successfully uploaded to GB repo{repo_name}")
    return {"Complete": status}


@app.post("/rdf_generation/", tags=["RDF Generation"], summary="Generate RDF from Config and Data")
async def generate_rdf_(file_config: Optional[UploadFile] = File(...),
                        data_tabular: Optional[UploadFile] = File(None),
                        DB: bool = Form(False),
                        db_str: Optional[str] = Form(None)
                        ):
    """
    Generate an RDF file from a provided configuration and optionally tabular data.

    - **file_config**: Configuration file in YAML format for generating the RDF.
    - **data_tabular**: Optional tabular data file.
    - **DB**: Boolean flag indicating if a database connection string is provided.
    - **db_str**: Database connection string (optional if `DB` is False).

    Returns:
    - A `.ttl` file containing the generated RDF.
    """
    await initialization_folders()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    check_format_config_yaml(file_config)
    file_conf_path, type_file = check_format_save_file(file_config)
    logging.info("DB is %s and db_str is %s", DB, "set" if db_str else "not set")
    await save_yaml_in_dir(file_conf_path, file_config)
    logging.info(f"Mapping successfully saved in {file_conf_path}")
    if not DB and not data_tabular:
        raise HTTPException(status_code=400, detail="Tabular data file required when DB=False")

    if DB is True:
        if DB and not db_str:
            raise HTTPException(status_code=400, detail="Database string is required when DB=True")
        logging.info("DB specified setting up process")
        config = generate_config(db=DB, db_str=db_str, yaml_path=file_conf_path)
        logging.info("Config generated for DB source")
    else:

        logging.info("No db in use ..trying using file ")
        await data_check_format_init(data_tabular)
        logging.info(f"Config defined with {PATH_PROCESSING_F} nad {file_conf_path}")

        config = generate_config(yaml_path=file_conf_path)
        logging.info("Config generated for file source")

    save_loc = f"{PATH_TRANSFER}{timestamp}output.ttl"
    await generate_graph(config, save_loc)
    logging.info(f"Config defined with {PATH_PROCESSING_F} nad {file_conf_path}")
    logging.info(f"Filename: {timestamp}output.ttl")

    return FileResponse(save_loc, filename="output.ttl",
                        media_type='text/turtle')
