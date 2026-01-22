# FastAPI RDF Converter Application

This FastAPI application allows for easy processing of YAML and CSV files to generate and manipulate RDF (Resource Description Framework) files. It supports:

- Generate r2rml script from yaml 
- Converting data from CSV or DB into RDF formats.Dynamically generating RDF files based on specified configurations
- Upload to the GraphDB repo

## Features

- **generate-r2rml**: Return the r2rml script from the yaml file and the data
- **load_gdb**: load a specified ttl file to graph db 
- **rdf_generation** Take as input yaml/ttl file, data or DB string to convert in RDF

## Requirements

- Docker
- Alternatively, a local Python environment with Python version 3.8 or higher.

## Installation & Running the Application

### Running Locally

1. **Set up a virtual environment**:

    For Unix/macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    For Windows:
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```

2. **Install the requirements**:
    ```bash
    pip install fastapi==0.103.0 kglab==0.6.6 morph-kgc==2.7.0 pandas==2.2.2 uvicorn==0.20.0 PyYAML python-multipart
    ```

3. **Run the server**:
    ```bash
    uvicorn main:app --reload
    ```

### Running with Docker

1. **Build the Docker image**:
    ```bash
    docker build -t rdf-converter .
    ```

2. **Run the container**:
    ```bash
    docker run -dp 8000:8000 rdf-converter
    ```

   The application will be accessible at `http://localhost:8000`.

## API Endpoints

### POST `/generate-r2rml/`
- **Expected Data**:
  - `yarrrml_file`: A YARRRML file (extension .yaml or .yml).

#### Example using `curl`:

```bash
curl -X 'POST' 'http://localhost:8000/generate-r2rml/' \\
  -H 'Content-Type: multipart/form-data' \\
  -F 'yarrrml_file=@path_to_your_yaml_file.yaml'
```

### POST `/load_gdb/`
- **Expected Data**:
  - `graph_address`: GraphDB base URL (e.g., http://localhost:7200).
  - `repo_name`: GraphDB repository name.
  - `file_name`: File name located in the transfer directory.

#### Example using `curl`:

```bash
curl -X 'POST' 'http://localhost:8000/load_gdb/' \\
  -F 'graph_address=http://localhost:7200' \\
  -F 'repo_name=my_repo' \\
  -F 'file_name=output.ttl'
```

### POST `/rdf_generation/`
- **Expected Data**:
  - `file_config`: Mapping configuration file (.yaml/.yml or .ttl).
  - `data_tabular`: CSV file (required when `DB=false`).
  - `DB`: Boolean flag to use DB mode.
  - `db_str`: Database connection string (required when `DB=true`).

#### Example using `curl`:

```bash
curl -X 'POST' 'http://localhost:8000/rdf_generation/' \\
  -H 'Content-Type: multipart/form-data' \\
  -F 'file_config=@path_to_config.yaml' \\
  -F 'data_tabular=@path_to_data.csv' \\
  -F 'DB=false'
```
