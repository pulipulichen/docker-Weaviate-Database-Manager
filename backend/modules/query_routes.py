from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .weaviate_client import get_weaviate_client

router = APIRouter()

class QueryRequest(BaseModel):
    weaviate_url: str
    className: str
    queryText: str
    queryType: str = Field(..., pattern="^(vector|keyword|hybrid)$")
    alpha: Optional[float] = Field(None, ge=0.0, le=1.0)
    embeddingModel: Optional[str] = None
    filter: Optional[Dict[str, Any]] = None
    limit: int = 10
    offset: int = 0
    properties: Optional[List[str]] = None

@router.post("/query")
async def execute_query(request: QueryRequest):
    """
    執行 Weaviate 查詢。
    """
    client = get_weaviate_client(request.weaviate_url)
    
    try:
        query = client.query.get(request.className, request.properties or [])
        
        if request.queryType == "vector":
            query = query.with_near_text({"concepts": [request.queryText]})
            if request.embeddingModel:
                pass # Weaviate client handles this if module is configured
        elif request.queryType == "keyword":
            query = query.with_bm25(query=request.queryText)
        elif request.queryType == "hybrid":
            query = query.with_hybrid(query=request.queryText, alpha=request.alpha)
            if request.embeddingModel:
                pass # Same as vector search, model handling depends on Weaviate module config
        
        if request.filter:
            query = query.with_where(request.filter)
            
        query = query.with_limit(request.limit).with_offset(request.offset)
        
        # Always request _additional properties for ID, distance, score
        query = query.with_additional(["id", "distance", "score"])

        result = query.do()
        
        # Weaviate returns data under 'data' -> 'Get' -> 'ClassName'
        # Extract the actual results
        class_data = result.get("data", {}).get("Get", {}).get(request.className, [])
        return class_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute query: {e}")
