# AI Data Analyst Assistant

An MVP that lets you upload CSV/XLSX files, explore dataset summaries, generate automatic charts, and get AI-powered insights via Google Gemini.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + TypeScript + Vite |
| Backend | FastAPI |
| Data | Pandas |
| Charts | Plotly |
| AI | Google Gemini API |

## Project Structure

```
AI_DATA_ANALYST/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Environment settings
│   │   ├── routers/           # API route handlers
│   │   ├── services/            # Business logic
│   │   ├── models/              # Pydantic schemas
│   │   └── utils/               # Helpers
│   ├── uploads/                 # Uploaded datasets (gitignored)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # UI components
│   │   ├── pages/               # Page views
│   │   ├── services/            # API client
│   │   ├── types/               # TypeScript types
│   │   └── styles/              # Global CSS
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # Add your GEMINI_API_KEY
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — the dev server proxies API calls to port 8000.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload CSV or XLSX file |
| GET | `/api/datasets/{id}/summary` | Dataset summary & stats |
| GET | `/api/datasets/{id}/charts` | Auto-generated Plotly charts |
| POST | `/api/datasets/{id}/insights` | Gemini AI insights |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes (for insights) | Google AI Studio API key |
| `UPLOAD_DIR` | No | Upload storage path (default: `uploads`) |
| `MAX_UPLOAD_MB` | No | Max file size in MB (default: 50) |
