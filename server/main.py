from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
import epicbox

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


@app.post("/test-code", response_model = schemas.ExecutionOutput)
def test_code(python_code: schemas.PythonCode, db: Session = Depends(get_db)):

    with open('server/user_code.py', 'w') as file:
        file.write(python_code.code)
    
    files = [{ 'name': 'user_code.py', 'content': python_code.code.encode('utf-8')}]
    output = epicbox.run('python', 'python3 user_code.py', files=files, limits=limits)

    if output['exit_code'] != 0:
        return schemas.ExecutionOutput(message=output['stderr'])
    
    return schemas.ExecutionOutput(message=output['stdout'])


