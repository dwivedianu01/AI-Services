import configparser
import os
import requests


"""
Adzuna API wrapper
Fetches jobs for a given title and location.

Credentials can be provided via environment variables:
- ADZUNA_APP_ID
- ADZUNA_APP_KEY
- If not provided, the tool will also try to read from the repository's config.ini
  under the ADZUNA section. If absent there as well, it will fall back to empty strings
  which will cause Adzuna API requests to fail gracefully.
"""


def _load_credentials_from_config() -> tuple[str, str]:
    # Look for config.ini in the same repo (job-analysis-tool/backend/config.ini)
    cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
    if not os.path.exists(cfg_path):
        return (None, None)
    parser = configparser.ConfigParser()
    parser.read(cfg_path)
    app_id = parser.get("ADZUNA", "app_id", fallback=None)
    app_key = parser.get("ADZUNA", "app_key", fallback=None)
    if app_id:
        app_id = str(app_id).strip()
    if app_key:
        app_key = str(app_key).strip()
    return (app_id, app_key)


def _load_credentials() -> tuple[str, str]:
    # Priority: environment variables, then config.ini
    app_id = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_APP_KEY")
    if app_id and app_key:
        return app_id, app_key
    cfg_app_id, cfg_app_key = _load_credentials_from_config()
    if cfg_app_id and cfg_app_key:
        return cfg_app_id, cfg_app_key
    # Fallback to empty strings (will cause request to fail gracefully)
    return ("", "")


APP_ID, APP_KEY = _load_credentials()


def fetch_jobs(title: str, location: str = "India", results_per_page: int = 5):
    """Fetch job postings from Adzuna API for a given title and location.

    Returns a list of simplified job dicts:
    - title
    - company
    - location
    - description (trimmed to 300 chars)
    - redirect_url
    """
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": results_per_page,
        "what": title,
        "where": location,
    }
    print(params)
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json() or {}
        results = data.get("results", [])
        jobs = []
        for item in results:
            jobs.append(
                {
                    "title": item.get("title"),
                    "company": item.get("company", {}).get("display_name"),
                    "location": item.get("location", {}).get("display_name"),
                    "description": (item.get("description") or "")[:300],
                    "redirect_url": item.get("redirect_url"),
                }
            )
        return jobs
    else:
        # Non-200 responses return empty list; callers can decide how to handle
        return []
