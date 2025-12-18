from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import pathlib

# --- Project Setup & Configuration ---
BASE = pathlib.Path(__file__).parent
app = FastAPI()

# Mount static files (CSS, JS, Images) to be accessible via /static
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

# Initialize Jinja2 templates for rendering HTML files
templates = Jinja2Templates(directory=str(BASE / "templates"))

# --- Data Loading Utility ---
# Loads the artifact data from a JSON file into memory for quick access
artifacts_path = BASE / "data" / "artifacts.json"
ARTIFACTS = {}

if artifacts_path.exists():
    try:
        with open(artifacts_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Create a dictionary where the key is the slug for O(1) lookup
            ARTIFACTS = {a["slug"]: a for a in data}
    except Exception as e:
        print(f"Error loading artifacts.json: {e}")
else:
    print("WARNING: data/artifacts.json not found!")

# --- Application Routes ---

# Home Page: Displays the featured artifacts gallery
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "artifacts": list(ARTIFACTS.values())},
    )

# About Page: Explains the museum's vision
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# QR Scanner Page: Interactive camera interface
@app.get("/scan", response_class=HTMLResponse)
async def scan(request: Request):
    return templates.TemplateResponse("scan.html", {"request": request})

# Museum Building Page: Interactive 3D/Map view of the structure
@app.get("/museum", response_class=HTMLResponse)
async def museum(request: Request):
    return templates.TemplateResponse("museum.html", {"request": request})

# [NEW] Partners Page: For corporate lending and collaboration
@app.get("/partners", response_class=HTMLResponse)
async def partners(request: Request):
    return templates.TemplateResponse("partners.html", {"request": request})

# [NEW] Café Page: Rooftop menu and atmosphere
@app.get("/cafe", response_class=HTMLResponse)
async def cafe(request: Request):
    return templates.TemplateResponse("cafe.html", {"request": request})

# [NEW] Events Page: Workshops and cultural activities
@app.get("/events", response_class=HTMLResponse)
async def events(request: Request):
    return templates.TemplateResponse("events.html", {"request": request})

# Artifact Detail Page: Shows specific artwork details and audio player
@app.get("/artifact/{slug}", response_class=HTMLResponse)
async def artifact_page(request: Request, slug: str):
    a = ARTIFACTS.get(slug)
    if not a:
        # Redirect to home if slug not found
        return RedirectResponse("/")

    return templates.TemplateResponse(
        "artifact.html",
        {
            "request": request,
            "slug": slug,
            "img": a["image"],
            "title": a["title"],
            "desc": a["description"],
            "artist": a["artist"],
            "lender": a["lender"],
        },
    )

# Edit Page: Canvas editor for remixing artworks
@app.get("/artifact/{slug}/edit", response_class=HTMLResponse)
async def edit_page(request: Request, slug: str):
    a = ARTIFACTS.get(slug)
    if not a:
        return RedirectResponse("/")

    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "slug": slug,
            "original_img": a["image"],
        },
    )