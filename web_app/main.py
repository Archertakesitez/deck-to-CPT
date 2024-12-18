from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from LLM_matching.text_to_CPT import pdf_to_cpt
from LLM_matching.matching import find_relevant_cpt_codes_tfidf

UPLOAD_DIR = "uploads"
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
@app.post("/pdf_to_cpt/")
async def upload_pdf(
    file: UploadFile = File(...),
    company: str = Form(...),
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    corresponding_CPT = pdf_to_cpt(file=file_path, company=company)
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
    return {"CPT_codes": list(corresponding_CPT.items())}


@app.post("/find_relevant_cpt_tfidf/")
async def find_relevant_cpt_tfidf_handler(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    corresponding_CPT = find_relevant_cpt_codes_tfidf(file=file_path)
    print(corresponding_CPT)
    os.remove(file_path)  # Clean up file after processing
    return {"CPT_codes": list(corresponding_CPT.items())}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
