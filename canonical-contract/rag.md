# RAG Contract

## Purpose

The RAG system provides institutional knowledge
to the Academic AI Assistant.

## Knowledge Sources

The knowledge base may contain:

- Academic regulations
- Academic calendar
- Student handbook
- Course information
- Institutional policies

## Behavior

The agent MUST use RAG when the answer depends
on institutional documentation.

The agent MUST NOT fabricate information when
relevant information cannot be found.

## Response

When possible, the response SHOULD include
the source document used to generate the answer.