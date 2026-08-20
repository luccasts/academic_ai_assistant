# Canonical Contract

## Purpose

This document defines the framework-independent specification
for the Academic AI Assistant.

The system will be implemented using:

- Google ADK
- LangChain
- Agno

The canonical contract is the single source of truth for
all three implementations.

## Core Principle

The three implementations MUST provide equivalent behavior.

Framework-specific APIs, classes, configuration and terminology
MUST NOT leak into the canonical contract.

## Goals

The contract defines:

- Agent responsibilities
- Input and output formats
- Tools
- Memory
- User identity and permissions
- RAG behavior
- Workflows
- Error handling
- Evaluation criteria

## Architecture

User/Channel
    ↓
Canonical API
    ↓
Agent
    ├── RAG
    ├── MCP Tools
    └── Memory
    ↓
Canonical Response

## Implementations

Each framework implements this contract independently:

/google-adk
/langchain
/agno