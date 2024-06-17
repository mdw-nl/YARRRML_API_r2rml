import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from typing import Optional


class mappingItemSourceColumns(BaseModel):
    name: str
    type: str
    nullable: bool


class mappingItemSourceTables(BaseModel):
    name: str
    columns: List[mappingItemSourceColumns]


class mappingItemSource(BaseModel):
    name: str
    type: str
    tables: List[mappingItemSourceTables]


class mappingItemMappingSource(BaseModel):
    database: Optional[str] = None
    schema: Optional[str] = None
    table: Optional[str] = None
    column: str


class mappingItemMappingTarget(BaseModel):
    primary_sub:bool
    type: str
    uri: str
    name: str


class mappingItemMapping(BaseModel):
    uri: dict
    type: str
    source: mappingItemMappingSource
    target: dict


class FlexibleData(BaseModel):
    source: List[mappingItemSource]
    mappings: List[mappingItemMapping]


def generate_yaml():
    name: str
    s: str
    typeSub: str
    o: str
