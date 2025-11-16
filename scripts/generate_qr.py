import qrcode, json, pathlib
BASE = pathlib.Path(__file__).resolve().parents[1]
with open(BASE / 'app' / 'data' / 'artifacts.json', 'r', encoding='utf-8') as f:
    arts = json.load(f)
qr_dir = BASE / 'qr_codes'; qr_dir.mkdir(exist_ok=True)
for a in arts:
    url = f"http://localhost:8000/artifact/{a['slug']}"
    img = qrcode.make(url)
    img.save(qr_dir / f"{a['slug']}.png")
print('QRs generated in', qr_dir)