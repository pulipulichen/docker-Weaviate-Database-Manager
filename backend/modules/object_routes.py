from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from .weaviate_client import get_weaviate_client

router = APIRouter()

class UpdateObjectRequest(BaseModel):
    weaviate_url: str
    className: str
    id: str
    propertyName: str
    value: Any

@router.patch("/object")
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
