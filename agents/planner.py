# Import the actual instance directly
from services.llm import llm

def plan(topic):
    prompt = f"""You are an elite research strategist. Create a highly focused research plan.

Topic: {topic}

Provide an actionable, step-by-step checklist of exactly what sub-topics must be explored to thoroughly understand this topic:
1.
2.
3."""

    
    result = llm.invoke(prompt) 
    return result.content

# Script to test the planner function independently
if __name__ == "__main__":
    test_topic = "The Future of Renewable Energy"
    research_plan = plan(test_topic)
    print(f"Research Plan for '{test_topic}':\n{research_plan}")

# The statement if __name__ == "__main__": is a standard Python idiom that acts as a gatekeeper. 
# It ensures that the block of code inside it only runs when you execute this specific script file directly, 
# but remains completely hidden if another file tries to import it.
