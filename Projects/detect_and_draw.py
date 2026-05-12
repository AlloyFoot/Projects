import os, io, time, random, requests, mimetypes
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from config import HF_API_KEY
MODEL = "facebook/detr-resnet-101"
API = f"https://router.huggingface.co/hf-inference/models/{MODEL}"
ALLOWED, MAX_MB = {".jpg",".jpeg",".png",".bmp",".gif",".webp",".tiff"}, 8
EMOJI = {"person":"🧍","car":"🚗","truck":"🚚","bus":"🚌","bicycle":"🚲","motorcycle":"🏍️","dog":"🐶","cat":"🐱",
    "bird":"🐦","horse":"🐴","sheep":"🐑","cow":"🐮","bear":"🐻","giraffe":"🦒","zebra":"🦓","banana":"🍌",
    "apple":"🍎","orange":"🍊","pizza":"🍕","broccoli":"🥦","book":"📘","laptop":"💻","tv":"📺","bottle":"🧴","cup":"🥤"}

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

MAX_TRIES = 8
SLEEP_WHEN_BUSY = 2.0 
TIMEOUT = 60  

def font(sz=18):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size=sz)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size=sz)
        except Exception:
            return ImageFont.load_default()

def ask_image():
    while True:
        p = input("Enter path to image: ").strip().strip('"').strip("'")
        if not os.path.isfile(p):
            print("File not found, try again.")
            continue
        ext = os.path.splitext(p)[1].lower()
        if ext not in ALLOWED:
            print(f"Unsupported extension '{ext}'. Allowed: {', '.join(sorted(ALLOWED))}")
            continue
        size_mb = os.path.getsize(p) / (1024*1024)
        if size_mb > MAX_MB:
            print(f"File too large ({size_mb:.2f} MB). Max is {MAX_MB} MB.")
            continue
        try:
            with Image.open(p) as im:
                im.verify()
        except Exception:
            print("Image appears corrupted or unreadable. Try another file.")
            continue
        return p
    
def detect_mime(path):
    ext = os.path.splitext(path)[1].lower()
    m = mimetypes.types_map.get(ext)
    if m:
        return m
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    return "application/octet-stream"

def infer(path, img_bytes, tries=MAX_TRIES):
    mime = detect_mime(path)
    attempt = 0
    while attempt < tries:
        attempt += 1
        try:
            headers = HEADERS.copy()
            headers["Content-Type"] = mime
            resp = requests.post(API, headers=headers, data=img_bytes, timeout=TIMEOUT)
        except requests.Timeout:
            print(f"Request timed out (attempt {attempt}/{tries}). Retrying...")
            time.sleep(1 + random.random())
            continue
        except requests.ConnectionError as e:
            print(f"Connection error (attempt {attempt}/{tries}): {e}. Retrying...")
            time.sleep(1 + random.random())
            continue

        if resp.status_code == 200:
            try:
                j = resp.json()
            except Exception as e:
                raise RuntimeError(f"Failed to decode JSON response: {e}. Raw: {resp.text}")
            if isinstance(j, dict) and j.get("error"):
                raise RuntimeError(f"Hugging Face error: {j.get('error')}")
            if isinstance(j, dict) and "data" in j and isinstance(j["data"], list):
                return j["data"]
            if not isinstance(j, list):
                raise RuntimeError(f"Unexpected response format from HF: {type(j)}")
            return j

        if resp.status_code == 503:
            print(f"Model busy/warming up (503). Waiting {SLEEP_WHEN_BUSY}s and retrying... ({attempt}/{tries})")
            time.sleep(SLEEP_WHEN_BUSY)
            continue

        if resp.status_code in (429, 500, 502, 504):
            backoff = min(4 + attempt * 2, 30)
            print(f"Transient error {resp.status_code}. Sleeping {backoff}s and retrying... ({attempt}/{tries})")
            time.sleep(backoff)
            continue

        try:
            err = resp.json()
        except Exception:
            err = resp.text
        raise RuntimeError(f"HF API returned status {resp.status_code}: {err}")

    raise TimeoutError(f"Model did not respond successfully after {tries} attempts.")

