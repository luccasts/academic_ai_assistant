# Memory Contract

## Short-term memory

The agent MUST preserve conversation context
during a single session.

The conversation history MUST be available to the
agent when generating subsequent responses.

## Long-term memory

Long-term memory is optional in version 1.0.

If implemented, it MUST NOT alter the canonical
input/output contract.

## Session

Each conversation MUST have a unique session_id.