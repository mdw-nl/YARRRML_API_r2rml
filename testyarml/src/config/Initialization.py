import os
from .constant import *
import logging
import pandas as pd
from io import StringIO
import kglab


def initialization_folders() -> None:
    """
    Create the required directory
    :return:
    """
    os.makedirs(os.path.dirname(PATH_DATA), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_TRANSFER), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_MAPPING), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_R2RLM), exist_ok=True)


def save_yaml_in_dir(yaml_path, yaml_config):
    """

    :param yaml_path:
    :param yaml_config:
    :return:
    """
    with open(yaml_path, 'wb') as out_file:
        content = yaml_config.file.read()
        out_file.write(content)
        logging.info(f"Yaml saved in folder {yaml_path}")


async def save_tabular_in_folder(data_tabular):
    """
    Save the tabular date in the appropriate folder
    :param data_tabular:
    :return:
    """
    logging.info(f"Data saved in folder {data_tabular.filename}")
    content = await data_tabular.read()
    content_str = StringIO(content.decode("utf-8"))
    df = pd.read_csv(content_str, sep=";")
    file_path = f"{PATH_DATA}{data_tabular.filename}"
    logging.info(f"Data saved in folder {file_path}")
    df.to_csv(file_path)


def generate_graph(config, save_loc):
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