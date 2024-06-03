from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
import epicbox
import subprocess
import os

CURRENT_DIR = './server'
CONTAINER_NAME = 'code_sandbox'

epicbox.configure(
    profiles=[
        epicbox.Profile('python', 'python:3.11-alpine3.19'),
    ]
)

limits = {
    # CPU time in seconds, None for unlimited
    'cputime': 2,
    # Real time in seconds, None for unlimited
    'realtime': 10,
    # Memory in megabytes, None for unlimited
    'memory': 128,
    # Limit the max processes the sandbox can have, -1 or None for unlimited(default)
    'processes': 5,
}


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# Enable all CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Function to get a database session.

Returns:
    Session: A database session to be used for database operations.
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Function to handle the startup event of the FastAPI application.

This function is triggered when the FastAPI application starts up. It builds a Docker image named 'code_sandbox'
where all user code is executed.
"""
@app.on_event("startup")
async def startup_event():
    # Build the Docker image
    build_process = subprocess.run(['docker', 'build', '-t', CONTAINER_NAME, CURRENT_DIR], capture_output=True, text=True)


"""
Execute the provided Python code in a secure Docker container.

Parameters:
    code (str): The Python code to be executed.

Returns:
    tuple: A tuple containing the standard output and standard error of the executed code.
"""
def execute_code(code: str) -> tuple[str, str]:
    try:
        with open('server/user_code.py', 'w') as file:
            file.write(code)
    except:
        return "", "Could not open user code file..."
    
    # Run the Docker container and capture output
    # Setup a timeout to protect against large malicious operations
    # No network connectivity means user code can't communicate over the network making the container more secure
    # Restrict resource utilzation to enhance security against untrusted/maliciuos code
    run_process = subprocess.run(['docker', 'run', '--network', 'none', '--ulimit', 'cpu=5:5', '--cpus=1.0', '--memory=512m', '--pids-limit=20', '--rm', '-v', f"{os.getcwd()}/server/user_code.py:/usr/src/app/user_code.py", CONTAINER_NAME], capture_output=True, text=True)

    return run_process.stdout, run_process.stderr


"""
Endpoint to test and run user-provided Python code.

Args:
    python_code (schemas.PythonCode): The Python code provided by the user.
    db (Session, optional): The database session to be used for database operations. Defaults to Depends(get_db).

Returns:
    schemas.ExecutionOutput: The output message from executing the provided Python code.

Notes:
    This endpoint writes the user-provided Python code to a file, 
    runs it in a Docker container with restricted resources, and captures the output. 
    If the execution is successful, the output is persisted in the database.
"""
@app.post("/test-code", response_model = schemas.ExecutionOutput)
def test_code(python_code: schemas.PythonCode, db: Session = Depends(get_db)) -> schemas.ExecutionOutput:

    stdout, stderr = execute_code(python_code.code)
    
    if stdout == "":
        return schemas.ExecutionOutput(message=stderr)
    
    return schemas.ExecutionOutput(message=stdout)


"""
Submit the provided Python code for execution and store the output in the database.

Args:
    python_code (schemas.PythonCode): The Python code to be submitted for execution.
    db (Session, optional): The database session to be used for database operations. Defaults to Depends(get_db).

Returns:
    schemas.ExecutionOutput: The execution output message after submitting the code for execution.
"""
@app.post("/submit", response_model = schemas.ExecutionOutput)
def submit(python_code: schemas.PythonCode, db: Session = Depends(get_db)) -> schemas.ExecutionOutput:

    stdout, stderr = execute_code(python_code.code)
    
    if stdout == "":
        return schemas.ExecutionOutput(message=f'Could not submit...\n {stderr}')
    
    # persists in db
    output: schemas.ExecutionOutput = schemas.ExecutionOutput(message=stdout)

    try:
        crud.submit_code(db, python_code, output)
    except:
        return schemas.ExecutionOutput(message='Something went wrong while submitting...')

    return schemas.ExecutionOutput(message='Congrats! Your code has been sucessfully submitted.')

