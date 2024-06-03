from sqlalchemy.orm import Session

from . import models, schemas

"""
Submit the provided Python code and its execution output to the database.

Parameters:
- db (Session): The database session to use for the operation.
- python_code (schemas.PythonCode): The Python code to submit.
- execution_output (schemas.ExecutionOutput): The output of executing the Python code.

Returns:
- schemas.ExecutionOutput: The execution output that was submitted.

"""
def submit_code(db: Session, python_code: schemas.PythonCode, execution_output: schemas.ExecutionOutput) -> schemas.ExecutionOutput:
    code_to_submit = models.SubmittedCode(code=python_code.code, output=execution_output.message)
    db.add(code_to_submit)
    db.commit()
    db.refresh(code_to_submit)
    return execution_output