import json
from fastapi import FastAPI
from swagger_for_mkdocs.transform_app import modify_app_for_swagger

def generate_openapi_config(app: FastAPI, title: str, tags: str, version: str, middleware: bool) -> dict:
    """
    Generates OpenAPI config from a FastAPI app with optional modifications.
    """
    modified_app = modify_app_for_swagger(app, title=title, tags=tags, version=version, middleware=middleware)
    return modified_app.openapi()

def save_openapi_json(openapi_data: dict, path: str = '', config_name: str = 'openapi.json') -> None:
    """
    Saves OpenAPI data to a JSON file.
    """
    with open(path + config_name, "w") as file:
        json.dump(openapi_data, file, indent=2)

def change_server_host(openapi_json: dict, new_host: str, description: str) -> dict:
    """
    Change server in openapi_json to correspond with the server used for the FastAPI endpoint.

    Args:
        openapi_json: dictionary structured with the openapi format.
        new_host: string with the base url
        description: description of the new server

    Returns:
        openapi_json: json file structured with the openapi format.
    
    
    """
    # Load JSON string into a dictionary
    openapi_json['servers'] = [{
                                "url": new_host,
                                "description": description
                                }]
    return openapi_json

def save_openapi_config(app: FastAPI, path: str = '', config_name: str = 'openapi.json',
                        title: str = "", tags: str = None, version: str = "",
                        host: str = None, description: str = 'No description.', middleware: bool = True) -> None:
    """
    Saves and corrects the OpenAPI configuration as a JSON file.

    Args:
        app: FastAPI object.
        path: Location to store the OpenAPI configuration.
        config_name: Name of the OpenAPI configuration file.
        title: Title of FastAPI app.
        tags: Tags related to FastAPI app.
        version: Version of FastAPI app.
        host: Base URL of the server.
        description: Description of the FastAPI app.
        middleware: Allow middleware to be set.
    """
    openapi_config = generate_openapi_config(app, title=title, tags=tags, version=version, middleware=middleware)
    if host:
        openapi_config = change_server_host(openapi_config, host, description)
    save_openapi_json(openapi_config, path=path, config_name=config_name)
