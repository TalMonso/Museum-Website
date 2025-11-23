from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json, pathlib, uuid
from PIL import Image
import torch
import cv2
import numpy as np
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from controlnet_aux import CannyDetector


# Base paths
BASE = pathlib.Path(__file__).parent
app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE / "templates"))


# Load artifacts
with open(BASE / "data" / "artifacts.json", "r", encoding="utf-8") as f:
    ARTIFACTS = {a["slug"]: a for a in json.load(f)}


# Device selection (MPS for Mac)
device = "mps" if torch.backends.mps.is_available() else "cpu"
dtype = torch.float16 if device != "cpu" else torch.float32

print("Using device:", device)


# Load ControlNet Canny + SD 1.5
print("Loading ControlNet Canny model...")

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=dtype
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=dtype
)

pipe = pipe.to(device)
pipe.enable_attention_slicing()

# Canny detector (for line extraction)
canny = CannyDetector()


# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "artifacts": list(ARTIFACTS.values())},
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/scan", response_class=HTMLResponse)
async def scan(request: Request):
    return templates.TemplateResponse("scan.html", {"request": request})


@app.get("/artifact/{slug}", response_class=HTMLResponse)
async def artifact_page(request: Request, slug: str):
    a = ARTIFACTS.get(slug)
    if not a:
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


# Edit page
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
            "result_img": None,
        },
    )


@app.post("/artifact/{slug}/edit", response_class=HTMLResponse)
async def edit_process(request: Request, slug: str, prompt: str = Form(...)):
    a = ARTIFACTS.get(slug)
    if not a:
        return RedirectResponse("/")

    # Load the image
    img_path = a["image"].lstrip("/")
    full_path = BASE / img_path

    init_image = Image.open(full_path).convert("RGB")
    init_image = init_image.resize((512, 512))

    # Load SD 1.5 img2img (safe mode)
    from diffusers import StableDiffusionImg2ImgPipeline

    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float32  # floats fix black images
    ).to(device)

    result = pipe(
        prompt=prompt,
        image=init_image,
        strength=0.35,        # low change, keeps original image
        guidance_scale=12.0,   # strong text influence
        num_inference_steps=35,
    ).images[0]

    # Save the output
    output_dir = BASE / "static" / "edits"
    output_dir.mkdir(exist_ok=True)

    filename = f"{slug}_{uuid.uuid4().hex}.png"
    save_path = output_dir / filename
    result.save(save_path)

    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "slug": slug,
            "original_img": a["image"],
            "result_img": f"/static/edits/{filename}",
        },
    )

