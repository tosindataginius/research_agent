from services.llm import llm

def research(topic, sources):
    # Formats each source into a clean, compact block with clear delimiters
    source_items = []
    for i, s in enumerate(sources, start=1):
        source_block = (
            f"--- SOURCE [{i}] ---\n"
            f"Title: {s['title']}\n"
            f"URL: {s['url']}\n"
            f"Content: {s['body']}"
        )
        source_items.append(source_block)
    
    # Joins sources with two clean lines separating them
    source_text = "\n\n".join(source_items)

    # Clean, direct prompt structure to maximize instruction adherence
    prompt = f"""You are an expert researcher. Research this topic: {topic}

CRITICAL INSTRUCTIONS:
1. Use ONLY the supplied sources below to form your answers.
2. For EVERY claim or fact you state, you MUST cite the source using its index number in brackets, for example: [1] or.
3. Do not invent information outside of these sources.

Sources:
{source_text}

Generate findings and include your inline citations:"""

    result = llm.invoke(prompt)
    return result.content

# Script to test the researcher function independently
if __name__ == "__main__":
    test_topic = "The Impact of Artificial Intelligence on Employment"
    test_sources = [
        {"title": "AI and Job Market", "url": "http://example.com/ai-jobs", "body": "AI is expected to automate many jobs, but also create new ones."},
        {"title": "Economic Effects of AI", "url": "http://example.com/ai-economy", "body": "The economic impact of AI could lead to increased productivity but also wage polarization."}
    ]
    findings = research(test_topic, test_sources)
    print(f"Research Findings for '{test_topic}':\n{findings}")