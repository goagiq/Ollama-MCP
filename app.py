try:
    from praisonaiagents import Agent, MCP
    print("PraisonAI agents imported successfully!")
except ImportError as e:
    print(f"ImportError: {e}")

search_agent = Agent(
    instructions="""
    You help book an apartment on Airbnb. 
    You will provide a list of apartments with the best one based on price per night, location, and amenities.
    You will also need to check the availability of the apartment for the given dates.
    """,
    llm="ollama/mistral",
    tools=MCP("npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt")
)

search_agent.start("Search for an apartment in Paris from 2025-08-01 to 2025-08-15 with a budget of $100 per night.")
