import requests


def upload_graph_db(graphdb_url, repository_id, data_file, contenttype, timeout=30):
    """

    @param graphdb_url:
    @param repository_id:
    @param json_data_path:
    @return:
    """

    # Define the URL for the GraphDB REST API endpoint to upload data
    upload_url = f"{graphdb_url}/repositories/{repository_id}/statements"

    # Load JSON-LD data from a file

    with open(data_file, "r") as file:
        data = file.read()
        data = data.encode('utf-8')

    # Set headers for the HTTP request
    headers = {
        "Content-Type": contenttype,
    }

    # Send a POST request to upload the data to GraphDB

    try:
        response = requests.post(upload_url, data=data, headers=headers, timeout=timeout)
    except requests.RequestException as exc:
        print(f"Error connecting to GraphDB: {exc}")
        return False

    # Check the response
    if response.status_code in (200, 204):
        print("Data imported successfully.")
        return True
    else:
        print(data_file)
        print("Error importing data. Status code:", response.status_code)
        print("Response content:", response.content)
        return False
