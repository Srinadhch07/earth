import csv
from serpapi.google_search import GoogleSearch

API_KEY = "e0bbf7157b200e19940f6d9ac7e98d2f0d98b042494724e297da9ff7c13c3158"

params = {
    "engine": "google",
    "q": "junior product management or intern jobs in linkedin, indeed, naukri",
    "location": "Hyderabad, Telangana, India",
    "hl": "hi",
    "gl": "in",
    "device": "desktop",
    "api_key": API_KEY
}

search = GoogleSearch(params)
results = search.get_dict()

organic_results = results.get("organic_results", [])

if not organic_results:
    print("No job results found")
    exit()

csv_file = "jobs.csv"

with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
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

    for job in organic_results:
        writer.writerow({
            "position": job.get("position"),
            "title": job.get("title"),
            "source": job.get("source"),
            "snippet": job.get("snippet"),
            "link": job.get("link"),
            "displayed_link": job.get("displayed_link"),
        })

print(f"Saved {len(organic_results)} jobs to {csv_file}")
