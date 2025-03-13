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
### POST `/load_gdb/`
### POST `/rdf_generation/`


.

- **Expected Data**: 
  - `file`: A YAML file (extension .yaml or .yml).
  
#### Example using `curl`:

```bash
curl -X 'POST' 'http://localhost:8000/process-yaml/' -H 'Content-Type: multipart/form-data' -F 'file=@path_to_your_yaml_file.yaml'