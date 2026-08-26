from google.adk.agents.llm_agent import Agent


root_agent = Agent(
    model='gemini-flash-latest',
    name='root_agent',
    description="The agent assists students with academic information and student-specific queries.",
    instruction="",
    tools=[],
    static_instruction="You are a students assistant that tells the academic information and student-specific queries."
)