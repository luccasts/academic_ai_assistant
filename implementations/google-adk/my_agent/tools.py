def get_student_profile():
    """
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
    """


def get_enrollments():
    """
### Purpose

Retrieve the authenticated student's current enrollments.

### Output

- course_id
- course_name
- semester
- status
    """
    pass
def get_grades():
    """
    Purpose
        Retrieve grades belonging to the authenticated student.

        Output

        - course_id
        - course_name
        - assessment
        - grade
        ```
    """
   
    results = retrieve(question, n_results=3)
    return {"query": question, "results": results}

    pass
def get_schedule():
    pass