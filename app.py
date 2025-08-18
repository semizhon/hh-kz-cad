
# app.py
import os, time, requests, json
from datetime import date, datetime
from pathlib import Path
from typing import Optional
from typing import List, Dict, Any
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

HH_API = "https://api.hh.ru"
# Use your email in UA to be a good API citizen (optional but recommended)
UA = os.environ.get("HH_USER_AGENT", "HH-KZ-CAD-Jobs/1.0 (mumble_subject_0a@icloud.com)")
KEYWORDS_DEFAULT = ["AutoCAD,Revit,Inventor,Fusion 360,Fusion,Advance Steel"]

app = FastAPI(title="HH KZ CAD Jobs API", version="1.0.0")

# Setup templates
templates = Jinja2Templates(directory="templates")

# --- tiny TTL cache to be friendly to hh.ru ---
_cache: Dict[str, Any] = {}
def cache_get(key, ttl_sec=180):
    v = _cache.get(key)
    if not v: return None
    ts, data = v
    return data if (time.time() - ts) < ttl_sec else None

def cache_set(key, data):
    _cache[key] = (time.time(), data)

# --- daily snapshot cache (persisted to disk) ---
DAILY_CACHE_DIR = Path(os.environ.get("DAILY_CACHE_DIR", "daily_cache"))
DAILY_SNAPSHOT_FILE = DAILY_CACHE_DIR / "jobs_snapshot.json"

def _today_str() -> str:
    return date.today().isoformat()

def read_daily_snapshot_if_fresh() -> Optional[Dict[str, Any]]:
    try:
        if not DAILY_SNAPSHOT_FILE.exists():
            return None
        with DAILY_SNAPSHOT_FILE.open("r", encoding="utf-8") as f:
            snapshot = json.load(f)
        if snapshot.get("date") == _today_str():
            return snapshot
        return None
    except Exception:
        # On any read/parse error, ignore snapshot
        return None

