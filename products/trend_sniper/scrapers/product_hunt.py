import requests
from bs4 import BeautifulSoup

def fetch_product_hunt():
    """Fetches today's top products from Product Hunt (Simplified Scraper)."""
    url = "https://www.producthunt.com/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        products = []

        # Note: Product Hunt structure changes often, this is a simplified version
        for item in soup.select('[data-test^="product-item-"]')[:10]:
            name_tag = item.select_one('[data-test="product-item-name"]')
            if not name_tag: continue

            name = name_tag.text.strip()
            desc_tag = item.select_one('[data-test="product-item-tagline"]')
            description = desc_tag.text.strip() if desc_tag else ""

            link_tag = item.select_one('a[href^="/posts/"]')
            link = f"https://www.producthunt.com{link_tag.get('href')}" if link_tag else url

            upvotes_tag = item.select_one('[data-test="vote-button"]')
            upvotes = upvotes_tag.text.strip() if upvotes_tag else "0"

            products.append({
                'source': 'Product Hunt',
                'name': name,
                'url': link,
                'description': description,
                'stars': int(upvotes) if upvotes.isdigit() else 0
            })

        return products
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    print(fetch_product_hunt()[:5])
