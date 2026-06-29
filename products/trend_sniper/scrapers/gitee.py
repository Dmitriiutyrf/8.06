import requests
from bs4 import BeautifulSoup

def fetch_gitee_trending(language='python'):
    """Fetches trending projects from Gitee (China's GitHub alternative)."""
    # Gitee uses a different structure for trending
    url = f"https://gitee.com/explore/{language if language else 'all'}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        repos = []

        # Note: Selectors for Gitee explore page
        for item in soup.select('.project-list-item')[:10]:
            title_tag = item.select_one('.repository')
            if not title_tag: continue

            name = title_tag.text.strip()
            link = f"https://gitee.com{title_tag.get('href')}"

            desc_tag = item.select_one('.project-desc')
            description = desc_tag.text.strip() if desc_tag else ""

            stars_tag = item.select_one('.stars-count')
            stars = stars_tag.text.strip() if stars_tag else "0"

            repos.append({
                'source': 'Gitee (China)',
                'name': name,
                'url': link,
                'description': description,
                'stars': int(stars) if stars.isdigit() else 100 # Default for trending
            })

        return repos
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    print(fetch_gitee_trending()[:3])
