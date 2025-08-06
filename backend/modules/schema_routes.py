from fastapi import APIRouter, HTTPException
from .weaviate_client import get_weaviate_client

router = APIRouter()

@router.get("/schema")
async def get_schema(weaviate_url: str):
    """
    獲取 Weaviate 實例的 Schema (包含所有 Class 及屬性)。
    """
    client = get_weaviate_client(weaviate_url)
    try:
        schema = client.schema.get()
        return schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve schema: {e}")
