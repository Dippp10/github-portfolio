import requests
import os

USERNAME = "Dippp10"
TOKEN = os.getenv("GH_TOKEN")

headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

repos = []
page = 1

while True:
    url = f"https://api.github.com/user/repos?per_page=100&page={page}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if not data:
        break
    repos.extend(data)
    page += 1

# Sort: public first
repos.sort(key=lambda r: r["private"])

with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# Consolidated Repository List\n\n")
    f.write("| Repository | Stars | Forks | Visibility | Score |\n")
    f.write("|------------|-------|-------|------------|-------|\n")

    for repo in repos:
        name = repo["name"]
        url = repo["html_url"]
        stars = repo["stargazers_count"]
        forks = repo["forks_count"]
        visibility = "Private" if repo["private"] else "Public"

        score = min(10, round(1 + (stars + forks) / 10, 1))

        f.write(f"| [{name}]({url}) | {stars} | {forks} | {visibility} | {score} |\n")
