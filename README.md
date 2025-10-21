## eCourtScraper – Delhi eCourts Cause List Scraper

Lightweight FastAPI backend with a static HTML/JS frontend to discover and export daily cause lists from Delhi District Courts. The backend talks to official eCourts endpoints and the New Delhi District Courts site, normalizes the responses, and the frontend offers a small UI to step through State → District → Court Complex → Establishment → Court Name and fetch the cause list for a given date.

### Repository layout

```
Think Act Rise Foundation/
├─ eCourtScraper/           # FastAPI backend
│  ├─ main.py               # API routes and scraping logic
│  ├─ config/db.py          # SQLModel engine and table bootstrap
│  └─ models/model.py       # SQLModel models (e.g., statecodes)
├─ eCourtScraperUi/         # Static frontend (open in browser)
│  ├─ index.html            # State->District->Complex->Establishment->Court flow
│  ├─ script.js             # Calls backend endpoints to populate selects
│  ├─ causelist.html        # CAPTCHA + court selection + submit
│  ├─ causelist.js          # Calls backend to fetch individual cause lists
│  └─ style.css             # Styles
└─ requirements.txt         # Python dependencies
```

### Prerequisites

- Python 3.13
- wkhtmltopdf (required by `pdfkit` for HTML→PDF conversion)
  - Windows: download and install `wkhtmltopdf` and ensure `wkhtmltopdf.exe` is on PATH.
- A database accessible via SQLAlchemy URI (e.g., PostgreSQL) for `SQLModel` metadata creation.

### Quick start (Windows / PowerShell)

1) Clone and enter the project directory.

2) Create and activate a virtual environment (or use the existing one in `eCourtScraperEnv`).

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3) Install dependencies.

```powershell
pip install -r requirements.txt
```

4) Configure environment variables.

Create a file `eCourtScraper/.env` with at least:

```env
DB_URI=postgresql+psycopg2://user:password@localhost:5432/your_db
```

5) Ensure `wkhtmltopdf` is installed and available on PATH.

6) Run the backend API.

```powershell
cd eCourtScraper
python main.py
```

By default the app starts Uvicorn on `http://127.0.0.1:60`.

7) Open the frontend.

- For the guided dropdown flow, open `eCourtScraperUi/index.html` in your browser.
- For the CAPTCHA + cause-list fetch flow, open `eCourtScraperUi/causelist.html`.

Note: The frontend files directly call the backend at `http://127.0.0.1:60`. CORS is enabled for development.

### Environment and database

`eCourtScraper/config/db.py` loads `DB_URI` from `eCourtScraper/.env` and initializes a `SQLModel` engine. On start, `create_table()` will create metadata tables (e.g., `statecodes`). Provide a valid SQLAlchemy URL (PostgreSQL, SQLite, etc.). Example (SQLite file):

```env
DB_URI=sqlite:///./ecourt.db
```

### API endpoints (backend)

Base URL: `http://127.0.0.1:60`

- GET `/fetchingstates`
  - Returns states from the local database (`statecodes`).

- GET `/fetchingdistricts/{statecode}`
  - Scrapes eCourts to return districts for the selected state.

- GET `/fetchingCourtComplex/{statecode}/{districtcode}`
  - Scrapes eCourts to return court complexes.

- GET `/fetchingCourtEstablishment/{statecode}/{districtcode}/{complexcode}`
  - Scrapes eCourts to return court establishments.

- GET `/fetchingCourtNames/{statecode}/{districtcode}/{complexcode}`
  - Scrapes eCourts to return court names available for cause lists.

- GET `/creatingSession`
  - Initializes a session against the New Delhi District Courts cause-list page and returns the CAPTCHA image URL. The frontend must call this first to obtain and display the CAPTCHA.

- GET `/gettingCourtNames/{civcri}`
  - Returns available court names for a given cause type.
  - Path parameter `civcri`: `2` for Civil, `3` for Criminal.

- GET `/fetchingEachCauseList/{courtName}/{date}/{civcri}/{captcha}/{count}`
  - Fetches cause list HTML for a court and date, validates the CAPTCHA, and saves both HTML and a PDF to a desktop folder (`C:/Users/<user>/OneDrive/Desktop/imagesandhtml/`).
  - Path parameters:
    - `courtName`: court code from the dropdown
    - `date`: `DD-MM-YYYY` (frontend transforms from `YYYY-MM-DD`)
    - `civcri`: `2` (Civil) or `3` (Criminal)
    - `captcha`: user-entered CAPTCHA string
    - `count`: sequential number used in output filenames

### Frontend usage

Flow 1 – discovery (no CAPTCHA):
- Open `eCourtScraperUi/index.html` and proceed through State → District → Court Complex → Establishment → Court Name. Each selection calls the corresponding backend endpoint to populate the next select.

Flow 2 – cause list fetch (with CAPTCHA):
- Open `eCourtScraperUi/causelist.html`.
- On load, it calls `/creatingSession` to retrieve and show the CAPTCHA image.
- Choose court complex, case type (Civil/Criminal), date, select a court, enter CAPTCHA, and click Submit.
- The backend saves HTML and a PDF to `C:/Users/<your-user>/OneDrive/Desktop/imagesandhtml/page{N}.html|.pdf`.

### Notes and caveats

- Respect the target sites' Terms of Use. This project is for educational and internal use only.
- The backend currently allows all CORS origins for local development. Tighten this for production.
- `pdfkit` requires `wkhtmltopdf`. If PDF generation fails, verify installation and PATH.
- Output paths in `main.py` are Windows-specific and absolute. Adjust paths if you run on a different machine or want outputs inside the repo.

### Troubleshooting

- Import/engine errors on start: verify `DB_URI` in `eCourtScraper/.env` and that your database is reachable.
- CAPTCHA always failing: ensure you call `/creatingSession` before submitting; refresh the session to get a new CAPTCHA.
- CORS errors in browser: confirm the backend is running on `127.0.0.1:60` and that you are opening the HTML files locally (or serve them via a simple file server). CORS is already enabled with `allow_origins=["*"]` for dev.
- PDF not generated: install `wkhtmltopdf`, confirm it’s on PATH, and that the output folder exists.

### License

No license file is included. Add one if you plan to distribute.


