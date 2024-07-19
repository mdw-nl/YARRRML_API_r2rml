import os
from constant import *
import logging
import pandas as pd
from io import StringIO
import kglab
import csv


def initialization_folders() -> None:
    """
    Create the required directory
    :return:
    """
    os.makedirs(os.path.dirname(PATH_DATA), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_TRANSFER), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_MAPPING), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_R2RLM), exist_ok=True)


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

    file_path = f"{PATH_DATA}{data_tabular.filename}"
    logging.info(f"Data saved in folder {file_path}")
    df.to_csv(file_path)


async def generate_graph(config, save_loc):
    """

    :param save_loc:
    :param config:
    :return:
    """

    kg = kglab.KnowledgeGraph(
    )
    kg.materialize(config)

    kg.save_rdf(save_loc)
    logging.info(f"Saved in temp location {save_loc}")


def generate_config(**variables):
    """

    :return:
    """
    yaml_path = variables.get('yaml_path', 'default_path')

    config = f"""
                                        [CONFIGURATION]
                                        udfs: {PATH_PROCESSING_F}
                                        [GTFS_CSV]
                                        mappings:{yaml_path}
                                     """
    return config
