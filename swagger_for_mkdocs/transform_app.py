from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




def modify_app_for_swagger(app: FastAPI, title: str = "", tags: str = None, version: str="", middleware: bool = True) -> FastAPI:
    """
    Chan FastAPI app to improve swagger documentation in mkdocs.

    Args:
        title: Title of FastAPI app.
        tags: Tags related to FastAPI app.
        version: Version of FastAPI app.
        middleware: Allow middelware to be set. 
    """

    # Set metadata
    app.title = title
    app.openapi_tags = tags
    app.version = version

    # Add CORS middleware
    if middleware:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],# Allow requests from any origin
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )

    return app
