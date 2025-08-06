import weaviate
from fastapi import HTTPException

def get_weaviate_client(weaviate_url: str):
    """
    Helper function to get Weaviate client.
    """
    try:
        client = weaviate.Client(url=weaviate_url)
        client.is_ready() # Check connection
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Weaviate: {e}")
