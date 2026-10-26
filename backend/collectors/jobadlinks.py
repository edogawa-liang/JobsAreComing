import requests


BASE_URL = "https://links.api.jobtechdev.se/joblinks"


def search_jobs(query: str, limit: int = 50) -> list:
    """
    Search jobs using Sweden's JobAd Links API.
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
    Convert JobAd Links response into
    JobsAreComing's standard job format.
    """

    employer = job.get("employer") or {}
    address = job.get("workplace_address") or {}
    source_links = job.get("source_links") or []

    # Find a usable original job URL.
    source_url = None

    for link in source_links:
        if isinstance(link, dict):
            source_url = (
                link.get("url")
                or link.get("href")
                or link.get("link")
            )

            if source_url:
                break

    return {
        "job_id": job.get("id"),
        "source": "jobadlinks",
        "title": job.get("headline"),
        "company": employer.get("name"),
        "country": "Sweden",
        "city": address.get("municipality"),
        "description": job.get("brief"),
        "published_at": job.get("publication_date"),
        "source_url": source_url,
        "raw_data": job
    }