def format_sources(sources):

    formatted = []

    for i, src in enumerate(sources, start=1):

        formatted.append(f""" [{i}] {src['title']} | URL: {src['url']}""")

    return "\n".join(formatted)



# Script to test the format_sources function independently
if __name__ == "__main__":
    test_sources = [
        {"title": "AI and Job Market", "url": "http://example.com/ai-jobs", "body": "AI is expected to automate many jobs, but also create new ones."},
        {"title": "Economic Effects of AI", "url": "http://example.com/ai-economy", "body": "The economic impact of AI could lead to increased productivity but also wage polarization."}
    ]
    formatted_citations = format_sources(test_sources)
    print(f"Formatted Citations:\n{formatted_citations}")