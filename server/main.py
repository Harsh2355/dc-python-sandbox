from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
import epicbox
import subprocess
import os

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

# Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    # Build the Docker image
    build_process = subprocess.run(['docker', 'build', '-t', 'code_sandbox', './server'], capture_output=True, text=True)

def execute_code(code: str):
    with open('server/user_code.py', 'w') as file:
        file.write(code)
    
    # Run the Docker container and capture output
    # Setup a timeout to protect against large malicious operations
    # No network connectivity means user code can't communicate over the network making the container more secure
    # Restrict resource utilzation to enhance security against untrusted/maliciuos code
    run_process = subprocess.run(['docker', 'run', '--network', 'none', '--ulimit', 'cpu=5:5', '--cpus=1.0', '--memory=512m', '--pids-limit=20', '--rm', '-v', f"{os.getcwd()}/server/user_code.py:/usr/src/app/user_code.py", 'code_sandbox'], capture_output=True, text=True)
    
    return run_process.stdout, run_process.stderr

@app.post("/test-code", response_model = schemas.ExecutionOutput)
def test_code(python_code: schemas.PythonCode, db: Session = Depends(get_db)):

    stdout, stderr = execute_code(python_code.code)
    
    if stdout == "":
        return schemas.ExecutionOutput(message=stderr)
    
    return schemas.ExecutionOutput(message=stdout)

@app.post("/submit", response_model = schemas.ExecutionOutput)
def test_code(python_code: schemas.PythonCode, db: Session = Depends(get_db)):

    stdout, stderr = execute_code(python_code.code)
    
    if stdout == "":
        return schemas.ExecutionOutput(message=f'Could not submit...\n {stderr}')
    
    # persists in db
    output: schemas.ExecutionOutput = schemas.ExecutionOutput(message=stdout)
    crud.submit_code(db, python_code, output)

    return schemas.ExecutionOutput(message='Congrats! Your code has been sucessfully submitted.')

