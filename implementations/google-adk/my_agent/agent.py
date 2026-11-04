"""Google ADK adapter for the framework-independent academic assistant."""
from __future__ import annotations

import sys
from pathlib import Path

from google.adk.agents.llm_agent import Agent
from tools import get_enrollments,  get_student_profile,  get_grades, get_schedule
PROJECT_ROOT = Path(__file__).resolve().parents[3] 
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shared.rag import retrieve


# def search_institutional_knowledge(question: str) -> dict:
#     """Search official institutional documents for academic facts and rules.

#     Use this tool before answering questions about calendars, courses,
#     prerequisites, academic regulations or institutional policies.
#     """
#     results = retrieve(question, n_results=3)
#     return {"query": question, "results": results}


root_agent = Agent(
    model="gemini-flash-latest",
    name="root_agent",
    description=(
        "Assists students with institutional academic information and "
        "student-specific questions."
    ),
    instruction=(
        "Responda em português. Para fatos institucionais, use "
        "search_institutional_knowledge e responda somente com base nos trechos "
        "recuperados. Cite o campo citation. Se a evidência não for suficiente, "
        "informe claramente que não encontrou a informação."
    ),
    tools=[get_enrollments, get_student_profile, get_grades, get_schedule],
)
