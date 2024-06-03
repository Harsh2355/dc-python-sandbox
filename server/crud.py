from sqlalchemy.orm import Session

from . import models, schemas

def submit_code(db: Session, python_code: schemas.PythonCode, execution_output: schemas.ExecutionOutput):
    code_to_submit = models.SubmittedCode(code=python_code.code, output=execution_output.message)
    db.add(code_to_submit)
    db.commit()
    db.refresh(code_to_submit)
    return execution_output