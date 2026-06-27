from scrapers.github_trending import fetch_github_trending
from scrapers.hacker_news import fetch_hn_hype
from scrapers.product_hunt import fetch_product_hunt
from scrapers.gitee import fetch_gitee_trending
import concurrent.futures

class HunterEngine:
    def __init__(self):
        self.scrapers = [
            fetch_github_trending,
            fetch_hn_hype,
            fetch_product_hunt,
            fetch_gitee_trending
        ]

    def hunt(self, query='AI'):
        """Runs all scrapers and aggregates results."""
        all_results = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # GitHub trending doesn't take the query, but HN does
            future_to_scraper = {
                executor.submit(fetch_github_trending): 'GitHub',
                executor.submit(fetch_hn_hype, query): 'HN',
                executor.submit(fetch_product_hunt): 'ProductHunt',
                executor.submit(fetch_gitee_trending): 'Gitee'
            }

            for future in concurrent.futures.as_completed(future_to_scraper):
                try:
                    data = future.result()
                    if isinstance(data, list) and len(data) > 0 and not data[0].get('error'):
                        all_results.extend(data)
                except Exception as e:
                    print(f"Scraper error: {e}")

        # Sort by 'stars' (hype factor) and take top picks
        sorted_results = sorted(all_results, key=lambda x: x.get('stars', 0), reverse=True)
        return sorted_results[:15]

    def analyze_monetization(self, project):
        """AI-style logic to suggest how to monetize a project."""
        name = project['name']
        desc = project['description'].lower()

        if 'ui' in desc or 'frontend' in desc:
            return "Mini-Agency: Build custom interfaces for local businesses using this tool."
        elif 'api' in desc or 'backend' in desc:
            return "Micro-SaaS: Wrap this API into a simple specialized service with a subscription."
        elif 'automation' in desc or 'agent' in desc:
            return "B2B Efficiency: Sell as an automation audit/implementation for mid-size companies."
        else:
            return "Content/Course: Create a 'How-to' guide or masterclass on mastering this tool."

if __name__ == "__main__":
    engine = HunterEngine()
    results = engine.hunt()
    for r in results[:3]:
        print(f"[{r['source']}] {r['name']} - {r['stars']} stars")
        print(f"Monetization Idea: {engine.analyze_monetization(r)}\n")
