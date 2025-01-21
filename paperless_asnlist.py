#!/usr/bin/env python3
import requests
import configparser

def main():
    documents = api_get("/api/documents/?archive_serial_number__isnull=0&sort=archive_serial_number")
    parse_documents(documents['results'])

def parse_documents(documents: list):
    sorted_documents = sorted(documents, key=lambda x: x['archive_serial_number'])
    data = []
    for document in sorted_documents:
        archive_serial_number = document['archive_serial_number']
        title = document['title']
        correspondent = get_correspondent_by_id(document['correspondent'])
        created_at = document['created']
        data.append(f"ASN{archive_serial_number:09};{correspondent};{title};{created_at}")

    with open("asnlist.csv", "w") as f:
        f.write("ASN;Correspondent;Title;Created At\n")
        f.write("\n".join(data))

def get_correspondent_by_id(id: int):
    # Cache the correspondent names to reduce the number of API calls
    correspondent_cache = {}

    if not id in correspondent_cache:
        correspondent = api_get(f"/api/correspondents/{id}/")
        correspondent_cache[id] = correspondent['name']

    return correspondent_cache[id]

def api_get(endpoint):
    config = configparser.ConfigParser()
    config.read('paperless.cfg')

    try:
        url = config['paperless']['url']
        api_key = config['paperless']['api_key']
    except KeyError as e:
        raise ValueError(f"Missing required configuration key: {e}")

    headers = { "Authorization": f"Token {api_key}", "Accept": "application/json; version=6" }

    response = requests.get(url + endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    main()