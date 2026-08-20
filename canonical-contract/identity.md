# Identity Contract

## User Context

Every authenticated request MUST provide:

- user_id
- role
- institution_id
- session_id

## Roles

Supported roles:

- student
- staff
- administrator

## Authorization

The agent MUST only access information allowed
for the authenticated user.

Student-specific tools MUST operate on the
authenticated user's identity.

The agent MUST NOT accept an arbitrary user_id
provided by the model as authorization.