# Workflow Contract

## Query Processing

Every user request follows this logical flow:

1. Receive canonical request.
2. Identify user context.
3. Determine user intent.
4. Determine whether external knowledge is required.
5. Determine whether a tool is required.
6. Execute the required operations.
7. Generate the final response.

## Knowledge Query

User
 ↓
Agent
 ↓
RAG
 ↓
Response

## Student Data Query

User
 ↓
Agent
 ↓
MCP Tool
 ↓
Response

## Combined Query

User
 ↓
Agent
 ├── RAG
 └── MCP
 ↓
Reasoning
 ↓
Response