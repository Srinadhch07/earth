import csv
import time
from typing import Optional, List, Dict, Any

from serpapi import GoogleSearch


def scrape_jobs_google(
    api_key: str,
    query: str,
    location: str,
    output_csv: str = "jobs.csv",
    hl: str = "en",
    gl: str = "in",
    device: str = "desktop",
) -> Optional[str]:

    enhanced_query = (
        f"{query} site:linkedin.com OR site:indeed.com OR site:naukri.com"
    )

    params = {
        "engine": "google",
        "q": enhanced_query,
        "location": location,
        "hl": hl,
        "gl": gl,
        "device": device,
        "api_key": api_key,
    }

    try:
        search = GoogleSearch(params)
        results: Dict[str, Any] = search.get_dict()

        # 🔍 Handle SerpAPI response-level errors
        error_msg = results.get("error")
        if error_msg:
            error_lower = error_msg.lower()

            if "exceeded" in error_lower:
                print("SerpAPI credit limit exceeded")
                return None

            if "rate limit" in error_lower:
                print(" Rate limited by SerpAPI, retrying once...")
                time.sleep(2)
                results = GoogleSearch(params).get_dict()
            else:
                print(f" SerpAPI error: {error_msg}")
                return None

        job_results: List[Dict[str, Any]] = (
            results.get("organic_results")
            or results.get("jobs_results")
            or []
        )

        if not job_results:
            print(" No job results found")
            return None

        try:
            with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "position",
                        "title",
                        "source",
                        "snippet",
                        "link",
                        "displayed_link",
                    ],
                )
                writer.writeheader()

                for idx, job in enumerate(job_results, start=1):
                    writer.writerow({
                        "position": job.get("position", idx),
                        "title": job.get("title"),
                        "source": job.get("source") or job.get("company_name"),
                        "snippet": job.get("snippet") or job.get("description"),
                        "link": job.get("link")
                                or (job.get("related_links", [{}])[0].get("link")),
                        "displayed_link": job.get("displayed_link")
                                           or job.get("location"),
                    })

        except IOError as file_err:
            print(f" File write error: {file_err}")
            return None

        print(f" Saved {len(job_results)} jobs to {output_csv}")
        return output_csv

    except Exception as e:
        # This safely catches all SerpAPI / network / parsing issues
        print(f"❌ Unexpected error: {e}")
        return None
