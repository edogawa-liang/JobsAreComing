import requests


BASE_URL = "https://jobsearch.api.jobtechdev.se/search"


def search_jobs(query: str, limit: int = 20) -> list:
    """
    Search for jobs using Sweden's JobTech API.
    """

    params = {
        "q": query,
        "limit": limit,
        "offset": 0
    }

    headers = {
        "accept": "application/json"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data.get("hits", [])


def normalize_job(job: dict) -> dict:
    """
    Convert JobTech API response into
    a standardized job format.
    """

    employer = job.get("employer") or {}
    address = job.get("workplace_address") or {}
    description = job.get("description") or {}

    return {
        "job_id": job.get("id"),
        "source": "jobtech",
        "title": job.get("headline"),
        "company": employer.get("name"),
        "country": "Sweden",
        "city": address.get("municipality"),
        "description": description.get("text"),
        "published_at": job.get("publication_date"),
        "source_url": job.get("webpage_url")
    }