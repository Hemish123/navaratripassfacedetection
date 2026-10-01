# 🪔 Navratri Face Pass — Verification System

Secure Navratri event entry using face recognition. Customers register their face via a unique link; security guards verify identity at the gate with a phone camera.

## Architecture

```
Customer receives unique link → /p/<token>/
    ↓
Uploads face photo + pass photo → Face embedding stored
    ↓
At the gate → /gate/?key=<GATE_KEY>
    ↓
Guard captures visitor's face → Matched against all registered embeddings
    ↓
Result: MATCH (green) / NO MATCH (red) / REVIEW (blue)
```

**Stack:** Django 4.2+ · InsightFace (ArcFace) · NumPy · OpenCV · Azure Blob (optional) · PostgreSQL / SQLite

---

## Quick Start (Local Development)

### 1. Clone & Setup

```bash
cd navratri_face_pass
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env — the defaults work for local dev (SQLite, local media)
```

### 3. Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Create Demo Passes

```bash
python manage.py create_demo_pass --count 5
# Outputs pass numbers and registration links
```

### 5. Run Server

```bash
python manage.py collectstatic --noinput
python manage.py runserver
```

### 6. Test the Flow

1. Open a registration link from the demo output: `http://localhost:8000/p/<token>/`
2. Fill in name, mobile, upload a face photo and pass photo, consent → Submit
3. Open the gate: `http://localhost:8000/gate/?key=change-me-in-production`
4. Capture/upload a face → See match result

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `True` | Django debug mode |
| `SECRET_KEY` | insecure default | **Change in production** |
| `DATABASE_URL` | (empty = SQLite) | PostgreSQL connection string |
| `REDIS_URL` | (empty = LocMem) | Redis URL for cache |
| `GATE_KEY` | `change-me-in-production` | Secret key for gate access |
| `GATE_MAX_ENTRIES_PER_DAY` | `1` | Max entries per pass per day |
| `FACE_MATCH_THRESHOLD` | `0.45` | Cosine similarity for MATCH |
| `FACE_REVIEW_THRESHOLD` | `0.35` | Cosine similarity for REVIEW |
| `FACE_MODEL_PACK` | `buffalo_l` | InsightFace model pack |
| `FACE_USE_GPU` | `False` | Use CUDA for face detection |
| `AZURE_STORAGE_CONNECTION_STRING` | (empty) | Azure Blob connection |
| `AZURE_OPENAI_ENDPOINT` | (empty) | Azure OpenAI for pass OCR |
| `AZURE_OPENAI_API_KEY` | (empty) | Azure OpenAI API key |

See `.env.example` for the full list.

---

## Production Setup

### PostgreSQL

```bash
DATABASE_URL=postgres://user:password@host:5432/navratri_face_pass
```

### Azure Blob Storage

```bash
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER=navratri-passes
```

Photos are stored in a **private** container. URLs are short-lived SAS tokens (10 min default).

### Running with Gunicorn

```bash
gunicorn saleswithai.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --worker-class gthread \
    --timeout 120
```

> **Note:** The InsightFace model loads once per worker process (~1-2 GB RAM per worker). Plan capacity accordingly.

### Redis Cache (recommended for multi-worker)

```bash
REDIS_URL=redis://localhost:6379/0
```

Redis keeps the embedding cache version in sync across multiple Gunicorn workers.

---

## Face Matching — How It Works

1. **Registration:** InsightFace detects the face, extracts a 512-dimensional embedding (ArcFace), L2-normalises it, and stores it as raw bytes.

2. **Gate scan:** The visitor's face embedding is computed, then compared against ALL registered embeddings using a single matrix dot product (cosine similarity).

3. **Classification:**
   - `score >= 0.45` → **MATCHED** (green)
   - `score >= 0.35` → **REVIEW** (blue, show top-3 candidates)
   - `score < 0.35`  → **NO MATCH** (red)

### Tuning Thresholds

- **Lower `FACE_MATCH_THRESHOLD`** (e.g., 0.40) → fewer false rejections, more false accepts
- **Raise `FACE_MATCH_THRESHOLD`** (e.g., 0.50) → stricter, may reject legitimate visitors
- Test with your actual gate photos before going live

---

## Management Commands

| Command | Description |
|---------|-------------|
| `create_demo_pass --count N` | Create N passes with sequential numbers |
| `create_demo_pass --csv file.csv` | Export passes to CSV |
| `rebuild_embeddings` | Validate and rebuild embedding cache |
| `purge_event_data --confirm` | Delete all face data after the event |
| `purge_event_data --dry-run` | Show what would be deleted |

---

## Admin Panel

Access at `/admin/` with your superuser account:

- **Passes:** Search, filter by status, bulk-generate 50 passes, export CSV, block/reset
- **Registrations:** View photos, search by name/mobile/pass number, flag for review
- **Entry Logs:** Filter by result/date, export CSV

---

## Testing

```bash
python manage.py test passes
```

Tests mock InsightFace and Azure OpenAI so they run without models or API keys.

---

## Security & Privacy

- **No login required** — registration is token-gated, gate uses a secret key
- **Face embeddings** are mathematical representations, not images
- **Photos** are stored in private Azure Blob containers (never publicly accessible)
- **EXIF metadata** is stripped from all uploads
- **Rate limiting** on gate and registration endpoints (django-ratelimit)
- **Consent** is required before storing face data
- **Purge command** deletes all data after the event
- **Atomic transactions** with `select_for_update` prevent race conditions

---

## Project Structure

```
passes/
├── models.py           # Pass, Registration, EntryLog
├── views.py            # Registration + gate endpoints
├── forms.py            # RegistrationForm with image validation
├── urls.py             # URL routing
├── admin.py            # Admin with CSV export, photo previews
├── services/
│   ├── face_engine.py  # InsightFace singleton, embedding, matching
│   ├── pass_reader.py  # QR / OCR / Azure OpenAI pass number extraction
│   └── storage.py      # Azure Blob / local file storage
├── templates/passes/   # Django templates (Navratri theme)
├── static/passes/      # CSS + camera.js
├── management/commands/ # create_demo_pass, rebuild_embeddings, purge_event_data
└── tests/              # Unit tests (models, face engine, pass reader, views, matching)
```
