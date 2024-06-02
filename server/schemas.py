from pydantic import BaseModel

class PythonCode(BaseModel):
    code: str

class ExecutionOutput(BaseModel):
    message: str