def draw(img: Image.Image, dets, thr=0.5):
    drawer = ImageDraw.Draw(img)
    fnt = font(sz=max(14, img.width // 60))
    counts = {}

    candidates = dets[:50] if isinstance(dets, list) else []
    for det in candidates:
        score = None
        if isinstance(det, dict):
            score = det.get("score") or det.get("confidence") or det.get("probability")
        if score is None:
            score_f = 1.0
        else:
            try:
                score_f = float(score)
            except Exception:
                score_f = 0.0
        if score_f < thr:
            continue

        label = det.get("label") or det.get("class") or det.get("name") or "object"

        box = det.get("box") or det.get("bbox") or det.get("box_coords") or det.get("boxes")
        coords = None
        if isinstance(box, dict):
            xmin = box.get("xmin") or box.get("x") or box.get("left")
            ymin = box.get("ymin") or box.get("y") or box.get("top")
            xmax = box.get("xmax") or box.get("x2")
            ymax = box.get("ymax") or box.get("y2")
            if xmax is None and box.get("width") is not None and xmin is not None:
                xmax = xmin + box.get("width")
            if ymax is None and box.get("height") is not None and ymin is not None:
                ymax = ymin + box.get("height")
            coords = [xmin, ymin, xmax, ymax]
        elif isinstance(box, (list, tuple)) and len(box) == 4:
            coords = list(box)
        else:
            alt = det.get("bbox")
            if isinstance(alt, (list, tuple)) and len(alt) == 4:
                coords = list(alt)

        if not coords:
            continue

        try:
            coords = [float(c) for c in coords]
        except Exception:
            continue

        x1, y1, x2, y2 = coords

        if 0.0 <= x1 <= 1.0 and 0.0 <= x2 <= 1.0 and 0.0 <= y1 <= 1.0 and 0.0 <= y2 <= 1.0:
            x1 *= img.width
            x2 *= img.width
            y1 *= img.height
            y2 *= img.height


        if x2 < x1 or y2 < y1:
            w = x2
            h = y2
            x2 = x1 + w
            y2 = y1 + h

        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(img.width, x2), min(img.height, y2)

        color = tuple(random.choices(range(30, 230), k=3))
        thickness = max(2, int(min(img.width, img.height) / 200))

        for t in range(thickness):
            drawer.rectangle([x1 - t, y1 - t, x2 + t, y2 + t], outline=color)

        emoji = EMOJI.get(label, "")
        text = f"{emoji} {label} {int(score_f*100)}%".strip()

        try:
            bbox = fnt.getbbox(text)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        except Exception:
            try:
                text_w, text_h = fnt.getsize(text)
            except Exception:
                text_w, text_h = (len(text) * 7, max(12, int(fnt.size if hasattr(fnt, "size") else 12)))

        text_x = x1
        text_y = y1 - text_h - 6
        if text_y < 0:
            text_y = y1 + 6
        bg = (color[0], color[1], color[2], 200) if img.mode.endswith("A") else color
        drawer.rectangle([text_x, text_y, text_x + text_w + 6, text_y + text_h + 4], fill=bg)
        drawer.text((text_x + 3, text_y + 2), text, fill=(255, 255, 255), font=fnt)

        counts[label] = counts.get(label, 0) + 1

    return counts


def main():
    print("Object detection with DETR (Hugging Face).")
    image_path = ask_image()  

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    try:
        detections = infer(image_path, img_bytes) 
    except Exception as e:
        print("API error:", e)
        return

    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except Exception as e:
        print("Failed to open image in PIL:", e)
        return

    counts = draw(img, detections, thr=0.5)

    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    base = os.path.splitext(os.path.basename(image_path))[0]
    out_name = f"{base}_annotated_{stamp}.jpg"

    try:
        img.save(out_name, quality=92)
        print(f"Annotated image saved to: {out_name}")
    except Exception as e:
        print("Failed to save annotated image:", e)
        return

    if counts:
        print("Detected objects:")
        for k, v in counts.items():
            emo = EMOJI.get(k, "")
            print(f"  {emo} {k}: {v}")
    else:
        print("No objects detected with confidence >= 50%. Try a clearer image or lower threshold.")

    print("Note: AI detections may be incorrect or incomplete. Use results as guidance only.")

if __name__ == "__main__":
    main()