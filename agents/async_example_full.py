import asyncio
import time
from typing import List, Dict
from praisonaiagents import Agent, Task, PraisonAIAgents, TaskOutput
from duckduckgo_search import DDGS
from pydantic import BaseModel

# 1. Define async tool
class SearchResult(BaseModel):
    query: str
    results: List[Dict[str, str]]
    total_results: int

async def async_search_tool(query: str) -> Dict:
    """
    Asynchronous search using DuckDuckGo.
    Args:
        query (str): The search query.
    Returns:
        dict: Search results in SearchResult model format
    """
    await asyncio.sleep(1)  # Simulate network delay
    try:
        results = []
        ddgs = DDGS()
        for result in ddgs.text(keywords=query, max_results=5):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })
        
        # Format response to match SearchResult model
        return {
            "query": query,
            "results": results,
            "total_results": len(results)
        }
    except Exception as e:
        print(f"Error during async search: {e}")
        return {
            "query": query,
            "results": [],
            "total_results": 0
        }

# 2. Define async callback
async def async_callback(output: TaskOutput):
    await asyncio.sleep(1)  # Simulate processing
    if output.output_format == "JSON":
        print(f"Processed JSON result: {output.json_dict}")
    elif output.output_format == "Pydantic":
        print(f"Processed Pydantic result: {output.pydantic}")

# 3. Create specialized agents
async_agent = Agent(
    name="AsyncSearchAgent",
    role="Asynchronous Search Specialist",
    goal="Perform fast and efficient asynchronous searches with structured results",
    backstory="Expert in parallel search operations and data retrieval",
    tools=[async_search_tool],
    self_reflect=False,
    verbose=True,
    markdown=True
)

summary_agent = Agent(
    name="SummaryAgent",
    role="Research Synthesizer",
    goal="Create comprehensive summaries and identify patterns across multiple search results",
    backstory="""Expert in analyzing and synthesizing information from multiple sources.
Skilled at identifying patterns, trends, and connections between different topics.
Specializes in creating clear, structured summaries that highlight key insights.""",
    self_reflect=True,  # Enable self-reflection for better summary quality
    verbose=True,
    markdown=True
)

# 4. Create async tasks
async_task = Task(
    name="async_search",
    description="""Search for 'Async programming' and return results in the following JSON format:
{
    "query": "the search query",
    "results": [
        {
            "title": "result title",
            "url": "result url",
            "snippet": "result snippet"
        }
    ],
    "total_results": number of results
}""",
    expected_output="SearchResult model with query details and results",
    agent=async_agent,
    async_execution=True,
    callback=async_callback,
    output_pydantic=SearchResult
)

# 6. Example usage functions
async def run_single_task():
    """Run single async task"""
    print("\nRunning Single Async Task...")
    agents = PraisonAIAgents(
        agents=[async_agent],
        tasks=[async_task],
        verbose=1,
        process="sequential"
    )
    result = await agents.astart()
    print(f"Single Task Result: {result}")

async def run_parallel_tasks():
    """Run multiple async tasks in parallel"""
    print("\nRunning Parallel Async Tasks...")
    
    # Define different search topics
    search_topics = [
        "Latest AI Developments 2024",
        "Machine Learning Best Practices",
        "Neural Networks Architecture"
    ]
    
    # Create tasks for different topics
    parallel_tasks = [
        Task(
            name=f"search_task_{i}",
            description=f"""Search for '{topic}' and return results in the following JSON format:
{{
    "query": "{topic}",
    "results": [
        {{
            "title": "result title",
            "url": "result url",
            "snippet": "result snippet"
        }}
    ],
    "total_results": number of results
}}""",
            expected_output="SearchResult model with detailed information",
            agent=async_agent,
            async_execution=True,
            callback=async_callback,
            output_pydantic=SearchResult
        ) for i, topic in enumerate(search_topics)
    ]
    
    # Create summarization task with the specialized summary agent
    summary_task = Task(
        name="summary_task",
        description="""As a Research Synthesizer, analyze the search results and create a comprehensive summary. Your task:

1. Analyze Results:
   - Review all search results thoroughly
   - Extract key findings from each topic
   - Identify main themes and concepts

2. Find Connections:
   - Identify relationships between topics
   - Spot common patterns or contradictions
   - Note emerging trends across sources

3. Create Structured Summary:
   - Main findings per topic
   - Cross-cutting themes
   - Emerging trends
   - Practical implications
   - Future directions

4. Quality Checks:
   - Ensure all topics are covered
   - Verify accuracy of connections
   - Confirm clarity of insights
   - Validate practical relevance

Present the summary in a clear, structured format with sections for findings, patterns, trends, and implications.""",
        expected_output="""A comprehensive research synthesis containing:
- Detailed findings from each search topic
- Cross-topic patterns and relationships
- Emerging trends and their implications
- Practical applications and future directions""",
        agent=summary_agent,  # Use the specialized summary agent
        async_execution=False,  # Run synchronously after search tasks
        callback=async_callback
    )
    
    # Create a single PraisonAIAgents instance with both agents
    agents = PraisonAIAgents(
        agents=[async_agent, summary_agent],  # Include both agents
        tasks=parallel_tasks + [summary_task],  # Include all tasks
        verbose=1,
        process="sequential"  # Tasks will run in sequence, with parallel tasks running first
    )
    
    # Run all tasks
    results = await agents.astart()
    print(f"Tasks Results: {results}")
    
    # Return results in a serializable format
    return {
        "search_results": {
            "task_status": {k: v for k, v in results["task_status"].items() if k != summary_task.id},
            "task_results": [str(results["task_results"][i]) if results["task_results"][i] else None 
                           for i in range(len(parallel_tasks))]
        },
        "summary": str(results["task_results"][summary_task.id]) if results["task_results"].get(summary_task.id) else None,
        "topics": search_topics
    }

# 7. Main execution
async def main():
    """Main execution function"""
    print("Starting Async AI Agents Examples...")
    
    try:
        # Run different async patterns
        await run_single_task()
        await run_parallel_tasks()
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())