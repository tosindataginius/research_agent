from datetime import datetime
from services.llm import invoke_with_clean_errors, llm

def write_report(topic, findings, citations):
    # Dynamically fetch the accurate current date from the host machine
    current_date = datetime.now().strftime("%B %d, %Y")

    # Clean, structurally-enforced prompt mapping
    prompt = f"""You are a professional corporate analyst. Generate an authoritative business report.

REPORT METADATA:
- Topic: {topic}
- Date: {current_date}

DATA CONTEXT:
Use only the following analyzed data and citations to fill out the structure.
--- Research Findings ---
{findings}

--- Sources & Citations ---
{citations}

REQUIRED OUTPUT FORMAT:
You must strictly format the report using these five markdown headers. Do not invent metadata or dates outside what is provided.

## 1 Executive Summary
[Write a detailed, high-level overview of the findings and core intent here]

## 2 Findings
[Flesh out detailed points here, incorporating the research text and keeping inline citation numbers]

## 3 Challenges
[Identify and explain any challenges or limitations found in the research, citing sources as needed]

## 4 Recommendations
[Provide logical, actionable steps based directly on the findings]

## 5 Conclusion
[Summarize the final outcomes and synthesis]

## 6 References
[List all the source URLs and citations cleanly here]

Begin the report directly with a title block containing the Topic and the provided Date ({current_date}):"""

    result = invoke_with_clean_errors(llm, prompt)
    return result.content



# Script to test the writer function independently
if __name__ == "__main__":
    test_topic = "The Impact of Artificial Intelligence on Employment"
    test_findings = "AI is expected to automate many jobs, but also create new ones. The economic impact of AI could lead to increased productivity but also wage polarization."
    test_citations = "[1] AI and Job Market - http://example.com/ai-jobs\n[2] Economic Effects of AI - http://example.com/ai-economy"
    
    report = write_report(test_topic, test_findings, test_citations)
    print(f"Generated Report for '{test_topic}':\n{report}")
