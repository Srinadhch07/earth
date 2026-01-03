from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.scrapers.google_scraper import scrape_jobs_google
from app.scrapers.platform_scraper import scrape_jobs_platform
from app.core.config import SERPAPI_KEY, DATA_DIR

app = FastAPI(title="Job Scraper")

templates = Jinja2Templates(directory="templates")
Path(DATA_DIR).mkdir(exist_ok=True)

SUPPORT_MSG = (
    "We're currently unavailable now. "
    "If you like the idea drop mail to srinadhc07@gmail.com"
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/google", response_class=HTMLResponse)
def google_page(request: Request):
    return templates.TemplateResponse("google_scraper.html", {"request": request})


@app.get("/platform", response_class=HTMLResponse)
def platform_page(request: Request):
    return templates.TemplateResponse("platform_scraper.html", {"request": request})



@app.post("/scrape/google")
def scrape_google_ui(
    query: str = Form(...),
    location: str = Form(...),
    hl: str = Form("en"),
    gl: str = Form("in"),
    device: str = Form("desktop"),
    output_csv: str = Form("google_jobs.csv"),
):
    output_path = f"{DATA_DIR}/{output_csv}"

    csv_file = scrape_jobs_google(
        api_key=SERPAPI_KEY,
        query=query,
        location=location,
        hl=hl,
        gl=gl,
        device=device,
        output_csv=output_path,
    )

    if not csv_file:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": SUPPORT_MSG},
        )

    return {
        "status": "success",
        "message": "successful",
        "download_url": f"/download/{output_csv}",
    }


@app.post("/scrape/platform")
def scrape_platform_ui(
    search_term: str = Form(...),
    location: str = Form(...),
    results_wanted: int = Form(20),
    hours_old: int = Form(72),
    google_search_term: str | None = Form(None),
    linkedin_fetch_description: bool = Form(True),
    output_csv: str = Form("platform_jobs.csv"),
):
    output_path = f"{DATA_DIR}/{output_csv}"

    csv_file = scrape_jobs_platform(
        site_names=["indeed", "linkedin", "zip_recruiter", "google"],
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
        google_search_term=google_search_term,
        linkedin_fetch_description=linkedin_fetch_description,
        output_csv=output_path,
    )

    if not csv_file:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": SUPPORT_MSG},
        )

    return {
        "status": "success",
        "message": "Successful",
        "download_url": f"/download/{output_csv}",
    }


@app.get("/download/{filename}")
def download_csv(filename: str):
    return FileResponse(
        f"{DATA_DIR}/{filename}",
        filename=filename,
        media_type="text/csv",
    )
