import os
from pathlib import Path
from .constant import *
import logging
import pandas as pd
from io import StringIO
import kglab
import csv
from fastapi import HTTPException


async def initialization_folders() -> None:
    """
    Create the required directory
    :return:
    """
    os.makedirs(os.path.dirname(PATH_DATA), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_TRANSFER), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_MAPPING), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_R2RLM), exist_ok=True)


def check_format_config_yaml(yaml_config):
    """
    Check that the file format is compatible
    :param yaml_config:
    :return:
    """
    logging.info(f"Filename is {yaml_config.filename}")
    if (not yaml_config.filename.endswith('.yaml') and not yaml_config.filename.endswith('.yml')) and \
            (not yaml_config.filename.endswith('.ttl')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .yaml, .yml, or .ttl files are accepted.")


async def data_check_format_init(data):
    if data.filename.endswith('.csv'):
        await save_tabular_in_folder(data)
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .csv is accepted.")


def check_format_save_file(file):
    """
    Select the format for the mapping file based on the input
    :param file:
    :return:
    """
    logging.info(f"File is {file}")
    if file.filename.endswith('.yaml') or file.filename.endswith('.yml'):
        return f"{PATH_MAPPING}mapping.yaml", "yml"
    if file.filename.endswith('.ttl'):
        return f"{PATH_MAPPING}mapping.ttl", "ttl"
    raise HTTPException(status_code=400, detail="Invalid file type. Only .yaml, .yml, or .ttl files are accepted.")


async def save_yaml_in_dir(yaml_path, yaml_config):
    """

    :param yaml_path:
    :param yaml_config:
    :return:
    """
    with open(yaml_path, 'wb') as out_file:
        content = yaml_config.file.read()
        out_file.write(content)
        logging.info(f"Yaml saved in folder {yaml_path}")


def remove_file(path_to_file) -> None:
    """

    :param path_to_file:
    :return:
    """
    if os.path.exists(path_to_file):
        os.remove(path_to_file)
    else:
        raise FileNotFoundError


async def save_tabular_in_folder(data_tabular):
    """
    Save the tabular date in the appropriate folder
    :param data_tabular:
    :return:
    """
    logging.info(f"Data saved in folder {data_tabular.filename}")
    content = await data_tabular.read()
    content_str = StringIO(content.decode("utf-8"))
    sample = content.decode("utf-8")[:1024]
    sniffer = csv.Sniffer()

    try:
        # Detect the delimiter
        dialect = sniffer.sniff(sample)
        delimiter = dialect.delimiter
    except csv.Error as e:
        logging.error(f"Could not detect delimiter: {e}")
        delimiter = ','  # Default to comma if detection fails

    # Read the CSV file with the detected delimiter
    df = pd.read_csv(content_str, sep=delimiter)

    safe_filename = os.path.basename(data_tabular.filename)
    if safe_filename != data_tabular.filename:
        raise HTTPException(status_code=400, detail="Invalid file name.")
    data_root = Path(PATH_DATA).resolve()
    file_path = (data_root / safe_filename).resolve()
    if file_path.parent != data_root:
        raise HTTPException(status_code=400, detail="Invalid file path.")
    logging.info(f"Data saved in folder {file_path}")
    df.to_csv(file_path)


async def generate_graph(config, save_loc):
    """

    :param save_loc:
    :param config:
    :return:
    """

    kg = kglab.KnowledgeGraph()
    kg.materialize(config)

    kg.save_rdf(save_loc)
    logging.info(f"Saved in temp location {save_loc}")


def generate_config(**variables):
    """

    :return:
    """

    yaml_path = variables.get('yaml_path', 'default_path')
    db = variables.get('db', None)
    if db:
        logging.info("Entering config db")
        db_str = variables.get('db_str', None)
        config = f"""
                                                [CONFIGURATION]
                                                udfs: {PATH_PROCESSING_F}
                                                [GTFS_CSV]
                                                db_url: {db_str}
                                                mappings:{yaml_path}
                                             """
    else:
        config = f"""
                                            [CONFIGURATION]
                                            na_values= #N/A,N/A,#N/A N/A,n/a,NA,<NA>,#NA,NULL,null,NaN,nan,None
                                            udfs: {PATH_PROCESSING_F}
                                            [GTFS_CSV]
                                            mappings:{yaml_path}
                                         """
    return config
