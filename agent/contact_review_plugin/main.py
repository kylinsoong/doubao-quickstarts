from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid

app = FastAPI()

# In-memory results
results_store = {}


class FileURLRequest(BaseModel):
    file_url: str  # the URL of the file to be processed


@app.post("/send_file_url")
async def send_file_url(body: FileURLRequest):
    """Receive a file URL and store processing info."""
    file_id = str(uuid.uuid4())

    # Simulate file URL handling
    results_store[file_id] = {
        "file_url": body.file_url,
        "status": "received"
    }

    return JSONResponse(content={
        "result": {
            "file_id": file_id,
            "message": "File URL received successfully."
        }
    })


@app.get("/get_rules")
async def get_rules():
    """Return configuration or rule details."""
    rules = {
        "accepted_input": "file_url",
        "url_protocols": ["http", "https"],
        "processing_mode": "async"
    }
    return JSONResponse(content={"result": rules})


@app.get("/get_results/{file_id}")
async def get_results(file_id: str):
    """Return result or status by file_id."""
    result = results_store.get(file_id)
    if not result:
        return JSONResponse(status_code=404, content={"result": {"error": "File ID not found"}})
    return JSONResponse(content={"result": result})

