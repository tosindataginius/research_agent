import time
from ddgs import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException

def gather_sources(query, max_results=5):
    
    collected = []

    # Try up to 3 times before giving up
    for attempt in range(3):
        try:
            #  FIXED: Pass timeout=10 here to initialize the client session safely
            with DDGS(timeout=10) as ddgs:

                results = ddgs.text(query, max_results=max_results)
                for r in results:
                    collected.append({
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "body": r.get("body")
                    })
                return collected
        except DuckDuckGoSearchException as e:
            print(f"Search timeout/error on attempt {attempt + 1}: {e}")
            if attempt < 2:
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                print("All search attempts failed. Returning empty source list.")
                return []


# Script to test the search function independently
if __name__ == "__main__":
    test_query = "The Future of Renewable Energy"
    search_results = gather_sources(test_query)

    print(f"Search results for '{test_query}':")
    for i, source in enumerate(search_results, start=1):
        print(f"{i}. {source['title']} - {source['url']}")   

