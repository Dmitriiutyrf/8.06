import requests

def fetch_hn_hype(query='AI', hits_per_page=10):
    """Fetches hyped stories from Hacker News using Algolia API."""
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        'query': query,
        'tags': 'story',
        'numericFilters': 'points>50',
        'hitsPerPage': hits_per_page
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        stories = []
        for hit in data.get('hits', []):
            stories.append({
                'source': 'Hacker News',
                'name': hit.get('title'),
                'url': hit.get('url') or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                'description': f"Points: {hit.get('points')} | Comments: {hit.get('num_comments')}",
                'stars': hit.get('points') # Using points as stars equivalent
            })
        return stories
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    print(fetch_hn_hype()[:5])
