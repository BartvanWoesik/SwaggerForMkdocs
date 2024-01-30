import json
from fastapi import FastAPI
from swagger_for_mkdocs.transform_app import modify_app_for_swagger


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



def save_openapi_json(app: FastAPI, 
                    path:str = '', 
                    config_name:str = 'openapi.json', 
                    host: str= None, 
                    description: str = 'No description.',
                    title: str = "", 
                    tags: str = None,
                    version: str="", 
                    middleware: bool = True):
    """
    Saves and corrects the openapi configuration as a json file. 
    
    Args:
        app: FastAPI object.
        path: Location to store the openapi configuration
        config_name: Name of the openapi configuration
        new_host: string with the base url
        title: Title of FastAPI app.
        tags: Tags related to FastAPI app.
        version: Version of FastAPI app.
        middleware: Allow middelware to be set. 
    
    """
    app = modify_app_for_swagger(app, title = title, tags = tags, version = version, middleware = middleware)

    openapi_data = app.openapi()
    if host:
        openapi_data = change_server_host(openapi_data, host , description)
 
    # Change "openapi.json" to desired filename
    with open(path + config_name, "w") as file:
        json.dump(openapi_data, file, indent =2 )