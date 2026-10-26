import json
from pathlib import Path

import requests

from backend.config.search_config import SEARCH_KEYWORDS

from backend.collectors import jobtech
from backend.collectors import jobadlinks


def save_jobs(jobs: list):
    """
    Save collected jobs into a JSON file.
    """

    output_path = Path("data/jobs.json")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            jobs,
            file,
            ensure_ascii=False,
            indent=2
        )


def main():

    print("JobsAreComing — Multi-Source Job Collection")
    print("--------------------------------------------")

    collectors = [
        ("JobSearch", jobtech),
        ("JobAd Links", jobadlinks)
    ]

    all_jobs = {}

    for source_name, collector in collectors:

        print(f"\n=== Searching {source_name} ===")

        for keyword in SEARCH_KEYWORDS:

            print(f"\nKeyword: {keyword}")

            try:
                raw_jobs = collector.search_jobs(
                    query=keyword,
                    limit=50
                )

                for raw_job in raw_jobs:

                    job = collector.normalize_job(raw_job)

                    job_id = job.get("job_id")

                    if not job_id:
                        continue

                    # Unique ID within each API source
                    unique_key = (
                        job["source"],
                        str(job_id)
                    )

                    all_jobs[unique_key] = job

                print(f"Retrieved {len(raw_jobs)} jobs")

            except requests.RequestException as error:

                print(
                    f"Search failed for "
                    f"{source_name} / {keyword}: {error}"
                )

    jobs = list(all_jobs.values())

    save_jobs(jobs)

    print("\n--------------------------------------------")
    print(f"Total unique source records: {len(jobs)}")
    print("Saved to data/jobs.json")


if __name__ == "__main__":
    main()