import csv
from typing import List, Optional
from jobspy import scrape_jobs
import pandas as pd


def scrape_jobs_platform(
    site_names: List[str],
    search_term: str,
    location: str,
    results_wanted: int = 20,
    hours_old: int = 72,
    country_indeed: str = "INDIA",
    google_search_term: Optional[str] = None,
    linkedin_fetch_description: bool = True,
    output_csv: str = "jobs.csv",
) -> Optional[str]:
    """
    Scrape jobs from multiple platforms using JobSpy.

    Handles:
    - Invalid inputs
    - Network / scraping failures
    - Empty results
    - CSV write errors
    - Unexpected crashes
    """

    if not site_names or not isinstance(site_names, list):
        print("Invalid site_names provided")
        return None

    if not search_term or not search_term.strip():
        print("search_term is required")
        return None

    if not location or not location.strip():
        print("location is required")
        return None

    if results_wanted <= 0 or results_wanted > 200:
        print("results_wanted must be between 1 and 200")
        return None

    if hours_old <= 0:
        print("hours_old must be greater than 0")
        return None

    try:
        jobs = scrape_jobs(
            site_name=site_names,
            search_term=search_term,
            google_search_term=google_search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_indeed=country_indeed,
            linkedin_fetch_description=linkedin_fetch_description,
        )

    except TimeoutError:
        print("Network timeout while scraping job platforms")
        return None

    except Exception as e:
        print(f"JobSpy scraping error: {e}")
        return None

    if jobs is None:
        print("JobSpy returned None")
        return None

    if not isinstance(jobs, pd.DataFrame):
        print("Unexpected JobSpy return type")
        return None

    print(f"Found {len(jobs)} jobs")

    if jobs.empty:
        print("No jobs found")
        return None

    try:
        jobs.to_csv(
            output_csv,
            quoting=csv.QUOTE_NONNUMERIC,
            escapechar="\\",
            index=False
        )
    except PermissionError:
        print("Permission denied while writing CSV")
        return None
    except FileNotFoundError:
        print("Invalid file path for CSV")
        return None
    except Exception as e:
        print(f"CSV write error: {e}")
        return None

    print(f"Jobs successfully saved to {output_csv}")
    return output_csv
