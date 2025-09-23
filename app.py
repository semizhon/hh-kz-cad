# app.py - Clean version for Railway deployment
import os, time, requests, json
import hashlib
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Optional
from typing import List, Dict, Any
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio

HH_API = "https://api.hh.ru"
# Use your email in UA to be a good API citizen (optional but recommended)
UA = os.environ.get("HH_USER_AGENT", "HH-KZ-CAD-Jobs/1.0 (mumble_subject_0a@icloud.com)")
KEYWORDS_DEFAULT = ["AutoCAD, Revit, Civil 3D, Inventor, Fusion 360, Navisworks, BIM, Autodesk, Advance Steel, PowerMill, FeatureCAM"]

# Create FastAPI app - NO LIFESPAN PARAMETER
app = FastAPI(title="HH KZ CAD Jobs API", version="1.0.0")

# Setup templates
templates = Jinja2Templates(directory="templates")

# --- tiny TTL cache to be friendly to hh.ru ---
_cache: Dict[str, Any] = {}
def cache_get(key, ttl_sec=180):
    v = _cache.get(key)
    if not v: return None
    if time.time() - v["ts"] > ttl_sec:
        del _cache[key]
        return None
    return v["data"]

def cache_set(key, data):
    _cache[key] = {"ts": time.time(), "data": data}

# --- standard search cache ---
STANDARD_CACHE_DIR = Path("standard_cache")
STANDARD_CACHE_DIR.mkdir(exist_ok=True)

def _standard_cache_path(country: str) -> Path:
    """Get the path for a standard cache file."""
    today = date.today().isoformat()
    return STANDARD_CACHE_DIR / f"standard_cache_{country}_{today}.json"

def read_standard_cache(country: str) -> Optional[Dict[str, Any]]:
    """Read standard cache data if it exists and is from today."""
    cache_path = _standard_cache_path(country)
    if not cache_path.exists():
        return None
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error reading standard cache for {country}: {e}")
        return None

def write_standard_cache(country: str, payload: Dict[str, Any]):
    """Write standard cache data to disk."""
    cache_path = _standard_cache_path(country)
    try:
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Standard cache written for {country}")
    except Exception as e:
        print(f"Error writing standard cache for {country}: {e}")

def is_standard_search(keywords: List[str], country: str, pages: int, per_page: int) -> bool:
    """Check if this is a standard search request."""
    # Standard searches are for specific keywords, countries, and page sizes
    standard_keywords = ["AutoCAD,Revit,Inventor,Fusion 360,Fusion,Advance Steel"]
    standard_countries = ["Kazakhstan", "Uzbekistan"]
    standard_pages = 100
    standard_per_page = 100
    
    return (keywords == standard_keywords and 
            country in standard_countries and 
            pages == standard_pages and 
            per_page == standard_per_page)

def get_area_id_for_country(country_name="Kazakhstan"):
    """Get area ID for a country from HH API."""
    # Hardcoded mapping for common countries
    country_mapping = {
        "Kazakhstan": "40",
        "Узбекистан": "97", 
        "Uzbekistan": "97",
        "Россия": "113",
        "Russia": "113",
        "Georgia": "28",
        "Грузия": "28",
        "Armenia": "13",
        "Армения": "13",
        "Azerbaijan": "9",
        "Азербайджан": "9",
        "Kyrgyzstan": "48",
        "Кыргызстан": "48",
        "Tajikistan": "86",
        "Таджикистан": "86",
        "Turkmenistan": "93",
        "Туркменистан": "93",
        "Belarus": "16",
        "Беларусь": "16",
        "Ukraine": "5",
        "Украина": "5",
        "Moldova": "62",
        "Молдова": "62"
    }
    
    if country_name in country_mapping:
        return country_mapping[country_name]
    
    # Fallback to API search
    try:
        response = requests.get(f"{HH_API}/areas", headers={"User-Agent": UA})
        if response.status_code == 200:
            areas = response.json()
            for area in areas:
                if area.get("name") == country_name:
                    return area.get("id")
    except Exception as e:
        print(f"Error fetching area ID for {country_name}: {e}")
    
    return None

