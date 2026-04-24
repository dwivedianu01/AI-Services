import requests

# Replace with your Adzuna credentials
APP_ID = "6b60b0b7"
APP_KEY = "cc632f404c3793b4ee3e9c9a191d6b0b"

def fetch_jobs(title: str, location: str = "India", results_per_page: int = 5):
    """
    Fetch job descriptions from Adzuna API by job title and location.
    """
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": results_per_page,
        "what": title,   # job title
        "where": location
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        jobs = response.json().get("results", [])
        for job in jobs:
            print("Title:", job.get("title"))
            print("Company:", job.get("company", {}).get("display_name"))
            print("Location:", job.get("location", {}).get("display_name"))
            print("Description:", job.get("description")[:300], "...")
            print("-" * 80)
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    # Example usage
    fetch_jobs("AI Engineer", "India", results_per_page=5)
