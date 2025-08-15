
# HH Job Market Analysis

A professional CRM interface for analyzing CAD job markets across different countries using HeadHunter API.

## Features

- **Multi-country search**: Kazakhstan, Russia, Ukraine, Belarus, and more
- **CAD product detection**: AutoCAD, Revit, Inventor, Fusion 360, Civil 3D, etc.
- **Company analytics**: Total jobs, CAD jobs, contact information
- **Excel-like interface**: Sortable, filterable, collapsible company groups
- **Export functionality**: CSV export for further analysis
- **Comprehensive search**: Up to 10,000 jobs per keyword

## Quick Deploy Options

### Option 1: Railway (Recommended - Free)

1. **Fork/Clone** this repository to your GitHub
2. Go to [Railway.app](https://railway.app)
3. **Sign up** with GitHub
4. Click **"New Project"** → **"Deploy from GitHub repo"**
5. Select your repository
6. Railway will automatically detect and deploy
7. Get your **public URL** instantly

### Option 2: Render (Free Tier)

1. **Fork/Clone** this repository to your GitHub
2. Go to [Render.com](https://render.com)
3. **Sign up** with GitHub
4. Click **"New +"** → **"Web Service"**
5. Connect your GitHub repository
6. Set **Build Command**: `pip install -r requirements.txt`
7. Set **Start Command**: `python app.py`
8. Deploy and get your **public URL**

### Option 3: Heroku (Paid)

1. **Fork/Clone** this repository to your GitHub
2. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Run commands:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

### Option 4: Python Anywhere (Free)

1. **Fork/Clone** this repository to your GitHub
2. Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
3. **Sign up** for free account
4. Go to **"Web"** tab → **"Add a new web app"**
5. Choose **"Flask"** framework
6. Upload your files
7. Set **WSGI configuration** to point to your app
8. Get your **public URL**

## Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd hh-kz-cad-jobs

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Access at http://localhost:8080
```

## Environment Variables

- `PORT`: Port number (default: 8080)
- `ENVIRONMENT`: Set to "production" to disable auto-reload

## API Endpoints

- `GET /`: Main web interface
- `GET /jobs`: Job search API
  - `keywords`: List of search keywords
  - `country`: Country to search in
  - `pages`: Number of pages to search
  - `per_page`: Results per page

## Usage

1. **Select Country**: Choose from dropdown (Kazakhstan, Russia, etc.)
2. **Enter Keywords**: CAD products like "AutoCAD, Revit, Inventor"
3. **Set Parameters**: Pages and results per page
4. **Search**: Click "Search Jobs" button
5. **Analyze**: View results in sortable table
6. **Export**: Download CSV for further analysis

## Search Capabilities

- **Comprehensive Search**: Up to 100 pages × 100 results per keyword
- **Total Capacity**: Up to 10,000 jobs per keyword
- **Multi-keyword**: Searches each keyword individually and combines results
- **Smart Pagination**: Automatically stops when no more results available

## Technologies

- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS, JavaScript
- **API**: HeadHunter (api.hh.ru)
- **Templates**: Jinja2

## License

MIT License
