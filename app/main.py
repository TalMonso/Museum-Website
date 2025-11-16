from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json, pathlib


# 1) הגדרת בסיס הפרויקט
BASE = pathlib.Path(__file__).parent
app = FastAPI()


# 2) סטטיק ותבניות
app.mount('/static', StaticFiles(directory=BASE / 'static'), name='static')
templates = Jinja2Templates(directory=str(BASE / 'templates'))


# 3) טעינת הנתונים (אנגלית בלבד בשלב זה)
with open(BASE / 'data' / 'artifacts.json', 'r', encoding='utf-8') as f:
    ARTIFACTS = {a['slug']: a for a in json.load(f)}


# 4) ראוטים
@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    # נשמור על סדר כפי שמופיע ב-JSON
    artifacts_list = list(ARTIFACTS.values())
    return templates.TemplateResponse('home.html', {
        'request': request,
        'artifacts': artifacts_list
    })


@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})


@app.get('/scan', response_class=HTMLResponse)
async def scan(request: Request):
    return templates.TemplateResponse('scan.html', {'request': request})


@app.get('/artifact/{slug}', response_class=HTMLResponse)
async def artifact(request: Request, slug: str):
    a = ARTIFACTS.get(slug)
    if not a:
        return RedirectResponse('/')
    return templates.TemplateResponse('artifact.html', {
        'request': request,
        'slug': slug,
        'img': a['image'],
        'title': a['title'],
        'desc': a['description'],
        'artist': a['artist'],
        'lender': a['lender'],
    })