def write_daily_snapshot(payload: Dict[str, Any], request_params: Dict[str, Any]) -> None:
    try:
        DAILY_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        snapshot = {
            "date": _today_str(),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "request_params": request_params,
            "payload": payload,
        }
        with DAILY_SNAPSHOT_FILE.open("w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False)
    except Exception:
        # Best-effort persistence; don't crash request handler
        pass

def hh_get(path, params=None):
    r = requests.get(
        f"{HH_API}{path}",
        params=params or {},
        headers={"User-Agent": UA, "Accept": "application/json"},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()

def get_area_id_for_country(country_name="Kazakhstan") -> str:
    """Find country 'Kazakhstan' in areas tree and return its id."""
    cache_key = "areas_tree"
    data = cache_get(cache_key, ttl_sec=3600)
    if not data:
        data = hh_get("/areas")  # full tree of countries/regions/cities
        cache_set(cache_key, data)
    
    # Map English country names to their possible Cyrillic equivalents
    country_mapping = {
        "kazakhstan": ["казахстан", "kz", "40"],
        "russia": ["россия", "рф", "ru", "1"],
        "ukraine": ["украина", "ua", "5"],
        "belarus": ["беларусь", "by", "16"],
        "uzbekistan": ["узбекистан", "uz", "97"],
        "kyrgyzstan": ["кыргызстан", "kg", "48"],
        "tajikistan": ["таджикистан", "tj", "86"],
        "turkmenistan": ["туркменистан", "tm", "87"],
        "azerbaijan": ["азербайджан", "az", "9"],
        "georgia": ["грузия", "ge", "28"],
        "armenia": ["армения", "am", "6"],
        "moldova": ["молдова", "md", "50"]
    }
    
    search_terms = [country_name.lower()]
    if country_name.lower() in country_mapping:
        search_terms.extend(country_mapping[country_name.lower()])
    
    for country in data:
        country_name_lower = country.get("name", "").lower()
        country_id = str(country.get("id", ""))
        
        if country_name_lower in search_terms or country_id in search_terms:
            return country_id
    
    raise RuntimeError(f"Country '{country_name}' not found in HH areas")

def get_company_details(employer_id: str) -> dict:
    """Get detailed company information including phone numbers."""
    cache_key = f"employer_{employer_id}"
    data = cache_get(cache_key, ttl_sec=3600)  # cache for 1 hour
    if not data:
        try:
            data = hh_get(f"/employers/{employer_id}")
            cache_set(cache_key, data)
        except:
            data = {}
    return data

def get_company_vacancies_count(employer_id: str) -> int:
    """Get total number of vacancies for a company from company details."""
    if not employer_id:
        return 0
    
    # Get company details which should contain "open_vacancies" field
    company_details = get_company_details(employer_id)
    
    # Look for "open_vacancies" field in the company details
    # This is the "активные вакансии" field
    open_vacancies = company_details.get("open_vacancies")
    if open_vacancies is not None:
        return open_vacancies
    
    # Also check for "active_vacancies" or similar fields as fallback
    active_vacancies = company_details.get("active_vacancies")
    if active_vacancies is not None:
        return active_vacancies
    
    # Also check for "vacancies_count" or similar fields
    vacancies_count = company_details.get("vacancies_count")
    if vacancies_count is not None:
        return vacancies_count
    
    # If not found, return 0
    return 0

def search_vacancies_in_kz(keywords: List[str], country="Kazakhstan", per_page=100, pages=1, products=None):
    area_id = get_area_id_for_country(country)
    print(f"Searching in {country} (area_id: {area_id})")

    seen, results = set(), []
    company_stats = {}  # Track company statistics
    
    # Process keywords - handle both individual keywords and comma-separated strings
    processed_keywords = []
    for kw in keywords:
        if ',' in kw:
            # Split comma-separated keywords
            processed_keywords.extend([k.strip() for k in kw.split(',') if k.strip()])
        else:
            processed_keywords.append(kw.strip())
    
    # Remove duplicates while preserving order
    unique_keywords = []
    for kw in processed_keywords:
        if kw not in unique_keywords:
            unique_keywords.append(kw)
    
    print(f"Processed keywords: {unique_keywords}")
    
        # COMPREHENSIVE SEARCH: Search each keyword with full pagination
    # HeadHunter API doesn't support OR syntax, so we search each keyword separately
    # and paginate through all specified pages for comprehensive results
    for kw in unique_keywords:
        print(f"Searching for keyword: {kw}")
        
        # Search through all specified pages for this keyword
        for page in range(pages):
            params = {
                "text": kw,
                "area": area_id,                       # filter to selected country
                "per_page": per_page,                  # use full per_page value
                "page": page,                          # paginate through all pages
                "order_by": "publication_time",
            }
            
            try:
                print(f"Making API call with params: {params}")
                data = hh_get("/vacancies", params)
                print(f"API response: {len(data.get('items', []))} items found")
                items = data.get("items", [])
                
                # If no items returned, we've reached the end
                if not items:
                    print(f"No more results for keyword '{kw}' at page {page}")
                    break
                
                for item in items:
                    vid = item.get("id")
                    if vid in seen:
                        continue
                    seen.add(vid)
                    
                    employer = item.get("employer") or {}
                    employer_id = employer.get("id")
                    company_name = employer.get("name")
                    
                    # Get company details and total vacancies only once per company
                    if company_name not in company_stats:
                        company_details = get_company_details(employer_id) if employer_id else {}
                        total_vacancies = get_company_vacancies_count(employer_id) if employer_id else 0
                        
                        company_stats[company_name] = {
                            "total_vacancies": total_vacancies,
                            "autodesk_vacancies": 0,
                            "phone": company_details.get("contacts", {}).get("phones", [{}])[0].get("number") if company_details.get("contacts", {}).get("phones") else None,
                            "website": company_details.get("site_url"),
                            "description": company_details.get("description"),
                            "logo_url": company_details.get("logo_url"),
                            "employer_id": employer_id
                        }
                    company_stats[company_name]["autodesk_vacancies"] += 1
                    
                    # Process salary information
                    salary = item.get("salary")
                    salary_fmt = None
                    if salary:
                        frm = salary.get("from")
                        to = salary.get("to")
                        cur = salary.get("currency")
                        parts = [f"{frm:,}" if frm else None, f"{to:,}" if to else None]
                        rng = "–".join([p for p in parts if p])
                        salary_fmt = f"{rng} {cur}".strip() if rng else None

                    # Apply product filtering if specified
                    if products:
                        # Check if any of the products are mentioned in the job
                        job_text = f"{item.get('name', '')} {item.get('snippet', {}).get('requirement', '')} {item.get('snippet', {}).get('responsibility', '')}"
                        job_text_lower = job_text.lower()
                        if not any(product.lower() in job_text_lower for product in products):
                            continue
                    
                    # Detect all mentioned products in job title and description
                    job_text = f"{item.get('name', '')} {item.get('snippet', {}).get('requirement', '')} {item.get('snippet', {}).get('responsibility', '')}"
                    job_text_lower = job_text.lower()
                    
                    mentioned_products = []
                    all_products = [
                        "AutoCAD", "Revit", "Inventor", "Fusion 360", "Fusion", "Advance Steel",
                        "Civil 3D", "Civil3D", "InfraWorks", "Navisworks", "BIM360", "BIM 360",
                        "Autodesk", "3ds Max", "3DS Max", "PowerMill", "FeatureCAM", "Autodesk CFD",
                        "автокад"  # Russian/Cyrillic version of AutoCAD
                    ]
                    
                    for product in all_products:
                        if product.lower() in job_text_lower:
                            mentioned_products.append(product)
                    
                    # If no products detected, use the source keyword
                    if not mentioned_products:
                        mentioned_products = [kw]
                    
                    results.append({
                        "id": vid,
                        "title": item.get("name"),
                        "company": company_name,
                        "company_id": employer_id,
                        "city": (item.get("area") or {}).get("name"),
                        "published_at": item.get("published_at"),
                        "url": item.get("alternate_url"),
                        "employment": (item.get("employment") or {}).get("name"),
                        "schedule": (item.get("schedule") or {}).get("name"),
                        "salary_raw": item.get("salary"),
                        "salary": salary_fmt,
                        "source_keyword": kw,
                        "mentioned_products": mentioned_products,
                        "company_phone": company_stats[company_name]["phone"],
                        "company_website": company_stats[company_name]["website"],
                        "company_description": company_stats[company_name]["description"],
                        "company_logo": company_stats[company_name]["logo_url"],
                        "total_vacancies": company_stats[company_name]["total_vacancies"],
                        "autodesk_vacancies": company_stats[company_name]["autodesk_vacancies"]
                    })
                
                # If we got fewer items than per_page, we've reached the end
                if len(items) < per_page:
                    print(f"Reached end of results for keyword '{kw}' at page {page}")
                    break
                    
            except Exception as e:
                print(f"Error searching for keyword '{kw}' at page {page}: {e}")
                continue

    results.sort(key=lambda x: x.get("published_at") or "", reverse=True)
    return results

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/jobs")
def get_jobs(
    keywords: List[str] = Query(default=KEYWORDS_DEFAULT, description="Keywords to search"),
    country: str = Query(default="Kazakhstan", description="Country to search in"),
    pages: int = Query(default=1),
    per_page: int = Query(default=100),
    products: List[str] = Query(default=[], description="Filter by specific products"),
):
    # 1) Serve today's persisted snapshot if present (global for the day)
    daily_snapshot = read_daily_snapshot_if_fresh()
    if daily_snapshot and daily_snapshot.get("payload"):
        return JSONResponse(daily_snapshot["payload"])

    # 2) Fallback to short-lived in-memory cache (prevents duplicate work within a couple of minutes)
    cache_key = f"jobs:{country}:{','.join(keywords)}:{pages}:{per_page}:{','.join(products)}"
    cached = cache_get(cache_key, ttl_sec=120)
    if cached:
        return JSONResponse(cached)

    try:
        data = search_vacancies_in_kz(keywords, country=country, per_page=per_page, pages=pages, products=products)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    payload = {
        "query": {"keywords": keywords, "country": country, "pages": pages, "per_page": per_page},
        "count": len(data),
        "items": data,
        "source": "api.hh.ru",
    }
    cache_set(cache_key, payload)

    # 3) Persist as today's snapshot so subsequent requests serve the same data today
    write_daily_snapshot(
        payload=payload,
        request_params={
            "keywords": keywords,
            "country": country,
            "pages": pages,
            "per_page": per_page,
            "products": products,
        },
    )
    return JSONResponse(payload)

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get("PORT", 8080))
    
    # Use 0.0.0.0 for production, 127.0.0.1 for development
    host = "0.0.0.0"
    
    # Disable reload in production
    reload = os.environ.get("ENVIRONMENT") != "production"
    
    uvicorn.run("app:app", host=host, port=port, reload=reload)
