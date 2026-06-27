import requests
from bs4 import BeautifulSoup

def fetch_github_trending(language=None, since='daily'):
    """Fetches trending repositories from GitHub."""
    url = "https://github.com/trending"
    if language:
        url += f"/{language}"
    params = {'since': since}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        repos = []

        for article in soup.select('article.Box-row'):
            title_tag = article.select_one('h2 a')
            if not title_tag:
                continue

            repo_path = title_tag.get('href').strip('/')
            description = article.select_one('p')
            description = description.text.strip() if description else ""

            stars = article.select_one('a[href$="/stargazers"]')
            stars = stars.text.strip().replace(',', '') if stars else "0"

            repos.append({
                'source': 'GitHub',
                'name': repo_path,
                'url': f"https://github.com/{repo_path}",
                'description': description,
                'stars': int(stars)
            })

        return repos
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    print(fetch_github_trending(since='daily')[:5])
