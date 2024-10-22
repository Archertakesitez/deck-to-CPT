from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import uvicorn

app = FastAPI()

# Directory where uploaded PDFs will be saved
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Set up Jinja2 template rendering
templates = Jinja2Templates(directory="templates")

# Serve static files (e.g., CSS) from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Route to render the drag-and-drop page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Route to handle the PDF upload
@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Here we can call our custom PDF information extraction function or so...
    # For now, just return the filename as a success message
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
