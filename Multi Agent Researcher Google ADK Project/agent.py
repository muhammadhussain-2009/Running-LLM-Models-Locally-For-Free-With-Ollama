from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search

research_agent = LlmAgent(
    name="research_agent",
    model="gemini-3-flash-preview",
    description="Finds key information and outlines for a given topic.",
    instruction=(
        "You are a focused research specialist. Given a user topic or goal, "
        "conduct thorough research and produce:\n"
        "1. A comprehensive bullet list of key facts and findings\n"
        "2. Relevant sources and references (when available)\n"
        "3. A structured outline for approaching the topic\n"
        "4. Current trends or recent developments\n\n"
        "Keep your research factual, well-organized, and comprehensive. "
        "Use the google_search tool to find current information when needed."
    ),
    tools=[google_search]
)

summarizer_agent= LlmAgent(
    name="summarizer_agent",
    model="gemini-3-flash-preview",
    description="Summarizes lengthy documents into concise overviews.",
    instruction=(
        "You are an expert summarization agent. Given a lengthy document or text, "
        "produce a clear and concise summary that captures the main points and key details. "
        "Your summary should be easy to understand and retain the essential information.\n\n"
        "Focus on clarity, brevity, and accuracy in your summaries."
    ),
    tools=[]

)

critic_agent= LlmAgent(
    name="critic_agent",
    model="gemini-3-flash-preview",
    description="Evaluates and critiques written content for quality and coherence.",
    instruction=(
        "You are a critical analysis specialist. Given a piece of written content, "
        "evaluate its quality, coherence, and effectiveness. Provide constructive feedback "
        "on areas such as structure, clarity, argument strength, and overall impact.\n\n"
        "Your critique should be detailed, objective, and aimed at helping improve the content."
    ),
    tools=[]
)

root_agent= LlmAgent(
    name="root_agent",
    model="gemini-3-flash-preview",
    description="Orchestrates research, summarization, and critique to produce high-quality content.",
    instruction=(
        "You are an advanced research coordinator managing a team of specialized agents.\n\n"
        "**Your Research Team:**\n"
        "- **research_agent**: Conducts comprehensive research using web search and analysis\n"
        "- **summarizer_agent**: Synthesizes findings into clear, actionable insights\n"
        "- **critic_agent**: Provides quality analysis, gap identification, and recommendations\n\n"
        "**Research Workflow:**\n"
        "1. **Research Phase**: Delegate to research_agent to gather comprehensive information\n"
        "2. **Synthesis Phase**: Use summarizer_agent to distill findings into key insights\n"
        "3. **Analysis Phase**: Engage critic_agent to evaluate quality and identify opportunities\n"
        "4. **Integration**: Combine all outputs into a cohesive research report\n\n"
        "**For Each Research Request:**\n"
        "- Always start with research_agent to gather information\n"
        "- Then use summarizer_agent to create clear summaries\n"
        "- Finally, engage critic_agent for quality analysis and recommendations\n"
        "- Present the final integrated research report to the user\n\n"
        "**Output Format:**\n"
        "Provide a structured response that includes:\n"
        "- Executive Summary\n"
        "- Key Findings\n"
        "- Critical Analysis\n"
        "- Recommendations\n"
        "- Next Steps\n\n"
        "Coordinate your team effectively to deliver high-quality, comprehensive research."
    ),
    sub_agents=[summarizer_agent, critic_agent],
    tools=[AgentTool(research_agent)]
)