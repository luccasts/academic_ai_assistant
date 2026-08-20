# Tool Contract

The Academic AI Assistant interacts with external
academic capabilities through MCP-compatible tools.

The canonical contract defines tool behavior independently
of the MCP implementation.

Each implementation MUST expose equivalent tool
capabilities.

## get_student_profile

### Purpose

Retrieve the authenticated student's basic academic profile.

### Input

No user_id is provided by the agent.

The MCP server derives the user identity
from the authenticated context.

### Output

- student_id
- name
- course
- semester

### Authorization

Only the authenticated student's profile
may be returned.

## get_enrollments

### Purpose

Retrieve the authenticated student's current enrollments.

### Output

- course_id
- course_name
- semester
- status

## get_grades

### Purpose

Retrieve grades belonging to the authenticated student.

### Output

- course_id
- course_name
- assessment
- grade

## get_schedule

### Purpose

Retrieve the authenticated student's class schedule.

### Output

- course_id
- course_name
- day_of_week
- start_time
- end_time
- location