def search_vacancies_in_kz(keywords: List[str], country: str = "Kazakhstan", pages: int = 5, per_page: int = 20, city_filter: str = None):
    """Search for vacancies in Kazakhstan/Uzbekistan with city filtering."""
    try:
        print(f"Searching for keywords: {keywords}")
        area_id = get_area_id_for_country(country)
        if not area_id:
            return {"error": f"Country '{country}' not found"}
        
        # Create cache key
        cache_key = f"search_{hashlib.md5(f'{keywords}_{country}_{pages}_{per_page}_{city_filter}'.encode()).hexdigest()}"
        cached_result = cache_get(cache_key, ttl_sec=300)  # 5 minute cache
        if cached_result:
            return cached_result
        
        all_vacancies = []
        
        for page in range(pages):
            params = {
                "text": " OR ".join(keywords),
                "area": area_id,
                "per_page": per_page,
                "page": page,
                "only_with_salary": False
            }
            
            try:
                response = requests.get(f"{HH_API}/vacancies", 
                                      params=params, 
                                      headers={"User-Agent": UA, "Accept": "application/json"},
                                      timeout=30)  # 30 second timeout
                
                if response.status_code == 200:
                    data = response.json()
                    vacancies = data.get("items", [])
                    
                    # Apply city filter if specified
                    if city_filter:
                        filtered_vacancies = []
                        for vacancy in vacancies:
                            # Check if city filter matches any part of the address
                            address = vacancy.get("address", {})
                            city = address.get("city", "")
                            if city_filter.lower() in city.lower():
                                filtered_vacancies.append(vacancy)
                        vacancies = filtered_vacancies
                    
                    all_vacancies.extend(vacancies)
                    
                    # If we got fewer results than requested, we've reached the end
                    if len(vacancies) < per_page:
                        break
                else:
                    print(f"Error fetching page {page}: {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"Exception on page {page}: {e}")
                break
    
        # Add city information to each vacancy
        for vacancy in all_vacancies:
            address = vacancy.get("address", {})
            vacancy["city"] = address.get("city", "Unknown")
        
        result = {
            "vacancies": all_vacancies,
            "total_found": len(all_vacancies),
            "country": country,
            "keywords": keywords,
            "pages_searched": pages,
            "per_page": per_page
        }
        
        cache_set(cache_key, result)
        return result
        
    except Exception as e:
        print(f"Error in search_vacancies_in_kz: {e}")
        return {"error": f"Search error: {str(e)}"}

async def run_standard_searches():
    """Run the standard searches and cache them."""
    print("Running standard searches...")
    
    for country in ["Kazakhstan", "Uzbekistan"]:
        try:
            print(f"Running standard search for {country}...")
            result = search_vacancies_in_kz(
                keywords=KEYWORDS_DEFAULT,
                country=country,
                pages=100,
                per_page=100
            )
            
            if "error" not in result:
                write_standard_cache(country, result)
                print(f"Standard search completed for {country}: {result['total_found']} jobs found")
            else:
                print(f"Error in standard search for {country}: {result['error']}")
                
        except Exception as e:
            print(f"Exception during standard search for {country}: {e}")

async def standard_search_scheduler():
    """Schedule standard searches to run daily at 06:00 Almaty time."""
    almaty_tz = ZoneInfo("Asia/Almaty")
    
    while True:
        try:
            now = datetime.now(almaty_tz)
            next_run = now.replace(hour=6, minute=0, second=0, microsecond=0)
            
            # If it's already past 6 AM today, schedule for tomorrow
            if now.hour >= 6:
                next_run += timedelta(days=1)
            
            wait_seconds = (next_run - now).total_seconds()
            print(f"Next standard search scheduled for {next_run} Almaty time (in {wait_seconds/3600:.1f} hours)")
            
            # Wait until the scheduled time
            await asyncio.sleep(wait_seconds)
            
            # Run the searches
            await run_standard_searches()
            
        except Exception as e:
            print(f"Error during scheduled standard searches: {e}")
        # Small delay before computing next run
        await asyncio.sleep(1)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway."""
    return {"status": "healthy", "message": "HH KZ CAD Jobs API is running"}

@app.get("/jobs")
def get_jobs(
    keywords: List[str] = Query(default=KEYWORDS_DEFAULT, description="Keywords to search"),
    country: str = Query(default="Kazakhstan", description="Country to search in"),
    pages: int = Query(default=5, description="Number of pages to search"),
    per_page: int = Query(default=20, description="Results per page"),
    city_filter: str = Query(default=None, description="Filter by city")
):
    """Get job vacancies with optional city filtering."""
    try:
        # Limit pages and per_page to prevent timeouts
        pages = min(pages, 10)  # Max 10 pages
        per_page = min(per_page, 50)  # Max 50 per page
        
        print(f"Received request: keywords={keywords}, country={country}, pages={pages}, per_page={per_page}")
        
        # Check if this is a standard search and we have cached results
        if is_standard_search(keywords, country, pages, per_page):
            standard_cache = read_standard_cache(country)
            if standard_cache:
                print(f"Serving standard search from cache for {country}")
                return standard_cache
        
        # Otherwise, perform a regular search
        result = search_vacancies_in_kz(keywords, country, pages, per_page, city_filter)
        print(f"Search completed, returning {result.get('total_found', 0)} results")
        return result
        
    except Exception as e:
        print(f"Error in get_jobs: {e}")
        return {"error": f"Internal server error: {str(e)}"}

@app.post("/trigger-standard-searches")
async def trigger_standard_searches():
    """Manually trigger standard searches."""
    await run_standard_searches()
    return {"message": "Standard searches completed"}

@app.get("/standard-cache-status")
def get_standard_cache_status():
    """Check the status of standard cache files."""
    status = {}
    for country in ["Kazakhstan", "Uzbekistan"]:
        cache_data = read_standard_cache(country)
        status[country] = {
            "cached": cache_data is not None,
            "total_jobs": cache_data.get("total_found", 0) if cache_data else 0,
            "cache_date": cache_data.get("cache_date", "N/A") if cache_data else "N/A"
        }
    return status

# Simple startup event handler
@app.on_event("startup")
async def startup_event():
    """Start the scheduler when the app starts."""
    try:
        print("Starting HH KZ CAD Jobs application...")
        # Start the scheduler in the background
        asyncio.create_task(standard_search_scheduler())
        print("Application startup complete!")
    except Exception as e:
        print(f"Error during startup: {e}")
        # Don't let startup errors crash the app

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable (Railway provides this)
    port = int(os.environ.get("PORT", 8080))
    
    # Use 0.0.0.0 for production, 127.0.0.1 for development
    host = "0.0.0.0"
    
    # Disable reload in production
    reload = os.environ.get("ENVIRONMENT") != "production"
    
    print(f"Starting server on {host}:{port}, reload={reload}")
    print(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    
    uvicorn.run("app:app", host=host, port=port, reload=reload, log_level="info")
