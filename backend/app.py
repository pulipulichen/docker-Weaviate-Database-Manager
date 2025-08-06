from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import weaviate
import os
import json

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:8080", # For frontend running on 8080 if not proxied
    "http://localhost:3000", # Common for Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to get Weaviate client
def get_weaviate_client(weaviate_url: str):
    try:
        client = weaviate.Client(url=weaviate_url)
        client.is_ready() # Check connection
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Weaviate: {e}")

@app.get("/api/schema")
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

@app.post("/api/query")
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
                # This part might need adjustment based on how the specific Weaviate module
                # handles targetVector or model selection.
                # For example, if using text2vec-openai, you might need to pass model in the nearText object
                # or configure the module in Weaviate itself.
                # For now, we'll assume default behavior or that the model is configured on Weaviate side.
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

class UpdateObjectRequest(BaseModel):
    weaviate_url: str
    className: str
    id: str
    propertyName: str
    value: Any

@app.patch("/api/object")
async def update_object_property(request: UpdateObjectRequest):
    """
    修改 Weaviate 中單一物件的指定屬性。
    """
    client = get_weaviate_client(request.weaviate_url)
    
    try:
        # Construct the properties dictionary for update
        properties_to_update = {request.propertyName: request.value}
        
        client.data_object.update(
            data_object=properties_to_update,
            class_name=request.className,
            uuid=request.id
        )
        return {"status": "success", "message": f"Object {request.id} property {request.propertyName} updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update object property: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
